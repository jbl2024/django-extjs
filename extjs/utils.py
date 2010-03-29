import datetime
import pickle
from copy import copy, deepcopy
from django import forms
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.forms import fields
from django.forms.models import ModelChoiceField, ModelMultipleChoiceField
from django.forms.forms import BoundField
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.serializers.json import Serializer as JSONSerializer
import simplejson
from django.utils.functional import Promise
from django.utils.encoding import force_unicode

class ExtJSONEncoder(DjangoJSONEncoder):
    """
    JSONEncoder subclass that knows how to encode django forms into ExtJS config objects.
    """

    CHECKBOX_EDITOR = {
        'xtype': 'checkbox'
    }
    COMBO_EDITOR = {
        'listWidth': 'auto',
        'value': '',
        'mode': 'local',
        'width': 150,
        'xtype': 'combo',
        'forceSelection': True,
        'editable': False,
        'triggerAction': 'all',
    }
    DATE_EDITOR = {
        'xtype': 'datefield'
    }
    EMAIL_EDITOR = {
        'vtype':'email',
        'xtype': 'textfield'
    }
    NUMBER_EDITOR = {
        'xtype': 'numberfield'
    }
    NULL_EDITOR = {
        'fieldHidden': True,
        'xtype': 'textfield'
    }
    TEXT_EDITOR = {
        'xtype': 'textfield'
    }
    TIME_EDITOR = {
        'xtype': 'timefield'
    }
    URL_EDITOR = {
        'vtype':'url',
        'xtype': 'textfield'
    }
    CHAR_PIXEL_WIDTH = 8

    EXT_DEFAULT_CONFIG = {
        'xtype': 'textfield',
        'labelWidth': 300,
        'autoWidth': True,
    }

    DJANGO_EXT_FIELD_TYPES = {
        fields.BooleanField: ["Ext.form.Checkbox", CHECKBOX_EDITOR],
        fields.CharField: ["Ext.form.TextField", TEXT_EDITOR],
        fields.SlugField: ["Ext.form.TextField", TEXT_EDITOR],
        fields.ChoiceField: ["Ext.form.ComboBox", COMBO_EDITOR],
        fields.TypedChoiceField: ["Ext.form.ComboBox", COMBO_EDITOR],
        fields.DateField: ["Ext.form.DateField", DATE_EDITOR],
        fields.DateTimeField: ["Ext.form.DateField", DATE_EDITOR],
        fields.DecimalField: ["Ext.form.NumberField", NUMBER_EDITOR],
        fields.EmailField: ["Ext.form.TextField", EMAIL_EDITOR],
        fields.IntegerField: ["Ext.form.NumberField", NUMBER_EDITOR],
        ModelChoiceField: ["Ext.form.ComboBox", COMBO_EDITOR],
        ModelMultipleChoiceField: ["Ext.form.ComboBox", COMBO_EDITOR],
        fields.MultipleChoiceField: ["Ext.form.ComboBox",COMBO_EDITOR],
        fields.NullBooleanField: ["Ext.form.Checkbox", CHECKBOX_EDITOR],
        fields.SplitDateTimeField: ["Ext.form.DateField", DATE_EDITOR],
        fields.TimeField: ["Ext.form.DateField", TIME_EDITOR],
        fields.URLField: ["Ext.form.TextField", URL_EDITOR],
    }

    EXT_DATE_ALT_FORMATS = 'm/d/Y|n/j/Y|n/j/y|m/j/y|n/d/y|m/j/Y|n/d/Y|m-d-y|m-d-Y|m/d|m-d|md|mdy|mdY|d|Y-m-d'

    EXT_TIME_ALT_FORMATS = 'm/d/Y|m-d-y|m-d-Y|m/d|m-d|d'

    DJANGO_EXT_FIELD_ATTRS = {
        #Key: django field attribute name
        #Value: tuple[0] = ext field attribute name,
        #       tuple[1] = default value
        'choices': ['store', None],
        #'default': ['value', None],
        'fieldset': ['fieldSet', None],
        'help_text': ['helpText', None],
        'initial': ['value', None],
        'label': ['fieldLabel', None],
        'max_length': ['maxLength', None],
        'max_value': ['maxValue', None],
        'min_value': ['minValue', None],
        'name': ['name', None],
        'required': ['allowBlank', False],
        'size': ['width', None],
        'hidden': ['fieldHidden', False],
        'value': ['value', False],
    }

    def default(self, o):
        """Serializer
        """
        # Serialize : Forms
        if issubclass(o.__class__, forms.Form) or issubclass(o.__class__, forms.ModelForm):
            flds = []

            for name, field in o.fields.items():
                if isinstance(field, dict):
                    field['title'] = name
                else:
                    field.name = name
                # Bound fields with data
                bf = BoundField(o, field, name)
                cfg = self.default(bf)
                flds.append(cfg)

            return flds

        if isinstance(o, Promise):
            return force_unicode(o)

        # Serialize : Dict
        elif isinstance(o, dict):
            #Fieldset
            default_config = {
                'autoHeight': True,
                'collapsible': True,
                'items': [],
                'labelWidth': 200,
                'title': o['title'],
                'xtype':'fieldset',
            }
            del o['title']

            #Ensure fields are added sorted by position
            for name, field in sorted(o.items()):
                field.name = name
                default_config['items'].append(self.default(field))
            return default_config

        # Serialize BoundFields
        elif issubclass(o.__class__, BoundField):
            # print o.field.__class__
            default_config = {}
            if o.field.__class__ in self.DJANGO_EXT_FIELD_TYPES:
                default_config.update(self.DJANGO_EXT_FIELD_TYPES[o.field.__class__][1])
                #print default_config
            else:
                default_config.update(self.EXT_DEFAULT_CONFIG['editor'])
            config = deepcopy(default_config)
            for dj, ext in self.DJANGO_EXT_FIELD_ATTRS.items():
                v = None
                # Adapt the value with type of field
                if dj == 'size':
                    v = o.field.widget.attrs.get(dj, None)
                    if v is not None:
                        if o.field.__class__ in (fields.DateField, fields.DateTimeField, fields.SplitDateTimeField, fields.TimeField):
                            v += 8
                        #Django's size attribute is the number of characters,
                        #so multiply by the pixel width of a character
                        v = v * self.CHAR_PIXEL_WIDTH
                elif dj == 'hidden':
                    v = o.field.widget.attrs.get(dj, default_config.get('fieldHidden', ext[1]))
                elif dj == 'name':
                    v = o.field.name
                elif dj == 'value':
                    # Get value depends of source
                    # http://code.djangoproject.com/browser/django/trunk/django/forms/forms.py#L432
                    if not o.form.is_bound:
                        data = o.form.initial.get(o.name, o.field.initial)
                        if callable(data):
                            data = data()
                        # temp hack for Checkbox
                        if not data and isinstance(o.field, fields.BooleanField):
                            data = o.data
                    else:
                        data = o.data
                    v = data
                elif dj == 'label':
                    v = o.field.widget.attrs.get(dj, None)
                    if v is None:
                        v = o.field.label
                        if v is None:
                            v = o.field.name
                        else:
                            v = force_unicode(v)
                elif getattr(o.field, dj, ext[1]) is None:
                    pass
                elif isinstance(ext[1], basestring):
                    v = getattr(o.field, dj, getattr(field, ext[1]))
                elif dj == 'choices':
                    v = getattr(o.field, dj, None)
                else:
                    v = getattr(o.field, dj, ext[1])

                # Time to use v
                if v is not None:
                    ejs, df = ext # extjsfield name, default value
                    if ejs == 'value':
                        config[ejs] = v
                    if ejs == 'name':
                        config[ejs] = v
                        config['header'] = v
                        if default_config == self.COMBO_EDITOR:
                            config['hiddenName'] = v
                    elif ejs not in ('dataIndex', 'fieldLabel', 'header', 'defaultValue'):
                        if ejs == 'store':
                            config[ejs] = [ [force_unicode(y), force_unicode(z)] for y, z in v]
                        else:
                            config[ejs] = v

                    elif isinstance(v, unicode):
                        config[ext[0]] = v.encode('utf8')
                    else:
                        config[ext[0]] = v
            return config
        elif issubclass(o.__class__, models.Model):
            return force_unicode(o)
        else:
            # Go up
            return super(ExtJSONEncoder, self).default(o)


class ExtJSONSerializer(JSONSerializer):
    """Convert a queryset into
    """
    def end_object(self, obj):
        """Don't add pk, model"""
        self.objects["data"].append(self._current)
        self._current = None

    def end_serialization(self):
        self.options.pop('stream', None)
        self.options.pop('fields', None)
        self.options.pop('use_natural_keys', None)
        extjs = self.options.pop('extjs', None)
        simplejson.dump(self.objects, self.stream, cls=ExtJSONEncoder, **self.options)
    def start_serialization(self):
        self._current = None
        self.message = getattr(self.options, "message", None)
        self.objects = {"success": True, "data":[]}
        if self.message:
            self.objects["message"] = self.message

def JsonResponse(content, *args, **kwargs):
    return HttpResponse(content, mimetype='text/javascript', *args, **kwargs)

def JsonError(error = ''):
    result = {"success": False, "msg": error }
    return JsonResponse(simplejson.dumps(result, cls=ExtJSONEncoder))

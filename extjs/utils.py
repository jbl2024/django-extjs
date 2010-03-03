import datetime
import pickle
from copy import copy, deepcopy
from django import forms
from django.core.serializers.json import DjangoJSONEncoder
from django.forms import fields
from django.forms.models import ModelChoiceField, ModelMultipleChoiceField
from django.forms.forms import BoundField
from django.http import Http404, HttpResponse, HttpResponseRedirect

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
        'xtype': 'combo'
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
                    v = o.data
                elif dj == 'label':
                    v = o.field.widget.attrs.get(dj, None)
                    if v is None:
                        v = o.field.name
                elif getattr(o.field, dj, ext[1]) is None:
                    pass
                elif isinstance(ext[1], basestring):
                    v = getattr(o.field, dj, getattr(field, ext[1]))
                elif dj == 'choices':
                    v = getattr(o.field, dj, None)
                else:
                    v = getattr(o.field, dj, ext[1])


                #print dj, ext, v
                #print
                # Time to use v
                if v is not None:
                    ejs, df = ext # extjsfield name, default value
                    if ejs == 'value':
                        config[ejs] = v
                    if ejs == 'name':
                        config[ejs] = v
                        config['header'] = v
                    elif ejs not in ('dataIndex', 'fieldLabel', 'header', 'defaultValue'):
                        if ejs == 'store':
                            config[ejs] = [ [unicode(y), unicode(z)] for y, z in v]
                        else:
                            config[ejs] = v

                    elif isinstance(v, unicode):
                        config[ext[0]] = v.encode('utf8')
                    else:
                        config[ext[0]] = v
            return config
        else:
            return super(ExtJSONEncoder, self).default(o)

# =========== TODO : Delete
def datetimeFromExtDateField(indatestr):
    if indatestr.count("T")>0:
        (date, time) = indatestr.split("T")
        (an, mois, jour) = date.split('-')
        (h, m, s) = time.split(':')
        return datetime.datetime(int(an), int(mois), int(jour), int(h), int(m), int(s))
    elif indatestr.count("/") == '2':
        if indatestr.count(' ')>0:
            (date, time) = indatestr.split(" ")
            (jour, mois, an) = date.split('/')
            (h, m, s) = time.split(':')
            return datetime.datetime(int(an), int(mois), int(jour), int(h), int(m), int(s))
        else:
            (jour, mois, an) = date.split('/')
            return datetime.date(int(an), int(mois), int(jour))
    return None


def DateFormatConverter(to_extjs = None, to_python = None):
    """ convert date formats between ext and python """
    f = {}
    f['a'] = 'D'
    f['A'] = 'l'
    f['b'] = 'M'
    f['B'] = 'F'
    #f['c'] =
    f['d'] = 'd'
    f['H'] = 'H'
    f['I'] = 'h'
    f['j'] = 'z'
    f['m'] = 'm'
    f['M'] = 'i'
    f['p'] = 'A'
    f['S'] = 's'
    f['U'] = 'W'
    #f['w'] =
    f['W'] = 'W'
    #f['x'] =
    #f['X'] =
    f['y'] = 'y'
    f['Y'] = 'Y'
    f['Z'] = 'T'
    out = ''
    if to_extjs:
        for char in to_extjs.replace('%',''):
            out += f.get(char, char)
    elif to_python:
        for char in to_python:
            if char in f.values():
                key = [key for key, val in f.items() if f[key] == char][0]
                out += '%%%s' % key
            else:
                out += char

    return out



def JsonResponse(contents, status=200):
    return HttpResponse(contents, mimetype='text/javascript', status=status)

def JsonSuccess(params = {}):
    d = {"success":True}
    d.update(params)
    return JsonResponse(JSONserialise(d))

def JsonError(error = ''):
    return JsonResponse('{"success":false, "msg":%s}' % JSONserialise(error))

def JSONserialise(obj):
    import simplejson
    return simplejson.dumps(obj, cls=ExtJsEncoder,)

def JSONserialise_dict_item(key, value, sep = '"'):
    # quote the value except for ExtJs keywords
    if key in ['renderer', 'editor', 'hidden', 'sortable', 'sortInfo', 'listeners', 'view', 'failure', 'success','scope', 'fn','store','handler','callback']:
        if u'%s' % value in ['True', 'False']:
            value = str(value).lower()
        else:
            # dont escape strings inside these special values (eg; store data)
            value = JSONserialise(value, sep='', escapeStrings = False)
        return '"%s":%s' % (key, value)
    else:
        value = JSONserialise(value, sep)
        return '"%s":%s' % (key, value)

def JSONserialise_dict(inDict):
    data=[]
    for key in inDict.keys():
        data.append(JSONserialise_dict_item(key, inDict[key]))
    data = ",".join(data)
    return "{%s}" % data

def JsonCleanstr(inval):
    try:
        inval = u'%s' % inval
    except:
        print "ERROR nunicoding %s" % inval
        pass
    inval = inval.replace('"',r'\"')
    inval = inval.replace('\n','\\n').replace('\r','')
    return inval
# =====================


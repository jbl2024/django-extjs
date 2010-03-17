import utils

import forms
from django.db import models

# width, dateFormat, renderer, hidden, align, type

class SimpleGrid(object):
    def to_grid(self, fields, rows, totalcount = None, json_add = {}, sort_field = 'id', sort_direction = 'DESC'):
        if not totalcount:
            totalcount = len(rows)
        jdict = {
            'success':True
           ,'metaData':{
                'root':'rows'
                ,'totalProperty':'totalCount'
                ,'successProperty':'success'
                ,'sortInfo':{
                   'field': sort_field
                   ,'direction': sort_direction
                }
                ,'fields':fields
                }
                ,'rows':rows
                ,'totalCount':totalcount
            }
        return utils.JSONserialise(jdict)


class VirtualField(object):
    def __init__(self, name):
        self.name = name

class ModelGrid(object):
    fields = None
    #exclude = None
    model = None

    def __init__(self, model=None, exclude=None, fields=None):
        """ Initialize the grid with params given on ModelGrid Definition or
        __init__
        """
        # Model
        model = model or self.model
        if not model or not issubclass(model, models.Model):
            raise IndexError("Please give a Model")
        else:
            self.model = model      # the model to use as reference

        # Excludes and Includes
        #exclude = exclude or self.exclude

        self.columns = {}        # holds the fields

        model_fields = self.model._meta._fields()
        base_fields = model_fields

        # Model base fields and needed fields
        self.mfields = [ f.name for f in model_fields ]
        self.fields = fields or self.fields or self.mfields

        # Get good field config for fields
        for field in base_fields:
            # Excludes and includes
            #if fields:
            #    if field.name not in fields:
            #        continue
            #elif exclude:
            #    if field.name in exclude:
            #        continue

            # XXX VirtualField  : wtf ?
            if field.__class__.__name__ == VirtualField:
                self.fields.append(self.Meta.fields_conf[field.name])
                continue
            fdict = {'name':field.name, 'header': field.name}

            if getattr(field, 'verbose_name', None):
                fdict['tooltip'] = u'%s' %  field.verbose_name

            if field.name == 'id':
                fdict['id']='id'
            if isinstance(field, models.DateTimeField):
                fdict['type'] = 'datetime'
                fdict['xtype'] = 'datecolumn'
                fdict['dateFormat'] = 'Y-m-d H:i:s'
                fdict['format'] = 'Y-m-d H:i:s'
            elif isinstance(field, models.DateField):
                fdict['type'] = 'date'
                fdict['xtype'] = 'datecolumn'
                fdict['dateFormat'] = 'Y-m-d'
                fdict['format'] = 'Y-m-d'
            elif isinstance(field, models.IntegerField):
                fdict['xtype'] = 'numbercolumn'
            elif isinstance(field, models.BooleanField):
                fdict['xtype'] = 'booleancolumn'
            elif isinstance(field, models.DecimalField):
                fdict['xtype'] = 'numbercolumn '
                fdict['renderer'] = 'function(v) {return (v.toFixed && v.toFixed(2) || 0);}'
            elif isinstance(field, models.ForeignKey):
                pass
            elif field.choices:
                #print 'FIELD CHOICES', field.choices
                a = {}
                for c in field.choices:
                    a[c[0]] = c[1]
                #fdict['renderer'] = 'function(v) {a = %s; return a[v] || "";}' % utils.JSONserialise(a)

            self.columns[field] = fdict

    def get_rows(self, queryset, start=0, limit=0, fields=None, *args, **kwargs):
        """
            return list from given queryset
            order the data based on given field list
            paging from start,limit
        """
        if not fields:
            fields = self.fields

        if limit > 0:
            queryset = queryset[int(start):int(start) + int(limit)]

        # Now update with specials methods
        data = []
        for obj in queryset:
            row = {}
            for field in fields:
                row[field] = getattr(obj, field)
            data.append(row)

        return data, len(data)

    def get_rows_json(self, queryset, jsonerror=True, *args, **kwargs):
        """
            return json message from given queryset
            order the data based on given field list
            paging from start,limit
        """
        try :
            data, length = self.get_rows(queryset, *args, **kwargs)
        except Exception, e:
            # TODO : replace with loggin solution
            if not jsonerror:
                raise e
            result = {'success': False, "message": "Error : %s" % e}
        else:
            result = {"data" : data, "success": True, "results": length}
        from django.core.serializers.json import DjangoJSONEncoder as Djson
        json_enc = Djson(ensure_ascii=False)
        return json_enc.encode(result)

    def to_store(self, fields=None, url=None, *args, **kwargs):
        """Create DataStore for this grid
        """
        if not fields:
            fields = self.fields

        field_list = []
        for field in fields:
            for f in self.columns.values():
                if f['name'] == field:
                    field_list.append(f)
        result = {'fields': field_list}
        if url:
            result['url'] = url
        return result


    def to_grid(self, queryset, start = 0, limit = 0, totalcount = None, json_add = {}, sort_field = 'id', sort_direction = 'DESC'):
        """ return the given queryset as an ExtJs grid config
        includes full metadata (columns, renderers, totalcount...)
        includes the rows data
        to be used in combination with Ext.ux.AutoGrid
        """
        if not totalcount:
            totalcount = queryset.count()

        #base_fields = self.get_fields(colModel)

        # todo : stupid ?
        id_field = base_fields[0]['name']

        jsondict = {
             'succes':True
            ,'metaData':{
                 'root':'rows'
                ,'totalProperty':'totalCount'
                ,'successProperty':'success'
                ,'idProperty':id_field
                ,'sortInfo':{
                   "field": sort_field
                   ,"direction": sort_direction
                }
                ,'fields':base_fields
            }
            #,'rows':self.get_rows(base_fields, queryset, start, limit)
            ,'totalCount':totalcount
        }
        if json_add:
            jsondict.update(json_add)

        #return utils.JSONserialise(jsondict)

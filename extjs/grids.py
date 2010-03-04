
import utils

import forms

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
    def __init__(self, model):
        self.model = model      # the model to use as reference
        self.fields = {}        # holds the fields

        model_fields = self.model._meta._fields()
        base_fields = model_fields


        for field in base_fields:
            if field.__class__.__name__ == VirtualField:
                self.fields.append(self.Meta.fields_conf[field.name])
                continue
            fdict = {'name':field.name, 'header': field.name}

            if getattr(field, 'verbose_name', None):
                fdict['tooltip'] = u'%s' %  field.verbose_name

            if field.name == 'id':
                fdict['id']='id'
            if  field.__class__.__name__ == 'DateTimeField':
                fdict['type'] = 'datetime'
                fdict['xtype'] = 'datecolumn'
                fdict['dateFormat'] = 'Y-m-d H:i:s'
                fdict['format'] = 'Y-m-d H:i:s'
            if  field.__class__.__name__ == 'DateField':
                fdict['type'] = 'date'
                fdict['xtype'] = 'datecolumn'
                fdict['dateFormat'] = 'Y-m-d'
                fdict['format'] = 'Y-m-d'
            elif field.__class__.__name__ == 'IntegerField':
                fdict['xtype'] = 'numbercolumn'
            elif field.__class__.__name__ == 'BooleanField':
                fdict['xtype'] = 'booleancolumn'
            elif field.__class__.__name__ == 'DecimalField':
                fdict['xtype'] = 'numbercolumn '
                fdict['renderer'] = 'function(v) {return (v.toFixed && v.toFixed(2) || 0);}'
            elif  field.__class__.__name__ == 'ForeignKey':
                pass
            elif field.choices:
                #print 'FIELD CHOICES', field.choices
                a = {}
                for c in field.choices:
                    a[c[0]] = c[1]
                #fdict['renderer'] = 'function(v) {a = %s; return a[v] || "";}' % utils.JSONserialise(a)

            self.fields[field] = fdict

    def get_rows(self, queryset, start=0, limit=0, *args, **kwargs):
        """
            return json message from given queryset
            order the data based on given field list
            paging from start,limit
        """
        rows = []
        if limit > 0:
            queryset = queryset[int(start):int(start) + int(limit)]
        from utils import ExtJSONSerializer
        s = ExtJSONSerializer()
        return s.serialize(queryset, **kwargs)


    def to_grid(self, queryset, start = 0, limit = 0, totalcount = None, json_add = {}, sort_field = 'id', sort_direction = 'DESC'):
        """ return the given queryset as an ExtJs grid config
        includes full metadata (columns, renderers, totalcount...)
        includes the rows data
        to be used in combination with Ext.ux.AutoGrid
        """
        raise NotImplementedError("Not Ready yet")
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

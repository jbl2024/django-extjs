from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import simplejson
from django.conf import settings

from test_project.apps.testapp.forms import ContactForm, AuthorForm, AuthorxcludeForm, WhatamessForm
from test_project.apps.testapp.models import Author, Whatamess
from test_project.apps.testapp.models import AuthorGrid, AuthorGrid_nofields


class FormsTestCase(TestCase):
    def testFormbasic(self):
        cf = ContactForm()
        expct = {"items":[
            {'fieldLabel': 'subject', 'xtype': 'textfield', 'fieldHidden': False, 'name': 'subject', 'header': 'subject', 'helpText': '', 'maxLength': 100, 'allowBlank': True},
            {'fieldLabel': 'message', 'xtype': 'textfield', 'fieldHidden': False, 'value': 'pony', 'name': 'message', 'header': 'message', 'helpText': '', 'allowBlank': True},
            {'vtype': 'email', 'fieldLabel': 'sender', 'allowBlank': True, 'fieldHidden': False, 'name': 'sender', 'header': 'sender', 'helpText': '', 'xtype': 'textfield'},
            {'fieldLabel': 'cc_myself', 'xtype': 'checkbox', 'fieldHidden': False, 'value': False, 'name': 'cc_myself', 'header': 'cc_myself', 'helpText': '', 'allowBlank': False},
        ]}
        self.assertEqual(expct, simplejson.loads(cf.as_extjs()))
        cf = ContactForm({'subject':'PONY'})
        expct["items"][0]["value"] = "PONY"
        self.assertEqual(expct, simplejson.loads(cf.as_extjs()))

    def testModelFormbasic(self):
        cf = AuthorForm()
        expct = {"items":[
            {"fieldLabel": "name", "xtype": "textfield", "fieldHidden": False, "header": "name", "allowBlank": True, "helpText": "", "maxLength": 100, "name": "name", "value": "Platon"},
            {"xtype": "combo", "forceSelection": True, "editable": False, "triggerAction": 'all', "hiddenName": "title", "fieldLabel": "title", "name": "title", "header": "title", "fieldHidden": False, "value": "", "width": 150, "allowBlank": True, "helpText": "", "mode": "local", "store": [["", "---------"], ["MR", "Mr."], ["MRS", "Mrs."], ["MS", "Ms."]], "listWidth": "auto"},
            {"fieldLabel": "birth_date", "allowBlank": False, "fieldHidden": False, "name": "birth_date", "header": "birth_date", "helpText": "", "xtype": "datefield"}
            ]}
        self.assertEqual(expct, simplejson.loads(cf.as_extjs()))
        cf = AuthorForm({"name":"PONNY"})
        expct["items"][0]["value"] = "PONNY"
        self.assertEqual(expct, simplejson.loads(cf.as_extjs()))

    def testModelFormcomplex(self):
        cf = WhatamessForm()
        expct = {"items":[
            {"fieldLabel": "name", "xtype": "textfield", "fieldHidden": False, "header": "name", "allowBlank": True, "helpText": "", "maxLength": 100, "name": "name"},
            {"fieldLabel": "number", "allowBlank": True, "fieldHidden": False, "name": "number", "header": "number", "helpText": "", "xtype": "numberfield"},
            {"fieldLabel": "slug", "xtype": "textfield", "fieldHidden": False, "header": "slug", "allowBlank": True, "helpText": "", "maxLength": 50, "name": "slug"},
            {"fieldLabel": "text", "allowBlank": True, "fieldHidden": False, "name": "text", "header": "text", "helpText": "", "xtype": "textfield"},
            {"xtype": "combo", "forceSelection": True, "editable": False, "triggerAction": 'all', "hiddenName": "author", "fieldLabel": "author", "name": "author", "header": "author", "fieldHidden": False, "value": "", "width": 150, "allowBlank": True, "helpText": "", "mode": "local", "store": [["", "---------"]], "listWidth": "auto"},
            {"xtype": "combo", "forceSelection": True, "editable": False, "triggerAction": 'all', "hiddenName": "title", "fieldLabel": "title", "name": "title", "header": "title", "fieldHidden": False, "value": "", "width": 150, "allowBlank": True, "helpText": "", "mode": "local", "store": [["", "---------"], ["1", "Mr."], ["2", "Mrs."], ["3", "Ms."]], "listWidth": "auto"},
            {"fieldLabel": "birth_date", "allowBlank": False, "fieldHidden": False, "name": "birth_date", "header": "birth_date", "helpText": "", "xtype": "datefield"}, {"fieldLabel": "yesno", "xtype": "checkbox", "fieldHidden": False, "value": False, "header": "yesno", "allowBlank": False, "helpText": "", "name": "yesno"}
            ]}
        self.assertEqual(expct, simplejson.loads(cf.as_extjs()))

    def testModelFormexcludebasic(self):
        cf = AuthorxcludeForm()
        expct = {"items":[
            {"fieldLabel": "name", "xtype": "textfield", "fieldHidden": False, "header": "name", "allowBlank": True, "helpText": "", "maxLength": 100, "name": "name", "value": "Platon"},
            {"fieldLabel": "birth_date", "allowBlank": False, "fieldHidden": False, "name": "birth_date", "header": "birth_date", "helpText": "", "xtype": "datefield"}
            ]}
        self.assertEqual(expct, simplejson.loads(cf.as_extjs()))

class GridTestCase(TestCase):
    def setUp(self):
        """
        """
        from datetime import date
        self.auth1 = Author.objects.create(name="toto", title="ToTo", birth_date=date(2000,1,2))
        self.auth2 = Author.objects.create(name="tata", title="TaTa", birth_date=date(2001,2,3))
        self.auth3 = Author.objects.create(name="tutu", title="TuTu", birth_date=date(2002,3,4))

    def testGridbasic_old(self):
        """Get a query from a GridModel
        """
        return
        #qry = Author.objects.all()
        #expct = {u"success": True, u"data": [
        #    {u"birth_date": u"2000-01-02", u"name": u"toto", u"title": u"ToTo"},
        #    {u"birth_date": u"2001-02-03", u"name": u"tata", u"title": u"TaTa"},
        #    {u"birth_date": u"2002-03-04", u"name": u"tutu", u"title": u"TuTu"},
        #]}
        #ag = AuthorGrid()
        #jsonresult = ag.get_rows(qry)
        #result = simplejson.loads(jsonresult)
        #self.assertEqual(expct, result)

    def testGridbasic(self):
        """Get a query from a GridModel
        """
        qry = Author.objects.all()
        import datetime
        expct_data = [
            (u"toto", u"ToTo", datetime.date(2000, 1, 2)),
            (u"tata", u"TaTa", datetime.date(2001, 2, 3)),
            (u"tutu", u"TuTu", datetime.date(2002, 3, 4)),
        ]
        ag = AuthorGrid()
        raw_result, length = ag.get_rows(qry,)
        self.assertEqual(expct_data, raw_result)
        self.assertEqual(length, 3)

        # And now get result in JSONResponse
        expct_data = [
            [u"ToTo", u"2000-01-02", u"toto"],
            [u"TaTa", u"2001-02-03", u"tata"],
            [u"TuTu", u"2002-03-04", u"tutu"],
        ]
        expct = {u"success": True, u"data": expct_data, u'results': 3}
        jsonresult = ag.get_rows_json(qry, fields=['title', 'birth_date', 'name'])
        result = simplejson.loads(jsonresult)
        self.assertEqual(expct, result)

        # use pre-configured View
        response = self.client.get("/api/author/getjson")
        result = simplejson.loads(response.content)
        expct_data = [
            ["toto", "ToTo", "2000-01-02"],
            ["tata", "TaTa", "2001-02-03"],
            ["tutu", "TuTu", "2002-03-04"],
        ]
        expct = {"success": True, "data": expct_data, 'results': 3}
        self.assertEqual(expct, result)

    def testGridbasic_nofields(self):
        """Get a query from a GridModel without fields
        """
        qry = Author.objects.all()
        import datetime
        expct_data = [
            (1, u"toto", u"ToTo", datetime.date(2000, 1, 2)),
            (2, u"tata", u"TaTa", datetime.date(2001, 2, 3)),
            (3, u"tutu", u"TuTu", datetime.date(2002, 3, 4)),
        ]
        ag = AuthorGrid_nofields()
        raw_result, length = ag.get_rows(qry,)
        self.assertEqual(expct_data, raw_result)
        self.assertEqual(length, 3)

    def testGridstore(self):
        """Get Store config from a grid
        """
        #expct = {'store': store,
        columns = [
            {'header': 'name', 'name': 'name', 'tooltip': u'name'},
            {'header': 'title', 'name': 'title', 'tooltip': u'title'},
            {'name': 'birth_date', 'dateFormat': 'Y-m-d', 'format': 'Y-m-d', 'tooltip': u'birth date', 'header': 'birth_date', 'type': 'date','xtype': 'datecolumn'}
        ]
        ag = AuthorGrid()
        store = ag.to_store()
        expct = {'fields': columns}
        self.assertEqual(expct, store)
        store = ag.to_store(url="/test/blah")
        expct = {'fields': columns, 'url': '/test/blah'}
        self.assertEqual(expct, store)


    def testGridconfig(self):
        """ expct = {
                    stripeRows: true,
                    autoExpandColumn: 'company',
                    height: 350,
                    width: 600,
                    title: 'Array Grid',
                    // config options for stateful behavior
                    stateful: true,
                    stateId: 'grid'        
        }"""
        pass
        #jsonresult = ag.get_rows(qry)
        #result = simplejson.loads(jsonresult)
        #self.assertEqual(expct, result)

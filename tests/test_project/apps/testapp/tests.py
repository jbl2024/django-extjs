from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import simplejson
from django.conf import settings

from test_project.apps.testapp.forms import ContactForm, AuthorForm, AuthorxcludeForm, WhatamessForm
from test_project.apps.testapp.models import Author, Whatamess
from test_project.apps.testapp.models import AuthorGrid


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

    def testGridbasic(self):
        qry = Author.objects.all()
        expct = {u"success": True, u"data": [
            {u"birth_date": u"2000-01-02", u"name": u"toto", u"title": u"ToTo"},
            {u"birth_date": u"2001-02-03", u"name": u"tata", u"title": u"TaTa"},
            {u"birth_date": u"2002-03-04", u"name": u"tutu", u"title": u"TuTu"},
        ]}
        ag = AuthorGrid()
        jsonresult = ag.get_rows(qry)
        result = simplejson.loads(jsonresult)
        self.assertEqual(expct, result)


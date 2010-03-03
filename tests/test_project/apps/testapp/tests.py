from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import simplejson
from django.conf import settings

from test_project.apps.testapp.forms import ContactForm, AuthorForm, AuthorxcludeForm, WhatamessForm

class SimpleTestCase(TestCase):
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
            {"xtype": "combo", "fieldLabel": "title", "name": "title", "header": "title", "fieldHidden": False, "value": "", "width": 150, "allowBlank": True, "helpText": "", "mode": "local", "store": [["", "---------"], ["MR", "Mr."], ["MRS", "Mrs."], ["MS", "Ms."]], "listWidth": "auto"},
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
            {"xtype": "combo", "fieldLabel": "author", "name": "author", "header": "author", "fieldHidden": False, "value": "", "width": 150, "allowBlank": True, "helpText": "", "mode": "local", "store": [["", "---------"]], "listWidth": "auto"},
            {"xtype": "combo", "fieldLabel": "title", "name": "title", "header": "title", "fieldHidden": False, "value": "", "width": 150, "allowBlank": True, "helpText": "", "mode": "local", "store": [["", "---------"], ["1", "Mr."], ["2", "Mrs."], ["3", "Ms."]], "listWidth": "auto"},
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

    def testModelFormcomplex(self):
        cf = WhatamessForm()
        expct = {"items":[
            {"fieldLabel": "name", "xtype": "textfield", "fieldHidden": False, "header": "name", "allowBlank": True, "helpText": "", "maxLength": 100, "name": "name"},
            {"fieldLabel": "number", "allowBlank": True, "fieldHidden": False, "name": "number", "header": "number", "helpText": "", "xtype": "numberfield"},
            {"fieldLabel": "slug", "xtype": "textfield", "fieldHidden": False, "header": "slug", "allowBlank": True, "helpText": "", "maxLength": 50, "name": "slug"},
            {"fieldLabel": "text", "allowBlank": True, "fieldHidden": False, "name": "text", "header": "text", "helpText": "", "xtype": "textfield"},
            {"xtype": "combo", "fieldLabel": "author", "name": "author", "header": "author", "fieldHidden": False, "value": "", "width": 150, "allowBlank": True, "helpText": "", "mode": "local", "store": [["", "---------"]], "listWidth": "auto"},
            {"xtype": "combo", "fieldLabel": "title", "name": "title", "header": "title", "fieldHidden": False, "value": "", "width": 150, "allowBlank": True, "helpText": "", "mode": "local", "store": [["", "---------"], ["1", "Mr."], ["2", "Mrs."], ["3", "Ms."]], "listWidth": "auto"},
            {"fieldLabel": "birth_date", "allowBlank": False, "fieldHidden": False, "name": "birth_date", "header": "birth_date", "helpText": "", "xtype": "datefield"}, {"fieldLabel": "yesno", "xtype": "checkbox", "fieldHidden": False, "value": False, "header": "yesno", "allowBlank": False, "helpText": "", "name": "yesno"}
            ]}
        self.assertEqual(expct, simplejson.loads(cf.as_extjs()))

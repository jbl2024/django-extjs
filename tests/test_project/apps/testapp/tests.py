from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import simplejson
from django.conf import settings

from test_project.apps.testapp.forms import ContactForm, AuthorForm

class SimpleTestCase(TestCase):
    def testFormbasic(self):
        cf = ContactForm()
        from extjs.utils import ExtJSONEncoder
        expct = {"items":[
            {'fieldLabel': 'subject', 'xtype': 'textfield', 'fieldHidden': False, 'name': 'subject', 'header': 'subject', 'helpText': '', 'maxLength': 100, 'allowBlank': True},
            {'fieldLabel': 'message', 'xtype': 'textfield', 'fieldHidden': False, 'value': 'pony', 'name': 'message', 'header': 'message', 'helpText': '', 'allowBlank': True},
            {'vtype': 'email', 'fieldLabel': 'sender', 'allowBlank': True, 'fieldHidden': False, 'name': 'sender', 'header': 'sender', 'helpText': '', 'xtype': 'textfield'},
            {'fieldLabel': 'cc_myself', 'xtype': 'checkbox', 'fieldHidden': False, 'value': False, 'name': 'cc_myself', 'header': 'cc_myself', 'helpText': '', 'allowBlank': False},
        ]}
        self.assertEqual(expct, simplejson.loads(cf.as_extjs()))

    def testModelFormbasic(self):
        cf = AuthorForm()
        expct = {"items":[
            {"fieldLabel": "name", "xtype": "textfield", "fieldHidden": False, "header": "name", "allowBlank": True, "helpText": "", "maxLength": 100, "name": "name"},
            {"xtype": "combo", "fieldLabel": "title", "name": "title", "header": "title", "fieldHidden": False, "value": "", "width": 150, "allowBlank": True, "helpText": "", "mode": "local", "store": [["", "---------"], ["MR", "Mr."], ["MRS", "Mrs."], ["MS", "Ms."]], "listWidth": "auto"},
            {"fieldLabel": "birth_date", "allowBlank": False, "fieldHidden": False, "name": "birth_date", "header": "birth_date", "helpText": "", "xtype": "datefield"}
            ]}
        self.assertEqual(expct, simplejson.loads(cf.as_extjs()))

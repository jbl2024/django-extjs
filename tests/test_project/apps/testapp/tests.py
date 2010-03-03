from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import simplejson
from django.conf import settings

from test_project.apps.testapp.forms import ContactForm, AuthorForm

class SimpleTestCase(TestCase):
    def testFormbasic(self):
        cf = ContactForm()
        expct = {"items":[
            {u'fieldLabel': u'subject', u'xtype': u'textfield', u'required': True, u'value': u'', u'name': u'subject', u'maxLength': 100, u'allowBlank': False},
            {u'fieldLabel': u'message', u'name': u'message', u'required': True, u'value': u'pony', u'allowBlank': False, u'xtype': u'textfield'},
            {u'vtype': u'email', u'fieldLabel': u'sender', u'allowBlank': False, u'required': True, u'value': u'', u'name': u'sender', u'xtype': u'textfield'},
            {u'fieldLabel': u'cc_myself', u'name': u'cc_myself', u'required': False, u'value': u'', u'allowBlank': True, u'xtype': u'checkbox'},
        ]}
        self.assertEqual(expct, simplejson.loads(cf.as_extjs()))

    def testModelFormbasic(self):
        cf = AuthorForm()
        expct = u'{"items":['
        expct += u'{"fieldLabel":"Name","xtype":"textfield","required":true,"value":"","allowBlank":false,"maxLength":100,"name":"name"},'
        expct += u'{"displayField":"display","forceSelection":true,"fieldLabel":"Title","xtype":"combo","required":true,"editable":true,"value":"","hiddenName":"title","typeAhead":true,"allowBlank":false,"blankText":"title :","valueField":"id","mode":"local","triggerAction":"all","store":new Ext.data.SimpleStore({fields: [\'id\',\'display\'],  data : [["","---------"],["MR","Mr."],["MRS","Mrs."],["MS","Ms."]] }),"name":"title"},'
        expct += u'{"fieldLabel":"Birth date","xtype":"datefield","format":"Y-m-d","required":false,"value":"","allowBlank":true,"name":"birth_date"}'
        expct += u']}'
        self.assertEqual(expct, cf.as_extjs())

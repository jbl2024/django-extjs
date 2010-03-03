from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import simplejson
from django.conf import settings

from test_project.apps.testapp.forms import ContactForm, AuthorForm

class SimpleTestCase(TestCase):
    def testFormbasic(self):
        cf = ContactForm()
        expct = {"items":[
            {"allowBlank":False,"fieldLabel":"subject","xtype":"textfield","maxLength":100,"value":"","name":"subject"},
            {"allowBlank":False,"fieldLabel":"message","xtype":"textfield","value":"pony","name":"message"},
            {"vtype":"email","fieldLabel":"sender","xtype":"textfield","allowBlank":False,"value":"","name":"sender"},
            {"allowBlank":True,"checked":"","xtype":"checkbox","fieldLabel":"cc_myself","value":"","name":"cc_myself"}
        ]}
        self.assertEqual(expct, simplejson.loads(cf.as_extjs()))

    def testModelFormbasic(self):
        cf = AuthorForm()
        expct = u'{"items":['
        expct += u'{"allowBlank":false,"fieldLabel":"Name","xtype":"textfield","maxLength":100,"value":"","name":"name"},'
        expct += u'{"displayField":"display","forceSelection":true,"fieldLabel":"Title","xtype":"combo","name":"title","editable":false,"blankText":"title :","hiddenName":"title","valueField":"id","allowBlank":false,"value":"","triggerAction":"all","store":new Ext.data.SimpleStore({fields: [\'id\',\'display\'],  data : [["","---------"],["MR","Mr."],["MRS","Mrs."],["MS","Ms."]] }),"mode":"local"},'
        expct += u'{"allowBlank":true,"fieldLabel":"Birth date","xtype":"datefield","format":"Y-m-d","value":"","name":"birth_date"}'
        expct += u']}'
        self.assertEqual(expct, cf.as_extjs())

#-*- coding: utf-8 -*-
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import simplejson
from django.conf import settings
from django.http import HttpRequest, QueryDict

from test_project.apps.testapp.forms import ContactForm, AuthorForm, AuthorxcludeForm, WhatamessForm, WhatamessFormFK, I18nForm
from test_project.apps.testapp.models import Author, AuthorProxy, Whatamess
from test_project.apps.testapp.models import AuthorGrid, AuthorGrid_nofields, AuthorGridProxy, WhatamessGrid
from extjs.utils import query_from_request

class FormsTestCase(TestCase):
    def testFormbasic(self):
        """Test a simple Form
        """
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
        """Test a ModelForm
        """
        cf = AuthorForm()
        expct = {"items":[
            {"fieldLabel": "Name", "xtype": "textfield", "fieldHidden": False, "header": "name", "allowBlank": True, "helpText": "", "maxLength": 100, "name": "name", "value": "Platon"},
            {"xtype": "combo", "forceSelection": True, "editable": False, "triggerAction": 'all', "hiddenName": "title", "fieldLabel": "Title", "name": "title", "header": "title", "fieldHidden": False, "value": "", "width": 150, "allowBlank": True, "helpText": "", "mode": "local", "store": [["", "---------"], ["MR", "Mr."], ["MRS", "Mrs."], ["MS", "Ms."]], "listWidth": "auto"},
            {"fieldLabel": "Birth date", "allowBlank": False, "fieldHidden": False, "name": "birth_date", "header": "birth_date", "helpText": "", "xtype": "datefield"}
            ]}
        self.assertEqual(expct, simplejson.loads(cf.as_extjs()))

        # With POST data
        cf = AuthorForm({"name":"PONNY"})
        expct["items"][0]["value"] = "PONNY"
        self.assertEqual(expct, simplejson.loads(cf.as_extjs()))

        # With an instance
        from datetime import date
        auth1 = Author.objects.create(name="toto", title="MR")
        expct["items"][0]["value"] = "toto"
        expct["items"][1]["value"] = "MR"
        cf = AuthorForm(instance=auth1)
        self.assertEqual(expct, simplejson.loads(cf.as_extjs()))

    def testModelFormcomplex(self):
        """Test a ModelForm with lot of fields
        """
        cf = WhatamessForm()
        expct = {"items":[
            {"fieldLabel": "Name", "xtype": "textfield", "fieldHidden": False, "header": "name", "allowBlank": True, "helpText": "", "maxLength": 100, "name": "name"},
            {"fieldLabel": "Number", "allowBlank": True, "fieldHidden": False, "name": "number", "header": "number", "helpText": "", "xtype": "numberfield"},
            {"fieldLabel": "Slug", "xtype": "textfield", "fieldHidden": False, "header": "slug", "allowBlank": True, "helpText": "", "maxLength": 50, "name": "slug"},
            {"fieldLabel": "Text", "allowBlank": True, "fieldHidden": False, "name": "text", "header": "text", "helpText": "", "xtype": "textfield"},
            {"xtype": "combo", "forceSelection": True, "editable": False, "triggerAction": 'all', "hiddenName": "author", "fieldLabel": "Author", "name": "author", "header": "author", "fieldHidden": False, "value": "", "width": 150, "allowBlank": True, "helpText": "", "mode": "local", "store": [["", "---------"]], "listWidth": "auto"},
            {"xtype": "combo", "forceSelection": True, "editable": False, "triggerAction": 'all', "hiddenName": "title", "fieldLabel": "Title", "name": "title", "header": "title", "fieldHidden": False, "value": "", "width": 150, "allowBlank": True, "helpText": "", "mode": "local", "store": [["", "---------"], ["1", "Mr."], ["2", "Mrs."], ["3", "Ms."]], "listWidth": "auto"},
            {"fieldLabel": "Birth date", "allowBlank": False, "fieldHidden": False, "name": "birth_date", "header": "birth_date", "helpText": "", "xtype": "datefield"},
            {"fieldLabel": "Yesno", "xtype": "checkbox", "fieldHidden": False, "value": False, "header": "yesno", "allowBlank": False, "helpText": "", "name": "yesno"}
            ]}
        self.assertEqual(expct, simplejson.loads(cf.as_extjs()))

    def testModelFormcomplexFK(self):
        """Test a ModelForm with only one field
        """
        cf = WhatamessFormFK()
        expct = {"items":[
            {"xtype": "combo", "forceSelection": True, "editable": False, "triggerAction": 'all', "hiddenName": "author", "fieldLabel": "Author", "name": "author", "header": "author", "fieldHidden": False, "value": "", "width": 150, "allowBlank": True, "helpText": "", "mode": "local", "store": [["", "---------"]], "listWidth": "auto"},
            ]}
        self.assertEqual(expct, simplejson.loads(cf.as_extjs()))

    def testModelFormexcludebasic(self):
        """Test a ModelForm with lot of fields and excludes
        """
        cf = AuthorxcludeForm()
        expct = {"items":[
            {"fieldLabel": "Name", "xtype": "textfield", "fieldHidden": False, "header": "name", "allowBlank": True, "helpText": "", "maxLength": 100, "name": "name", "value": "Platon"},
            {"fieldLabel": "Birth date", "allowBlank": False, "fieldHidden": False, "name": "birth_date", "header": "birth_date", "helpText": "", "xtype": "datefield"}
            ]}
        self.assertEqual(expct, simplejson.loads(cf.as_extjs()))

    def testModelFormComplexwithAuthor(self):
        """Test a ModelForm with lot of fields and an Author
        """
        from datetime import date
        auth1 = Author.objects.create(name="toto", title="ToTo", birth_date=date(2000,1,2))
        cf = WhatamessForm()
        expct = {"items":[
            {"fieldLabel": "Name", "xtype": "textfield", "fieldHidden": False, "header": "name", "allowBlank": True, "helpText": "", "maxLength": 100, "name": "name"},
            {"fieldLabel": "Number", "allowBlank": True, "fieldHidden": False, "name": "number", "header": "number", "helpText": "", "xtype": "numberfield"},
            {"fieldLabel": "Slug", "xtype": "textfield", "fieldHidden": False, "header": "slug", "allowBlank": True, "helpText": "", "maxLength": 50, "name": "slug"},
            {"fieldLabel": "Text", "allowBlank": True, "fieldHidden": False, "name": "text", "header": "text", "helpText": "", "xtype": "textfield"},
            {"xtype": "combo", "forceSelection": True, "editable": False, "triggerAction": 'all', "hiddenName": "author", "fieldLabel": "Author", "name": "author", "header": "author", "fieldHidden": False, "value": "", "width": 150, "allowBlank": True, "helpText": "", "mode": "local", "store": [["", "---------"], ['1', 'toto'],], "listWidth": "auto"},
            {"xtype": "combo", "forceSelection": True, "editable": False, "triggerAction": 'all', "hiddenName": "title", "fieldLabel": "Title", "name": "title", "header": "title", "fieldHidden": False, "value": "", "width": 150, "allowBlank": True, "helpText": "", "mode": "local", "store": [["", "---------"], ["1", "Mr."], ["2", "Mrs."], ["3", "Ms."]], "listWidth": "auto"},
            {"fieldLabel": "Birth date", "allowBlank": False, "fieldHidden": False, "name": "birth_date", "header": "birth_date", "helpText": "", "xtype": "datefield"},
            {"fieldLabel": "Yesno", "xtype": "checkbox", "fieldHidden": False, "value": False, "header": "yesno", "allowBlank": False, "helpText": "", "name": "yesno"}
            ]}
        self.assertEqual(expct, simplejson.loads(cf.as_extjs()))

    def testFormI18N(self):
        """Test a I18N Form
        """
        cf = I18nForm()
        expct = {"items":[
            {'fieldLabel': 'Subject', 'xtype': 'textfield', 'fieldHidden': False, 'name': 'subject', 'header': 'subject', 'helpText': '', 'maxLength': 100, 'allowBlank': True},
        ]}
        self.assertEqual(expct, simplejson.loads(cf.as_extjs()))

class FormsDataTestCase(TestCase):
    """Tests to have form data
    """
    def testFormbasic(self):
        """Test a simple Form datas
        """
        # With error
        cf = ContactForm({'subject':'PONY', 'message': 'test', 'cc_myself': False})
        expct = {u'errors': {u'sender': [u'This field is required.']}, u'success': False}
        self.assertEqual(expct, simplejson.loads(cf.as_extjsdata()))
        # Without error
        expct_data = {
            'subject': 'PONY',
            'message': 'test',
            'sender': 'pony@wonder.land',
            'cc_myself': False,
        }
        cf = ContactForm({'subject':'PONY', 'message': 'test', 'sender': 'pony@wonder.land', 'cc_myself': False})
        expct = {u"success": True, u"data": expct_data}
        self.assertEqual(expct, simplejson.loads(cf.as_extjsdata()))

    def testModelFormbasic(self):
        """Test a ModelForm
        """
        # With an instance
        auth1 = Author.objects.create(name="toto", title="MR")
        cf = AuthorForm(instance=auth1)
        expct_data = {
            u"name" : u'toto',
            u"title" : u"MR",
            u"birth_date" : None,
            }
        expct = {u"success": True, u"data": expct_data}
        self.assertEqual(expct, simplejson.loads(cf.as_extjsdata()))

    def testFormComplex(self):
        """Test a simple Form datas
        """
        # Without error
        from datetime import date
        auth1 = Author.objects.create(name="toto", title="ToTo", birth_date=date(2000,1,2))
        data = {
            'name':'PONY',
            'number': 1,
            'slug': 'slug',
            'text': 'test',
            'author' : 1,
            'title': 1,
            'yesno':True
        }
        cf = WhatamessForm(data)
        expct_data = {
            'name':'PONY',
            'number': 1,
            'slug': 'slug',
            'text': 'test',
            'author': "toto",
            'title': 1,
            'yesno': True,
            'birth_date': None
        }
        expct_data["author"] = "toto"
        expct = {u"success": True, u"data": expct_data}
        self.assertEqual(expct, simplejson.loads(cf.as_extjsdata()))

class GridTestCase(TestCase):
    def setUp(self):
        """
        """
        from datetime import date
        self.auth1 = Author.objects.create(name="toto", title="ToTo", birth_date=date(2000,1,2))
        self.auth2 = Author.objects.create(name="tata", title="TaTa", birth_date=date(2001,2,3))
        self.auth3 = Author.objects.create(name="tutu", title="TuTu", birth_date=date(2002,3,4))
        self.wam1 = Whatamess.objects.create(name="dodo", title=1, number=1, text="d o d o", author=self.auth1, yesno=True, birth_date=date(2000,1,2))
        self.wam2 = Whatamess.objects.create(name="dada", title=1, number=2, text="d a d a", author=self.auth2, yesno=True, birth_date=date(2001,2,3))
        self.wam3 = Whatamess.objects.create(name="dudu", title=1, number=3, text="d u d u", author=self.auth3, yesno=True, birth_date=date(2002,3,4))

    def testGridbasic(self):
        """Get a query from a GridModel
        """
        qry = Author.objects.all()
        import datetime
        expct_data = [
            {'his_name': u"toto", 'title': u"ToTo", 'birth_date': datetime.date(2000, 1, 2)},
            {'his_name': u"tata", 'title': u"TaTa", 'birth_date': datetime.date(2001, 2, 3)},
            {'his_name': u"tutu", 'title': u"TuTu", 'birth_date': datetime.date(2002, 3, 4)},
        ]
        ag = AuthorGrid()
        raw_result, length = ag.get_rows(qry,)
        self.assertEqual(expct_data, raw_result)
        self.assertEqual(length, 3)

        # And now get result in JSONResponse
        expct_data = [
            {'title': u"ToTo", 'birth_date': u"2000-01-02", 'his_name': u"toto"},
            {'title': u"TaTa", 'birth_date': u"2001-02-03", 'his_name': u"tata"},
            {'title': u"TuTu", 'birth_date': u"2002-03-04", 'his_name': u"tutu"},
        ]
        expct = {u"success": True, u"data": expct_data, u'results': 3}
        jsonresult = ag.get_rows_json(qry, fields=['title', 'birth_date', 'his_name'])
        result = simplejson.loads(jsonresult)
        self.assertEqual(expct, result)

        # use pre-configured View
        response = self.client.get("/api/author/getjson")
        result = simplejson.loads(response.content)
        expct_data = [
            {'his_name': "toto", 'title': "ToTo", 'birth_date': "2000-01-02"},
            {'his_name': "tata", 'title': "TaTa", 'birth_date': "2001-02-03"},
            {'his_name': "tutu", 'title': "TuTu", 'birth_date': "2002-03-04"},
        ]
        expct = {"success": True, "data": expct_data, 'results': 3}
        self.assertEqual(expct, result)

    def testGridbasic_nofields(self):
        """Get a query from a GridModel without fields
        """
        qry = Author.objects.all()
        import datetime
        expct_data = [
            {"id": 1, 'name': u"toto", 'title': u"ToTo", 'birth_date': datetime.date(2000, 1, 2)},
            {"id": 2, 'name': u"tata", 'title': u"TaTa", 'birth_date': datetime.date(2001, 2, 3)},
            {"id": 3, 'name': u"tutu", 'title': u"TuTu", 'birth_date': datetime.date(2002, 3, 4)},
        ]
        ag = AuthorGrid_nofields()
        raw_result, length = ag.get_rows(qry,)
        self.assertEqual(expct_data, raw_result)
        self.assertEqual(length, 3)

    def testGridbasic_utf8(self):
        """Get a query from a GridModel with utf8
        """
        # adds utf8 record
        from datetime import date
        self.auth4 = Author.objects.create(name="tété", title="TéTé", birth_date=date(2000,1,2))
        qry = Author.objects.all()

        # And now get result in JSONResponse
        expct_data = [
            {'title': u"ToTo", 'birth_date': u"2000-01-02", 'his_name': u"toto"},
            {'title': u"TaTa", 'birth_date': u"2001-02-03", 'his_name': u"tata"},
            {'title': u"TuTu", 'birth_date': u"2002-03-04", 'his_name': u"tutu"},
            {'title': u"TéTé", 'birth_date': u"2000-01-02", 'his_name': u"tété"},
        ]
        ag = AuthorGrid()
        expct = {u"success": True, u"data": expct_data, u'results': 4}
        jsonresult = ag.get_rows_json(qry, fields=['title', 'birth_date', 'his_name'])
        result = simplejson.loads(jsonresult)
        self.assertEqual(expct, result)

    def testGridstore(self):
        """Get Store config from a grid
        """
        #expct = {'store': store,
        columns = [
            {'header': 'name', 'name': 'name', 'tooltip': u'Name'},
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

    def testGridProxy(self):
        """Get a query from a GridModel with proxy and customs methods
        """
        qry = AuthorProxy.objects.all()
        import datetime
        expct_data = [
            {'id': 1, 'name': u"toto", 'title': u"ToTo", 'birth_date': datetime.date(2000, 1, 2)},
            {'id': 2, 'name': u"tata", 'title': u"TaTa", 'birth_date': datetime.date(2001, 2, 3)},
            {'id': 3, 'name': u"tutu", 'title': u"TuTu", 'birth_date': datetime.date(2002, 3, 4)},
        ]
        ag = AuthorGridProxy()
        raw_result, length = ag.get_rows(qry,)
        self.assertEqual(expct_data, raw_result)
        self.assertEqual(length, 3)

        # Use method
        expct_data = [
            {'name': u"toto", 'title': u"ToTo", 'birth_date': datetime.date(2000, 1, 2), "aprint" : "Proxy here : toto"},
            {'name': u"tata", 'title': u"TaTa", 'birth_date': datetime.date(2001, 2, 3), "aprint" : "Proxy here : tata"},
            {'name': u"tutu", 'title': u"TuTu", 'birth_date': datetime.date(2002, 3, 4), "aprint" : "Proxy here : tutu"},
        ]
        ag = AuthorGridProxy()
        raw_result, length = ag.get_rows(qry, fields=['name', 'title', 'birth_date', 'aprint'])
        self.assertEqual(expct_data, raw_result)
        self.assertEqual(length, 3)

    def testGridComplex(self):
        """test FK resolutions in ExtJSONEncoder
        """
        qry = Whatamess.objects.all()
        import datetime
        # Use method
        expct_data = [
            {u'name': u"dodo", u'author': u'toto'},
            {u'name': u"dada", u'author': u'tata'},
            {u'name': u"dudu", u'author': u'tutu'},
        ]
        wg = WhatamessGrid()
        expct = {u"success": True, u"data": expct_data, u'results': 3}
        jsonresult = wg.get_rows_json(qry, fields=['name', 'author'])
        result = simplejson.loads(jsonresult)
        self.assertEqual(expct, result)

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

    def testGridError(self):
        """Get a error with a query from a GridModel
        """
        qry = Author.objects.all()
        ag = AuthorGrid()
        # And now get result in JSONResponse
        expct_data = [
            {'title': u"ToTo", 'birth_date': u"2000-01-02", 'name': u"toto"},
            {'title': u"TaTa", 'birth_date': u"2001-02-03", 'name': u"tata"},
            {'title': u"TuTu", 'birth_date': u"2002-03-04", 'name': u"tutu"},
        ]
        expct = {u"success": False, u"message": "Error : No mapped field 'titl'"}
        jsonresult = ag.get_rows_json(qry, fields=['titl', 'birth_date', 'name'])
        result = simplejson.loads(jsonresult)
        self.assertEqual(expct, result)
        # Without jsonerror we get normal Django's exception
        self.assertRaises(AttributeError, ag.get_rows_json, qry, fields=['titl', 'birth_date', 'name'], jsonerror=False)

class QueryFromRequestTest(TestCase):
    """Test fonction query From request
    """
    def setUp(self):
        """
        """
        self.auth0 = Author.objects.create(name="to", title="MR")
        self.auth1 = Author.objects.create(name="tata", title="MR")
        self.auth2 = Author.objects.create(name="tototo", title="MR")
        self.auth3 = Author.objects.create(name="totototo", title="MR")
        self.auth4 = Author.objects.create(name="dototototo", title="MR")
        self.request = HttpRequest()

    def test_query_filter(self):
        """Test simples args
        """
        self.request = HttpRequest()
        qr = Author.objects.all()
        qrd = QueryDict('start=0&dir=ASC&name=tata')
        self.request.REQUEST = qrd
        fields = {"name": "name", "desc": "description", "id": "id"}
        result_qr = query_from_request(self.request, qr, fields=fields)
        self.assertEqual(list(result_qr), [self.auth1])

    def test_query_limit(self):
        """Test limit args
        """
        # test limit
        self.request = HttpRequest()
        qr = Author.objects.all()
        qrd = QueryDict('sort=id&dir=ASC&limit=2')
        self.request.REQUEST = qrd
        fields = {"name": "name", "desc": "description", "id": "id"}
        result_qr = query_from_request(self.request, qr, fields=fields)
        self.assertEqual(result_qr.count(), 2)

        # test start only
        qrd = QueryDict('start=2&sort=id&dir=ASC')
        self.request.REQUEST = qrd
        result_qr = query_from_request(self.request, qr, fields=fields)
        self.assertTrue(self.auth1 not in result_qr)
        self.assertEqual(result_qr.count(), 3)

        # test start & limit
        qrd = QueryDict('start=2&sort=id&dir=ASC&limit=2')
        self.request.REQUEST = qrd
        result_qr = query_from_request(self.request, qr, fields=fields)
        self.assertTrue(self.auth1 not in result_qr)
        self.assertEqual(result_qr.count(), 2)

        # test exception
        qrd = QueryDict('start=2&sort=id&dir=ASC&limit=abc')
        self.request.REQUEST = qrd
        result_qr = query_from_request(self.request, qr, fields=fields)
        self.assertEqual(result_qr.count(), 0)

        # test high limit
        qrd = QueryDict('start=4&sort=id&dir=ASC&limit=20')
        self.request.REQUEST = qrd
        result_qr = query_from_request(self.request, qr, fields=fields)
        self.assertEqual(result_qr.count(), 1)

        # test high start
        qrd = QueryDict('start=24&sort=id&dir=ASC&limit=20')
        self.request.REQUEST = qrd
        result_qr = query_from_request(self.request, qr, fields=fields)
        self.assertEqual(result_qr.count(), 0)

    def test_query_filter_unknowsort(self):
        """Test unknowsort arg
        """
        qr = Author.objects.all()
        qrd = QueryDict('start=0&sort=id&dir=ASC&group_id=1&name=test')
        self.request.REQUEST = qrd
        fields = {"name": "name", "desc": "description"}
        self.assertRaises(IndexError, query_from_request, self.request, qr, fields=fields)

    def test_query_order(self):
        """Test order
        """
        self.request = HttpRequest()
        qr = Author.objects.all()
        qrd = QueryDict('sort=dame&dir=ASC')
        self.request.REQUEST = qrd
        fields = {"dame": "name", "desc": "description", "pk": "id"}
        result_qr = query_from_request(self.request, qr, fields=fields)
        self.assertEqual(result_qr.count(), 5)
        self.assertEqual(result_qr[0], self.auth4)

    def test_query_order_reverse(self):
        """Test order DESC
        """
        self.request = HttpRequest()
        qr = Author.objects.all()
        qrd = QueryDict('sort=dame&dir=DESC')
        self.request.REQUEST = qrd
        fields = {"dame": "name", "desc": "description", "pk": "id"}
        result_qr = query_from_request(self.request, qr, fields=fields)
        self.assertEqual(result_qr.count(), 5)
        self.assertEqual(result_qr[4], self.auth4)

    def test_query_filter_on_model(self):
        """Test simples args
        """
        self.request = HttpRequest()
        qr = Author.objects.all()
        qrd = QueryDict('start=0&dir=ASC&his_name=tata')
        self.request.REQUEST = qrd
        ag = AuthorGrid()
        result_qr = ag.query_from_request(self.request, qr)
        self.assertEqual(list(result_qr), [self.auth1])

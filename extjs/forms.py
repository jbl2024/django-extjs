from django import forms

CHAR_PIXEL_WIDTH = 8
CHAR_PIXEL_HEIGHT = 15

import utils
import simplejson


class ExtJsForm(object):
    """
        .add a as_extjs method to forms.Form or forms.ModelForm; this method returns a formpanel json config, with all fields, buttons and logic
        .add a as_extjsfields method that returns only the field list. useful if you want to customise the form layout
        .add a html_errorlist to return form validations error for an extjs window
    """
    @classmethod
    def register(self, cls):
        cls.as_extjsfields = self.as_extjsfields
        cls.as_extjs = self.as_extjs
        cls.html_errorlist = self.html_errorlist
        # default submit handler
        handler_submit = "function(btn) {console.log(this, btn);this.findParentByType(this.form_xtype).submitForm()}"
        handler_reset = "function(btn) {console.log(this, btn);this.findParentByType(this.form_xtype).resetForm()}"
        cls.ext_baseConfig = {
        }

    @staticmethod
    def as_extjs(self,):
        config = ""
        config_dict = self.ext_baseConfig
        if getattr(self, 'ext_config', None):
            config_dict.update(self.ext_config)
        config_dict['items'] = self
        return simplejson.dumps(config_dict, cls=utils.ExtJSONEncoder)

    @staticmethod
    def html_errorlist(self):
        html = ''
        for field, err in self.errors.items():
            html += '<br><b>%s</b> : %s' % (field, err.as_text())
        return html

    @staticmethod
    def as_extjsfields(self, excludes = []):
        """Return field of Form in list
        """
        raise NotImplemented("Not used for the moment")



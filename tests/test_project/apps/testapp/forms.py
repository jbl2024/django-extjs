from django import forms
import extjs

from models import Author, Whatamess

class ContactForm(forms.Form):
    """ A simple Form"""
    subject = forms.CharField(max_length=100)
    message = forms.CharField(initial="pony")
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)

extjs.register(ContactForm)

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author

extjs.register(AuthorForm)

class WhatamessForm(forms.ModelForm):
    class Meta:
        model = Whatamess

extjs.register(WhatamessForm)

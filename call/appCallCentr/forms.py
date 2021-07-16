from django import forms
from django.utils.translation import ugettext as _


class AddContactForm(forms.Form):
    first_name = forms.CharField(label=_(u'first_name'))
    last_name = forms.CharField(label=_(u'last_name'))
    email = forms.EmailField(label=_(u'email'))
    number_0 = forms.CharField(label=_(u'number'))
    description = forms.CharField(label=_(u'description'))



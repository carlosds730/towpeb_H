__author__ = 'Roly4'
from django import forms

from Shop_Site import models


class RegisterForm(forms.Form):
    name = forms.CharField(max_length=100, required=False)
    email = forms.EmailField(required=True, max_length=100)
    password = forms.CharField(required=True, max_length=100, widget=forms.PasswordInput)
    address = forms.CharField(max_length=100, widget=forms.TextInput, required=False
                              )

    def is_valid(self):
        value = super(RegisterForm, self).is_valid()
        try:
            models.Clients.objects.get(email=self.cleaned_data['email'])
            return False
        except models.Clients.DoesNotExist:
            return value

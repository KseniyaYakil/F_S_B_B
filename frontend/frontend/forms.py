from django import forms
from django.forms import PasswordInput, ValidationError
from django.contrib.auth import authenticate
from django.db import IntegrityError

class LoginForm(forms.Form):
		username = forms.CharField(label='User name', max_length=64)
		password = forms.CharField(label='Password', max_length=64, widget=PasswordInput())

		def clean(self):
				super(LoginForm, self).clean()

				self.username = self.cleaned_data['username']
				self.password = self.cleaned_data['password']



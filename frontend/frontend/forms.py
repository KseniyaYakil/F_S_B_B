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

class PositionCreationForm(forms.Form):
		name = forms.CharField(label='Position name', max_length=64)
		salary = forms.IntegerField(label='Salary', min_value=5000)
		salary_currency = forms.CharField(label='Salary currency')

		def set_values(self, name, salary, salary_currency):
				self.name = name
				self.salary = salary
				self.salary_currency = salary_currency

		def clean(self):
				super(PositionCreationForm, self).clean()

				self.name = self.cleaned_data['name']
				self.salary = self.cleaned_data['salary']
				self.salary_currency = self.cleaned_data['salary_currency']

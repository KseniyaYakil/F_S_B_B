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

		def clean(self):
				super(PositionCreationForm, self).clean()

				self.name = self.cleaned_data['name']
				self.salary = self.cleaned_data['salary']
				self.salary_currency = self.cleaned_data['salary_currency']

class EmployeForm(forms.Form):
		pos_id = forms.IntegerField(label='Position_id', min_value=0)
		user_id = forms.IntegerField(label='User_id', min_value=0)

		def clean(self):
				super(EmployeForm, self).clean()

				self.pos_id = self.cleaned_data['pos_id']
				self.user_id = self.cleaned_data['user_id']

class PosIDForm(forms.Form):
		pos_id = forms.IntegerField(label='Position id', min_value=0)
		pos_get_by_id = 0

		def clean(self):
				print self.data
				if 'pos_get_by_id' in self.data:
						self.pos_get_by_id = 1
				super(PosIDForm, self).clean()

				print self.cleaned_data
				if 'pos_id' in self.cleaned_data:
						print self.cleaned_data['pos_id']
						self.pos_id = self.cleaned_data['pos_id']

class EmpIDForm(forms.Form):
		emp_id = forms.IntegerField(label='Employer id', min_value=0)
		emp_get_by_id = 0

		def clean(self):
				print self.data
				if 'emp_get_by_id' in self.data:
						self.emp_get_by_id = 1
				super(EmpIDForm, self).clean()

				print self.cleaned_data
				if 'emp_id' in self.cleaned_data:
						print self.cleaned_data['emp_id']
						self.emp_id = self.cleaned_data['emp_id']


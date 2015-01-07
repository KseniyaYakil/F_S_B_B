from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from .proto import SessionAgent
from .forms import LoginForm
import urllib3
import json
import re

def home(request):
		return render(request, 'frontend/home.html')

def method(request):
		session_agent = SessionAgent()

		res = session_agent.check_if_authorized(request)
		if res == -1:
				response = HttpResponse()
				response.status_code = 500
				return response

		if res == 0:
				print "INF: redirect to login page"
				return render(request, 'frontend/ask_to_login.html')

		#authorized -> request to backend

		return HttpResponse("some method answer")


@csrf_exempt
def login(request):
		if request.method == 'GET':
				login_form = LoginForm()
				return render(request, 'frontend/login_user.html', {'form' : login_form})

		login_form = LoginForm(request.POST)
		if not login_form.is_valid():
				return render(request, 'frontend/login_user.html', {'form' : login_form})

		print "INF: username {} password {}".format(login_form.username, login_form.password)

		session_agent = SessionAgent()
		session_cookies = session_agent.auth_user(login_form.username, login_form.password)

		response = HttpResponse()
		if session_cookies is None:
				response.status_code = 500
				return response

		response = redirect('method')
		for key, value in session_cookies.items():
				response.set_cookie(key, value)

		return response

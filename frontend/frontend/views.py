from django.http import HttpResponse
from django.shortcuts import render, redirect
from .proto import SessionAgent
import urllib3
import json

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
				return redirect('login')

		#authorized -> request to backend

		return HttpResponse("some method answer")

def login(request):
		#login page
		return HttpResponse("login page")


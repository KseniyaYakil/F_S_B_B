from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from .proto import SessionAgent, PositionAgent
from .forms import LoginForm, PositionCreationForm
import urllib3
import json

def home(request):
		return render(request, 'frontend/home.html')

def check_if_authorised(request):
		session_agent = SessionAgent()
		return session_agent.check_if_authorized(request)

def method(request):
		res = check_if_authorised(request)

		if res == -1:
				response = HttpResponse()
				response.status_code = 500
				return response

		if res == 0:
				print "INF: ask for log in"
				return render(request, 'frontend/ask_to_login.html')

		#authorized -> request to backend

		return HttpResponse("some method answer")

def position_create(request):
		res = check_if_authorised(request)
		if res != 1:
				print "INF: access is not allowed"
				return HttpResponse("Access is denied. Please, authorize")

		if request.method == 'GET':
				creation_form = PositionCreationForm()
				return render(request, 'frontend/position_modify.html', {'form': creation_form})

		creation_form = PositionCreationForm(request.POST)
		if not creation_form.is_valid():
				return render(request, 'frontend/position_modify.html', {'form': creation_form})

		print "INF: creation of position (name={}; salary={}; currency={})".format(creation_form.name,
																				creation_form.salary,
																				creation_form.salary_currency)
		fields = dict()
		fields['name'] = creation_form.name
		fields['salary'] = creation_form.salary
		fields['salary_currency'] = creation_form.salary_currency

		position_agent = PositionAgent()
		json_ans = position_agent.create(fields)

		if json_ans is not None:
				print "INF: status = {}".format(json_ans['status'])

		return redirect('position', pos_id=json_ans['pos_id'])

def position_modify(request, pos_id):
		res = check_if_authorised(request)
		if res != 1:
				print "INF: access is not allowed"
				return HttpResponse("Access is denied. Please, authorize")

		if request.method == 'GET':
				fields = dict()
				fields['pos_id'] = pos_id

				position_agent = PositionAgent()
				pos_data = position_agent.get_position(fields)
				if pos_data is None:
						response = HttpResponse
						response.status_code = 500
						return response

				position = pos_data['positions'].pop()

				modify_form = PositionCreationForm()
				return render(request, 'frontend/position_modify.html', {'form': modify_form, 'set_values': position})

		modify_form = PositionCreationForm(request.POST)
		if not modify_form.is_valid():
				return render(request, 'frontend/position_modify.html', {'form': modify_form})

		print "INF: modify of position (name={}; salary={}; currency={})".format(modify_form.name,
																				modify_form.salary,
																				modify_form.salary_currency)
		fields = dict()
		fields['name'] = modify_form.name
		fields['salary'] = modify_form.salary
		fields['salary_currency'] = modify_form.salary_currency

		position_agent = PositionAgent()
		position_agent.modify_position(pos_id, fields)

		return redirect('position', pos_id)

def position_get_common(request, fields):
		position_agent = PositionAgent()
		pos_data = position_agent.get_position(fields)

		if pos_data is None:
				response = HttpResponse
				response.status_code = 500
				return response

		if pos_data['page'] == 0:
				return render(request, 'frontend/position.html', {'fields': pos_data['positions']})
		else:
				return render(request, 'frontend/position.html', {		'fields': pos_data['positions'],
																		'page': pos_data['page'],
																		'pages_count': pos_data['pages_count']})
def position(request, pos_id):
		res = check_if_authorised(request)
		if res != 1:
				print "INF: access is not allowed"
				return HttpResponse("Access is denied. Please, authorize")

		print "INF: position by id={}".format(pos_id)
		fields = dict()
		fields['pos_id'] = pos_id

		return position_get_common(request, fields)

def position_all(request):
		res = check_if_authorised(request)
		#TODO: if not authorised then show just positions names
		if res != 1:
				print "INF: access is not allowed"
				return HttpResponse("Access is denied. Please, authorize")

		fields = dict()
		fields['page'] = 1

		return position_get_common(request, fields)

def position_delete(request, pos_id):
		res = check_if_authorised(request)
		if res != 1:
				print "INF: access is not allowed"
				return HttpResponse("Access is denied. Please, authorize")

		print "INF: removing position with id={}".format(pos_id)

		position_agent = PositionAgent()
		pos_data = position_agent.delete_position(pos_id)

		if pos_data is None:
				response = HttpResponse
				response.status_code = 500
				return response

		if pos_data['status'] != 'removed':
				print "INF: couldn't remove position with id ={}".format(pos_id)
				return HttpResponse("Position with id = {} was not removed".format(pos_id))

		return HttpResponse("Position with id = {} was succesfully removed".format(pos_id))


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

def logout(request):
		session_agent = SessionAgent()
		res = session_agent.logout_user(request)

		if res == 0:
				print "ERR: couldn't logout user"

		return redirect('home')


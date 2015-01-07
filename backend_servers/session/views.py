from django.shortcuts import render
from django.http.response import HttpResponse, Http404
from .config import SessionConf
from django.http import JsonResponse
from .models import SessionAuth
from uuid import uuid4
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

def generate_cookie():
		return uuid4().hex

def verify_token(request):
		if 'HTTP_COOKIE_TOKEN' and 'HTTP_USER_ID' not in request.META:
				print "ERR: all cookies are not specified"
				return JsonResponse({'status' : 'not valid'}, status=403)

		cookie_token = request.META.get('HTTP_COOKIE_TOKEN')
		cookie_user_id = request.META.get('HTTP_USER_ID')

		if cookie_token is None or cookie_user_id is None:
				print "ERR: all cookies are not specified"
				return JsonResponse({'status' : 'not valid'}, status=403)

		print "DEB: recv cookie_token {} cookie_user_id {}".format(cookie_token, cookie_user_id)

		try:
				session_obj = SessionAuth.objects.get(cookie_token=cookie_token)
		except SessionAuth.DoesNotExist:
				print "INF: requested token does not exist in session.db"
				return JsonResponse({'status': 'not valid'}, status=403)

		if session_obj.is_expired():
				print "INF: cookie is expired"
				return JsonResponse({'status': 'not valid'}, status=401)

		if "{}".format(session_obj.user.pk) != cookie_user_id:
				print "ERR: user_id from req != user_id from db"
				return JsonResponse({'status': 'not valid'}, status=401)

		return JsonResponse({'status': 'valid'}, status=200)

@csrf_exempt
def auth_user(request):
		if 'user_login' not in request.POST or 'user_pass' not in request.POST:
				print "ERR: no fields user_login/user_pass"
				return JsonResponse({'status': 'not valid'}, status=400)

		user_login = request.POST['user_login']
		user_pass = request.POST['user_pass']

		print "INF: check user: `{}' pass: `{}' in db".format(user_login, user_pass)
		try:
				user = User.objects.get(username=user_login, password=user_pass)
		except User.DoesNotExist:
				print "ERR: not such user"
				return JsonResponse({'status': 'not valid'}, status=401)

		session_obj = SessionAuth.objects.create(cookie_token=generate_cookie(), user=user)
		response = JsonResponse({'status': 'valid'}, status=200)
		response.set_cookie(SessionConf.cookie_token_key, session_obj.cookie_token)
		response.set_cookie(SessionConf.cookie_user_key, session_obj.user.pk)

		print "INF: created cookie_token `{}' and cookie_user `{}'".format(session_obj.cookie_token, session_obj.user.pk)
		return response

def home(request):
		return HttpResponse("session home page")


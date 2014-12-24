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
		#check if there is a cookie in requset
		cookie_token = request.META.get('HTTP_COOKIE')
		if cookie_token is None:
				print "No cookie_token!"
				return JsonResponse({'status' : 'not valid'}, status=403)

		cookie_user_id = 1
		print "DEB: recv cookie_token {} cookie_user_id {}".format(cookie_token, cookie_user_id)

		#check cookie in base
		try:
				session_obj = SessionAuth.objects.get(cookie_token=cookie_token)
		except SessionAuth.DoesNotExist:
				print "INF: requested token doesn not exist in session.db"
				return JsonResponse({'status': 'not valid'}, status=403)

		if session_obj.is_expired():
				print "INF: cookie is expired"
				return JsonResponse({'status': 'not valid'}, status=401)

		if session_obj.user.pk != cookie_user_id:
				print "ERR: user_id from req != user_id from db"
				return JsonResponse({'status': 'not valid'}, status=401)

		return JsonResponse({'status': 'valid'}, status=200)

@csrf_exempt
def auth_user(request):
		if 'user_login' not in request.POST or 'user_pass' not in request.POST:
				print "ERR: no fileds user_login/user_pass"
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
		return response

def home(request):
		return HttpResponse("session home page")


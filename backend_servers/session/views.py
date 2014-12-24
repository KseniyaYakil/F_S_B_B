from django.shortcuts import render
from django.http.response import HttpResponse, Http404
from .config import SessionConf
from django.http import JsonResponse

# Create your views here.
def home(request):
		return HttpResponse("session home page")

def verify_token(request):
		cookie_token = request.META.get('HTTP_COOKIE')
		if cookie_token is None:
				print "No cookie_token!"
				return JsonResponse({'status' : 'not valid'}, status=403)

		print cookie_token
		return JsonResponse({'status': 'valid'}, status=200)

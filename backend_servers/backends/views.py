from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Position, Employe

def home(request):
		print "INF: home bachends"
		return JsonResponse(status=200)

@csrf_exempt
def positions(request):
		if request.method == 'POST':
				req = request.POST
				print "INF: position creation (name={}, salary={}, currency={})".format(req['name'],
																						req['salary'],
																						req['salary_currency'])
				pos_obj = Position.objects.create(name=req['name'], salary=req['salary'],
														salary_currency=req['salary_currency'])

				return JsonResponse({'status': 'created', 'pos_id': pos_obj.pk},status=200)

		return JsonResponse(status=200)

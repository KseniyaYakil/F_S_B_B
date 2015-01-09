from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Position, Employe
from django.shortcuts import get_object_or_404
import math
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

POS_PER_PAGE = 3

def home(request):
		print "INF: home bachends"
		return JsonResponse(status=200)

def paginate(request, objects, objects_per_page):
    paginator = Paginator(objects, objects_per_page)
    page = request.GET.get('page')
    try:
        return paginator.page(page)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return []

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
		elif request.method == 'GET':
				result = dict()

				if 'pos_id' in request.GET:
						pos_id = request.GET.get('pos_id')
						print "INF: position req by id={}".format(pos_id)
						pos_obj = get_object_or_404(Position, pk=pos_id)
						result['positions'] = [{'name': pos_obj.name,
												'salary': pos_obj.salary,
												'salary_currency': pos_obj.salary_currency}]
						result['page'] = 0
						result['pages_count'] = 0
				else:
						pos_objects = Position.objects.all()
						result['page'] = request.GET['page']
						result['pages_count'] = math.ceil(pos_objects.count() / POS_PER_PAGE)

						pos_paginated = paginate(request, pos_objects, POS_PER_PAGE)
						result['positions'] = [{'name': p.name,
												'salary': p.salary,
												'salary_currency': p.salary_currency} for p in pos_paginated]

				return JsonResponse({	'page': result['page'],
										'pages_count': result['pages_count'],
										'positions': result['positions']}, status=200)

		return JsonResponse(status=200)

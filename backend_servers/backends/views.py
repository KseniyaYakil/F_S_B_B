from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Position, Employe
from django.shortcuts import get_object_or_404
import math
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User

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
def employes(request):
		if request.method == 'POST':
				req = request.POST

				pos_id = int(req['pos_id'])
				user_id = int(req['user_id'])

				#check if already exist
				emp_obj = None
				try:
						emp_obj = Employe.objects.get(position_id=pos_id, user_id=user_id)
				except Employe.DoesNotExist:
						print "INF: employe creation (pos_id = {}, user_id = {})".format(pos_id, user_id)

				if emp_obj is not None:
						print "INF: employe exist (pos_id = {}, user_id = {})".format(pos_id, user_id)
						return JsonResponse({'status': 'exist', 'emp_id': emp_obj.pk}, status=200)

				try:
						emp_obj = Employe.objects.create(position_id=pos_id, user_id=user_id)
				except Employe.ValidationError:
						print "ERR: no position with id = {} or user with is = {}".format(req['pos_id'], req['user_id'])
						return JsonResponse({'status': 'not created'}, status=401)

				return JsonResponse({'status': 'created', 'emp_id': emp_obj.pk}, status=200)

		return JsonResponse({'status': 'nothing'}, status=200)

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

		return JsonResponse({'status': 'nothing'}, status=200)

@csrf_exempt
def position(request, pos_id):
		if request.method == 'DELETE':
				try:
						pos_obj = Position.objects.get(pk=pos_id)
				except Position.DoesNotExist:
						return JsonResponse({'status': 'no such position'}, status=401)

				print "INF: position with id={} was removed".format(pos_id)
				pos_obj.delete()
				return JsonResponse({'status': 'removed'}, status=200)

		elif request.method == 'PUT':
				pos_fields = json.loads(request.body.decode('utf-8'))
				print "INF: modify position ({})".format(pos_fields)

				pos_obj = get_object_or_404(Position, pk=pos_id)
				pos_obj.name = pos_fields['name']
				pos_obj.salary = pos_fields['salary']
				pos_obj.salary_currency = pos_fields['salary_currency']

				pos_obj.save()
				return JsonResponse({'status': 'modified'}, status=200)


		return JsonResponse(status=200)

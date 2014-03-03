# -*- coding: utf-8 -*-

#######################################################
# Страница пользователя
#######################################################

from django.contrib.auth.models import User
from webservice.models import UserAccount, DrawingsInMy
from webservice.forms import AccountForm, AccountFormPlus
from django.core.context_processors import csrf
from django.shortcuts				import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
import json
from django.core.exceptions import ObjectDoesNotExist



def my(request):
	if request.user.is_authenticated() is False:
		return HttpResponseRedirect('/')
	elif request.user.is_authenticated() is True:
		session = request.user
		#table userauth
		user = User.objects.get(username=request.user)
		first_name = user.first_name
		last_name = user.last_name
		#table useraccount
		#useraccount = UserAccount.objects.get(user_id=user.id)
		#date_of_birth = useraccount.date_of_birth
		#growth = useraccount.growth
		#eyes_color = useraccount.eyes_color
		#about = useraccount.about
		#personal_field = useraccount.personal_field
		#education = useraccount.education
		#career = useraccount.career
		#places = useraccount.places
		#c = {'session': session, 'first_name': first_name, 'last_name': last_name, 'date_of_birth': date_of_birth, 'growth': growth,
		#	'eyes_color': eyes_color, 'about': about, 'personal_field': personal_field, 'education': education, 'career': career,
		#	'places': places}
		account_form = AccountForm(auto_id='id_account_%s')
		account_plus_form = AccountFormPlus(auto_id='id_account_%s')
		c = {'session': session, 'first_name': first_name, 'last_name': last_name, 'account_form': account_form, 'account_plus_form': account_plus_form}
		c.update(csrf(request))
		return render_to_response('my.html', c)
	else:
		return HttpResponse('Impossible!')

def ajax_get_label_coords(request):
	if request.user.is_authenticated() is False:
		return HttpResponse('You are NOT authenticated')
	elif request.user.is_authenticated() is True:
		session = request.user
		user = User.objects.get(username=request.user)
		try:
		    drawings_in_my = DrawingsInMy.objects.get(user_id_id=user)
		except ObjectDoesNotExist:
			pass
		response_data = {}
		response_data['x'] = drawings_in_my.main_label_x
		response_data['y'] = drawings_in_my.main_label_y
		return HttpResponse(json.dumps(response_data), mimetype="application/json")

def ajax_set_label_coords(request):
	if request.user.is_authenticated() is False:
		return HttpResponse('You are NOT authenticated')
	elif request.user.is_authenticated() is True:
		session = request.user
		user = User.objects.get(username=request.user)
		try:
		    drawings_in_my = DrawingsInMy.objects.get(user_id_id=user)
		    drawings_in_my.main_label_x = request.POST.get('x','')
		    drawings_in_my.main_label_y = request.POST.get('y','')
		    drawings_in_my.save()
		except ObjectDoesNotExist:
		    main_label_x = request.POST.get('x','')
		    main_label_y = request.POST.get('y','')
		    new_drawings_in_my = DrawingsInMy(user_id=user, main_label_x = main_label_x,
                                              main_label_y = main_label_y)
		    new_drawings_in_my.save()
		return HttpResponse('OK')
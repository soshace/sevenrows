# -*- coding: utf-8 -*-

#######################################################
# brief: Вспомогательные функции авторизации
# author: Denis Nefyodov (denova) 2013
#######################################################

import datetime
import time
import hashlib

from django.core.validators import validate_email, ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.db import IntegrityError
from django.core.mail import send_mail

from webservice.models import UserAccount, ListOfEducation, ListOfCareer, ListOfPlaces, DrawingsInMy

#/////////////////////////// Логин
def ajax_login(request):
	"""(POST)Принимает email, password"""
	if request.method == 'POST':
		email = request.POST.get('email','')
		try:
			validate_email(email)
		except ValidationError:
			return HttpResponse('Email is NOT valid')
		try:
			users = User.objects.get(email=email)
		except ObjectDoesNotExist:
			return HttpResponse('NO such email in db')
		password = request.POST.get('password','')
		user = authenticate(username=users, password=password)
		try:
			login(request,user)
		#точно не знаю какой здесь эксепш, когда пароль не совпадает
		except Exception, e:
			return HttpResponse('Password is incorrect')
		message = "OK"
		return HttpResponse(message)
	else:
		message = "Can't login"
		return HttpResponse(message)

def ajax_logout(request):
	"""(POST) Пустой"""
	logout(request)
	message = "yes"
	return HttpResponse(message)

#/////////////////////////// Регистрация
def ajax_reg(request):
	"""
		(POST) Принимает email
		hash_username = md5(email)
	"""
	if request.method == 'POST':
		email = request.POST.get('email','')
		try:
			validate_email(email)
		except ValidationError:
			return HttpResponse('Email is NOT valid')
		hash_username = hashlib.md5(email).hexdigest()[2:33]
		hash_password = hashlib.md5(hash_username).hexdigest()[0:8]
		reg_email_link = 'http://localhost:8000/?hash=' + hashlib.md5(str(datetime.time())+email).hexdigest()
		# wtf is reg_email_link? maybe to send to email address...
		try:
			user = User.objects.create_user(hash_username, email, hash_password)
			user.set_password(hash_password)
			user.save()
		except IntegrityError:
			return HttpResponse('IntegrityError: maybe this email exists (Duplicate key)?')
		#дпишем запись в таблицу useraccount user_id_id
		#user = User.objects.get(username=hash_username)
		#user_id = user.id
		#ListOfEducationObject = ListOfEducation.objects.get(education="default")
		#ListOfCareerObject = ListOfCareer.objects.get(career="default")
		#ListOfPlacesObject = ListOfPlaces.objects.get(places="default")
		#user_account_entry = UserAccount(user_id_id = user_id, date_of_birth = '1990-11-22', growth = '180', eyes_color = 'default', career=ListOfCareerObject, education=ListOfEducationObject, places=ListOfPlacesObject, about='default', personal_field='default')
		#user_account_entry.save()
		#drawings_in_my_entry = DrawingsInMy(user_id_id = user_id)
		#drawings_in_my_entry.save()
		send_mail('Badaboo1m registration', 'Dear, ' + email + '. You must confirm: '+reg_email_link, 'no_reply@Badaboom.com', ('to',email), fail_silently=True)
		email_message = 'Dear ' + hash_username + ', email was sent to ' + email + ' with password: ' + hash_password + '.'
		message = 'OK'
		user_to_auth = authenticate(username=user, password=hash_password)
		login(request, user_to_auth)
		return HttpResponse(message)
	else:
		message = "nothing"
		return HttpResponse(message)

#/////////////////////////// Просмотр профиля по qr с главной с предложением зарегаться или залогиниться
def ajax_qr(request):
	if request.method == 'POST':
		hash_code = request.POST.get('hash_code','')
		if hash_code is not None and hash_code is not u'' and hash_code is not '' and request.POST.get('hash_code','') is not None:
			try:
				card = Cards.objects.get(hash_code=hash_code)
				#return HttpResponse('card exists')
				card_owner = card.owner_id
				return HttpResponseRedirect('/'+str(card_owner))
			except ObjectDoesNotExist:
				return HttpResponse('card does NOT exist')
		else:
			return HttpResponse('Problem with hash_code')
# -*- coding: utf-8 -*-

#######################################################
# Аккаунтинг
#######################################################

from webservice.forms import AccountForm, AccountFormPlus
from django.core.context_processors import csrf
from django.shortcuts				import render_to_response
from webservice.models import Cards, UserAccount, Friends
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User

#/////////////////////////// отрисовка страницы аккаунт
def account(request):
	if request.user.is_authenticated() is False:
		return HttpResponseRedirect('/')
	elif request.user.is_authenticated() is True:
		account_form = AccountForm(auto_id='id_account_%s')
		account_plus_form = AccountFormPlus(auto_id='id_account_%s')
		session = request.user
		c = {'session': session, 'account_form': account_form, 'account_plus_form': account_plus_form}
		c.update(csrf(request))
		return render_to_response('account.html', c)

#/////////////////////////// изменение имени
def ajax_account_change_all(request):
	if request.user.is_authenticated() is False:
		return HttpResponseRedirect('/')
	elif request.user.is_authenticated() is True:
		user = request.user
		#SECONDARY table webservice_useraccount with exist checking
		try:
			if request.user.useraccount:
				# Do something
				#return HttpResponse('useraccount exists')
				eye_color = request.POST.get('eye_color','')
				if (eye_color is not None and eye_color is not u''):
				    user = User.objects.get(username=user)
				    user_id = user.id
				    UserAccount.objects.filter(user_id=user_id).update(eyes_color=eye_color)
				    #return HttpResponse(eye_color)
				#date_of_birth - лучше сделать выпадающий список, дабы избежать исключений
				date_of_birth = request.POST.get('date_of_birth','')
				if (date_of_birth is not None and date_of_birth is not u''):
				    user = User.objects.get(username=user)
				    user_id = user.id
				    UserAccount.objects.filter(user_id=user_id).update(date_of_birth=date_of_birth)
				    #return HttpResponse(date_of_birth)
				#growth
				growth = request.POST.get('growth','')
				if (growth is not None and growth is not u''):
				    user = User.objects.get(username=user)
				    user_id = user.id
				    UserAccount.objects.filter(user_id=user_id).update(growth=growth)
				    #return HttpResponse(growth)
				#about
				about = request.POST.get('about','')
				if (about is not None and about is not u''):
				    user = User.objects.get(username=user)
				    user_id = user.id
				    UserAccount.objects.filter(user_id=user_id).update(about=about)
				    #return HttpResponse(about)
				#personal_field
				personal_field = request.POST.get('personal_field','')
				if (personal_field is not None and personal_field is not u''):
				    user = User.objects.get(username=user)
				    user_id = user.id
				    UserAccount.objects.filter(user_id=user_id).update(personal_field=personal_field)
				    #return HttpResponse(personal_field)
		except ObjectDoesNotExist:
			#return HttpResponse('useraccount does NOT exist')
			user_object = User.objects.get(username=user)
			new_useraccount = UserAccount.objects.create(user=user_object, eyes_color=request.POST.get('eye_color',''),
                                                         date_of_birth=request.POST.get('date_of_birth',''),
                                                         growth=request.POST.get('growth',''),
                                                         about=request.POST.get('about',''),
                                                         personal_field=request.POST.get('personal_field',''))
		#FIRSTLY table auth_user
		#username есть смысл поставить в конец, т.к. все по нему ищут запись
		username = request.POST.get('username','')
		if (username is not None and username is not u''):
			User.objects.filter(username=user).update(username=username)
			#return HttpResponse(username)
		#first_name
		first_name = request.POST.get('first_name','')
		if (first_name is not None and first_name is not u''):
			User.objects.filter(username=user).update(first_name=first_name)
			#return HttpResponse(first_name)
		#second_name / last_name
		second_name = request.POST.get('second_name','')
		if (second_name is not None and second_name is not u''):
			User.objects.filter(username=user).update(last_name=second_name)
			#return HttpResponse(second_name)
		#eye_color
		return HttpResponse('Ok')
	else:
		return HttpResponse('Huy znaet chto s toboy')

#/////////////////////////// изменение учебы, карьеры, мест
def ajax_account_change_plus(request):
	if request.user.is_authenticated() is False:
		return HttpResponseRedirect('/')
	elif request.user.is_authenticated() is True:
		user = request.user
		#необходимо прицепить регулярки
		#решил сделать одно поле для каждой сущности, при добавлении идет сверка с уэе имеющимися элементами. Если нет такого, то добавляется
		education = request.POST.get('education', '')
		education = education.strip()
		career = request.POST.get('career', '')
		career = career.strip()
		places = request.POST.get('places', '')
		places = places.strip()
		#education
		if education is not u'':
			try:
				educationObjects = ListOfEducation.objects.get(education=education)
			except ObjectDoesNotExist:
				education_entry = ListOfEducation(education=education)
				education_entry.save()
			try:
				educationObjects
			except NameError:
				educationObject= ListOfEducation.objects.get(education=education)
				education_id = educationObject.id
				users = User.objects.get(username=user)
				user_id_id = users.id
				UserAccount.objects.filter(user_id_id=user_id_id).update(education=education_id)
				#return HttpResponse(educationObjects)
		#career
		if career is not u'':
			try:
				careerObjects = ListOfCareer.objects.get(career=career)
			except ObjectDoesNotExist:
				career_entry = ListOfCareer(career=career)
				career_entry.save()
			try:
				careerObjects
			except NameError:
				careerObject = ListOfCareer.objects.get(career=career)
				career_id = careerObject.id
				users = User.objects.get(username=user)
				user_id_id = users.id
				UserAccount.objects.filter(user_id_id=user_id_id).update(career=career_id)
		#places
		if places is not u'':
			try:
				placesObjects = ListOfPlaces.objects.get(places=places)
			except ObjectDoesNotExist:
				places_entry = ListOfPlaces(places=places)
				places_entry.save()
			try:
				placesObjects
			except NameError:
				placesObject = ListOfPlaces.objects.get(places=places)
				places_id = placesObject.id
				users = User.objects.get(username=user)
				user_id_id = users.id
				UserAccount.objects.filter(user_id_id=user_id_id).update(places=places_id)
	return HttpResponse('the end')


def ajax_add_friend_when_authenticated(request, guest_user, hash_code):
	if request.user.is_authenticated() is False:
		return HttpResponseRedirect('/')
	elif request.user.is_authenticated() is True:
		try:
			cards = Cards.objects.get(hash_code=hash_code)
			card_owner = cards.owner
			user1_id = card_owner
			user2_id = request.user
			try:
				relativity = Friends.objects.get((Q(suppliant=user1_id) & Q(accepter=user2_id)) | (Q(suppliant=user2_id) & Q(accepter=user1_id)))
			except ObjectDoesNotExist:
				friends_entry = Friends(suppliant=User.objects.get(username=guest_user), accepter=card_owner, is_active=True)
				friends_entry.save()
		except ObjectDoesNotExist:
			return HttpResponse('smth wrong')
		return HttpResponseRedirect('/messages/'+str(card_owner)+'/')
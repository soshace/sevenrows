# -*- coding: utf-8 -*-

#######################################################
# Карточки
#######################################################

from webservice.models import Cards, CardsActivationHistory
from django.db.models import Q
from webservice.forms import OrderCardForm
from django.core.context_processors import csrf
from django.shortcuts				import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
from webservice.models import UserAccount
import hashlib
import os

import Image, ImageDraw     #from PIL
import qrcode.image.base
import qrcode.image.pil

#/////////////////////////// отрисовка страницы cards
def cards(request):
	if request.user.is_authenticated() is False:
		return HttpResponseRedirect('/')
	elif request.user.is_authenticated() is True:
		total_cards = Cards.objects.filter(owner=request.user).count()
		activated_cards = Cards.objects.filter(Q(owner=request.user) & Q(is_activated=True)).count()
		order_card_form = OrderCardForm(auto_id='id_cards_%s')
		session = request.user
		c = {'session': session, 'order_card_form': order_card_form, 'total_cards': total_cards, 'activated_cards': activated_cards}
		c.update(csrf(request))

		if request.method == 'POST':
			form = OrderCardForm(request.POST)
			if form.is_valid():
				qr_filepath = 'cards/' + str(request.user.id) + '/' + str(hashlib.md5(str(datetime.now())).hexdigest()) + '.png'
				order_card_entry = Cards(owner=request.user,
					label = form.cleaned_data['label'],
					design_no = form.cleaned_data['design_no'],
					order_date = datetime.now(),
					is_activated = False,
					hash_code = card_hash_code(request, 'string'),
					qr_code = card_hash_code(request, 'qr'),
					#qr_filepath = settings.MEDIA_ROOT + 'cards/' + str(request.user.id) + '/' + str(hashlib.md5(str(datetime.now())).hexdigest()) + '.png')
					qr_filepath = qr_filepath)
				order_card_entry.save()
				generate_qr(request, 'http://pogoda.yandex.ru/').save(settings.MEDIA_ROOT + qr_filepath)
				return HttpResponse('saved')
			return HttpResponse('form is not valid!')
		#запилить вывод картинок
		cardObjects = Cards.objects.filter(owner=request.user)
		listofcards = []
		for element in cardObjects:
			tmpdict = {'label': element.label, 'design_no': element.design_no, 'order_date': element.order_date, 'hash_code': element.hash_code, 'is_activated': element.is_activated }
			listofcards.append(tmpdict)
		c['cards'] = listofcards

		return render_to_response('cards.html', c, context_instance=RequestContext(request))

def qr_code_picture(request):
	string = 'http://pogoda.yandex.ru/'
	img = generate_qr(request, string)
	response = HttpResponse(mimetype="image/png")
	img.save(response, "PNG")
	return response

#/////////////////////////// возвращает 8ми значный код человечка
def card_hash_code(request, goal):
	user = User.objects.get(username=request.user)
	user_id = user.id
	if user_id >= 1 and user_id <=9:
		tmpstr = '00' + str(user_id)
	elif user_id >= 10 and user_id <=99:
		tmpstr = '0' + str(user_id)
	elif user_id >= 100 and user_id <=999:
		tmpstr = str(user_id)
	else:
		tmpstr = ''
	if goal == 'qr':
		return tmpstr+str(hashlib.md5(str(datetime.now())).hexdigest())
	else:
	#return HttpResponse(tmpstr+str(hashlib.md5(str(datetime.now())).hexdigest())[0:5])
		return tmpstr+str(hashlib.md5(str(datetime.now())).hexdigest())[0:5]

def generate_qr(request, string):
	if not os.path.isdir(settings.MEDIA_ROOT + 'cards/'):
		os.makedirs(settings.MEDIA_ROOT + 'cards/')
		if not os.path.isdir(settings.MEDIA_ROOT + 'cards/' + str(request.user.id) + '/'):
			os.makedirs(settings.MEDIA_ROOT + 'cards/' + str(request.user.id) + '/')
	return qrcode.make(string, box_size=10, border=1)

#/////////////////////////// показывает страничку человечка
def show_man(request, hash_code):
	request.session.set_expiry(0)
	request.session.save()
	try:
		cards = Cards.objects.get(hash_code=hash_code)
		if cards.owner_id == request.user.id:
			pass
		else:
			Cards.objects.filter(hash_code=hash_code).update(is_activated=True)
		target_id = cards.owner
		if (CardsActivationHistory.objects.filter(card=cards).count() > 2) and CardsActivationHistory.objects.filter(session_key=request.session.session_key).count() == 0:
			return HttpResponse('This card has been more than 3 times activated!')
		else:
			if CardsActivationHistory.objects.filter(session_key=request.session.session_key).count() == 0:
				if str(request.user) == "AnonymousUser":
					who_activated = request.user
				else:
					user = User.objects.get(username=request.user)
					who_activated = user.id
				card_history_entry = CardsActivationHistory(card=cards, who_activated=who_activated, when_activated=datetime.now(), session_key=request.session.session_key)
				card_history_entry.save()
			#информация о человечке
			session = request.user
			#table userauth
			user = User.objects.get(username=target_id)
			first_name = user.first_name
			last_name = user.last_name
			username = user.username
			#table useraccount
			useraccount = UserAccount.objects.get(user_id=target_id)
			date_of_birth = useraccount.date_of_birth
			growth = useraccount.growth
			eyes_color = useraccount.eyes_color
			about = useraccount.about
			personal_field = useraccount.personal_field
			#education = useraccount.education
			#career = useraccount.career
			#places = useraccount.places
			c = {'session': session, 'username': username, 'first_name': first_name, 'last_name': last_name, 'date_of_birth': date_of_birth, 'growth': growth,
				'eyes_color': eyes_color, 'about': about, 'personal_field': personal_field, 'hash_code': hash_code, 'guest_is_here': True}
			c.update(csrf(request))
			return render_to_response('my.html', c, context_instance=RequestContext(request))
	except ObjectDoesNotExist:
		return HttpResponse('hash_code is not valid')

		
	return HttpResponse(target_id)

#/////////////////////////// отрисовка страницы cards__details
def cards_details(request, hash_code):
	try:
		card = Cards.objects.get(Q(hash_code=hash_code) & Q(owner=request.user))
		card_id = card.id
	except ObjectDoesNotExist:
		#!!!!!!!!!!!!!!!!!!!!!!! должен быть редирект или 404, чтобы не прочухали номера карт перебором
		return HttpResponse('hash_code bad or it is not your card')
	else:
		cardHistory = CardsActivationHistory.objects.filter(card=card_id)
		activity = []
		for element in cardHistory:
			tmpdict = {'who': element.who_activated, 'when': element.when_activated}
			activity.append(tmpdict)
		c = {'session': request.user, 'activity': activity}
		c.update(csrf(request))
		return render_to_response('cards__details.html', c, context_instance=RequestContext(request))
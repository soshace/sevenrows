# -*- coding: utf-8 -*-

#######################################################
# Сообщения
#######################################################

from django.contrib.auth.models import User
from webservice.models import Friends, Messages
from django.core.context_processors import csrf
from django.shortcuts				import render_to_response, RequestContext
from django.db.models import Q
from webservice.forms import SendMessageForm
from datetime import datetime

#/////////////////////////// отрисовка страницы MESSANGING
def messages(request):
	if request.user.is_authenticated() is False:
		return HttpResponseRedirect('/')
	elif request.user.is_authenticated() is True:
		user = request.user
		userObject = User.objects.get(username=user)
		user_id = userObject.id
		list_of_friends_where_suppliant = Friends.objects.filter(suppliant=user_id).values_list('accepter')
		list_of_friends_where_accepter = Friends.objects.filter(accepter=user_id).values_list('suppliant')
		friends = []
		for friend in list_of_friends_where_suppliant:
			friends.append(User.objects.get(id=friend[0]).username)
		for friend in list_of_friends_where_accepter:
			friends.append(User.objects.get(id=friend[0]).username)
		send_message_form = SendMessageForm(auto_id='id_messages_toFriend_%s')
		session = request.user
		c = {'session': session, 'friends': friends, 'send_message_form': send_message_form}
		c.update(csrf(request))
		return render_to_response('messages.html', c)

#/////////////////////////// отрисовка страницы сообщения определенному пользователю
def messages_toFriend(request, username):
	if request.user.is_authenticated() is False:
		return HttpResponseRedirect('/')
	elif request.user.is_authenticated() is True:
		user1 = User.objects.get(username=request.user)
		user1_id = user1.id
		try:
			user2 = User.objects.get(username=username)
			user2_id = user2.id
		except ObjectDoesNotExist:
			return HttpResponse('User does not exist')
		#вставляем сообщение пользователя
		message_text = request.POST.get('text','')
		if (message_text is not None and message_text is not u'' and message_text is not ''):
		    message_entry = Messages(suppliant=user1, accepter=user2, text=message_text, datetime=datetime.now())
		    message_entry.save()
		relativity = Friends.objects.get((Q(suppliant=user1_id) & Q(accepter=user2_id)) | (Q(suppliant=user2_id) & Q(accepter=user1_id)))
		if (relativity is not None):
			dictionary = view_chat(request, user1_id, user2_id)
		session = request.user
		c = {'session': session, 'full_path': request.get_full_path(), 'messages': dictionary}
		c.update(csrf(request))
		return render_to_response('messages_toFriend.html', c, context_instance=RequestContext(request))

#/////////////////////////// показывает сообщения пользователей из баз данных
def view_chat(request, user1_id, user2_id):
	list_of_messages = []
	list_of_messages= Messages.objects.filter((Q(suppliant=user1_id) & Q(accepter=user2_id)) | (Q(suppliant=user2_id) & Q(accepter=user1_id))).order_by('datetime')
	messages = []
	suppliant = []
	accepter = []
	datetime = []
	for element in list_of_messages:
		messages.append(element.text)
		if (element.suppliant == request.user):
			suppliant.append('me')
		else:
			suppliant.append(element.suppliant)
		accepter.append(element.accepter)
		datetime.append(element.datetime)
	dictionary = { 'suppliant': suppliant, 'accepter': accepter, 'messages': messages, 'datetime': datetime}
	return dictionary
# -*- coding: utf-8 -*-

#######################################################
# Отображение галереи + Аватар
#######################################################

from webservice.forms import UploadImageForm
from django.core.context_processors import csrf
from webservice.models import Images
from django.shortcuts				import render_to_response
from django.template import RequestContext
from datetime import datetime
from django.contrib.auth.models import User
from django.http import HttpResponse

def images(request):
	if request.user.is_authenticated() is False:
		return HttpResponseRedirect('/')
	elif request.user.is_authenticated() is True:
		upload_image_form = UploadImageForm(auto_id='id_images_%s')
		session = request.user
		c = {'session': session, 'upload_image_form': upload_image_form}
		c.update(csrf(request))
		if request.method == 'POST':
			form = UploadImageForm(request.POST, request.FILES)
			if form.is_valid():
				upload_image_entry = Images(owner=request.user,
					description=form.cleaned_data['description'],
					is_deleted=False,
					is_avatar=False,
					filepath=form.cleaned_data['image'],
					datetime=datetime.now())
				upload_image_entry.save()
				return HttpResponse('saved')
			return HttpResponse('form is not valid!')
		#запилить вывод картинок
		imageObjects = Images.objects.filter(owner=request.user)
		pictures = []
		descriptions = []
		for element in imageObjects:
			pictures.append(element.filepath)
			descriptions.append(element.description)
		c['pictures'] = pictures
		c['descriptions'] = descriptions
		return render_to_response('images.html', c, context_instance=RequestContext(request))
# -*- coding: utf-8 -*-

#######################################################
# brief: Отображение начальной страницы
# author: Denis Nefyodov (denova) 2013
#######################################################

from django.shortcuts				import render_to_response
from django.core.context_processors import csrf
from django.template				import RequestContext
from django.http 					import HttpResponse, HttpResponseRedirect

from webservice.forms 				import RegForm, LoginForm, QRForm

#/////////////////////////// Начальная страница
def index(request):
	if request.user.is_authenticated() is False:
		request.session.set_expiry(0)
		reg_form = RegForm(auto_id='id_reg_%s')
		login_form = LoginForm(auto_id='id_login_%s')
		qr_form = QRForm(auto_id='id_qr_%s')
		
		c = {'reg_form' : reg_form, 'login_form': login_form, 'qr_form': qr_form, 'session': request.user}
		c.update(csrf(request))
		
		return render_to_response('index.html', c, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect("/my/")
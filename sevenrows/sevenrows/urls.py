# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'webservice.views.index'), #????: ???????????, ????? ??? QR.
    (r'my/$', 'webservice.views.my'), #????: ???????????, ????? ??? QR.

    #??????? ?? ???????? ???????
    #(r'scripts/reg/$', 'webservice.views.scripts_reg'),
    (r'account/$', 'webservice.views.account'),
    (r'messages/$', 'webservice.views.messages'),
    (r'^messages/([A-za-z\d]+)/$', 'webservice.views.messages_toFriend'),
    (r'images/$', 'webservice.views.images'),
    url(r'^media/(.*)$', 'django.views.static.serve', {'document_root' : '/home/denova/badaboom/webservice/media/'}),
    (r'cards/$', 'webservice.views.cards'), #???????? ????????
    (r'cards/([a-z0-9]{8})/$', 'webservice.views.cards_details'), #???????? ??????????? ? ????????
    (r'^([A-Za-z0-9]{8})/$', 'webservice.views.show_man'), #??????? ?? ???? ???????? ?? ???????? ????????????

    #???????? ???? ??? ???????
    (r'view_chat/$', 'webservice.views.view_chat'),
    (r'card_hash_code/$', 'webservice.views.card_hash_code'),

    (r'ajax/check/email/$', 'webservice.views.ajax_check_email'),
    (r'ajax/login/$', 'webservice.views.ajax_login'),
    (r'ajax/logout/$', 'webservice.views.ajax_logout'),
    (r'ajax/reg/$', 'webservice.views.ajax_reg'),
    (r'ajax/qr/$', 'webservice.views.ajax_qr'),
    (r'ajax/account/change_all/$', 'webservice.views.ajax_account_change_all'),
    (r'ajax/account/change_plus/$', 'webservice.views.ajax_account_change_plus'),
    (r'ajax/add_friend_when_authenticated/([A-za-z\d]+)/([A-Za-z0-9]{8})/$', 'webservice.views.ajax_add_friend_when_authenticated'),
    (r'ajax/get_label_coords/$', 'webservice.views.ajax_get_label_coords'),
    (r'ajax/set_label_coords/$', 'webservice.views.ajax_set_label_coords'),

    (r'qr_code_picture/$', 'webservice.views.qr_code_picture'),
    # Examples:
    # url(r'^$', 'sevenrows.views.home', name='home'),
    # url(r'^sevenrows/', include('sevenrows.sevenrows.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

from datetime import datetime
from hashlib import md5
from os import path as op
from time import time


#/////////////////////////////////////////////////////////////////////////////////////
#////////////////// Models for users

class ListOfEducation(models.Model):
	education = models.TextField(max_length=250)
	def __unicode__(self):
	    return self.education

class ListOfCareer(models.Model):
	career = models.TextField(max_length=250)
	def __unicode__(self):
	    return self.career

class ListOfPlaces(models.Model):
	places = models.TextField(max_length=250)
	def __unicode__(self):
	    return self.places

class UserAccount(models.Model):
	user = models.OneToOneField(User, default=None)
	date_of_birth = models.DateField(blank=True, null=True)
	growth = models.PositiveSmallIntegerField(blank=True, null=True)
	eyes_color = models.TextField(max_length=15, blank=True, null=True)
	about = models.TextField(max_length=250, blank=True, null=True)
	personal_field = models.TextField(max_length=250, blank=True, null=True)

class Friends(models.Model):
	suppliant = models.ForeignKey(User, default=None, related_name='+')
	accepter = models.ForeignKey(User, default=None, related_name='+')
	is_active = models.BooleanField(default=False)
	#def __unicode__(self):
	#	return self.suppliant

class Messages(models.Model):
	suppliant = models.ForeignKey(User, default=None, related_name='+')
	accepter = models.ForeignKey(User, default=None, related_name='+')
	text = models.TextField(max_length=1000)
	datetime = models.DateTimeField(auto_now_add=True)

#/////////////////////////// upload_to для поля модели Images.image
def upload_to(instance, filename, prefix=None, unique=False):
    """ Auto generate name for File and Image fields.
    """
    ext = op.splitext(filename)[1]
    name = str(instance.pk or '') + filename + (str(time()) if unique else '')

    # We think that we use utf8 based OS file system
    filename = str(instance.owner.id) + '/' + md5(name.encode('utf8')).hexdigest() + ext
    basedir = instance._meta.module_name
    if prefix:
        basedir = op.join(basedir, prefix)
    return op.join(basedir, filename)

class Images(models.Model):
	owner = models.ForeignKey(User, default=None)
	filepath = models.ImageField(upload_to=upload_to, default=None)
	description = models.TextField(max_length=250, default='default')
	datetime = models.DateTimeField(auto_now_add=True, default='1971-12-12 00:00:01')
	is_avatar = models.BooleanField(default=False)
	is_deleted = models.BooleanField(default=False)

class Cards(models.Model):
	owner = models.ForeignKey(User, default=None)
	label = models.TextField(max_length=140)
	design_no = models.PositiveSmallIntegerField(default=1)
	order_date = models.DateTimeField(auto_now_add=True, default='1971-12-12 00:00:01')
	is_activated = models.BooleanField(default=False)
	hash_code = models.TextField(max_length=7)
	qr_code = models.TextField(max_length=150, default='ololo')
	qr_filepath = models.TextField(max_length=140, default='ololo')

class CardsActivationHistory(models.Model):
	card = models.ForeignKey(Cards, default=None)
	who_activated = models.TextField(max_length=250)
	when_activated = models.DateTimeField(auto_now_add=True, default='1971-12-12 00:00:01')
	session_key = models.TextField(max_length=100, default='AnonymousUserSessionKey')

#/////////////////////////////////////////////////////////////////////////////////////
#////////////////// Models for meta data

#////////////////// Remember position for each person
class DrawingsInMy(models.Model):
	user_id = models.ForeignKey(User, default=True)
	main_label_x = models.PositiveSmallIntegerField(default=100)
	main_label_y = models.PositiveSmallIntegerField(default=100)
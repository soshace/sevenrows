# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils import simplejson
from django.contrib.sessions.backends.db import SessionStore

import hashlib #���������� ����� ��� ������
from datetime import datetime
import time

from webservice.forms import RegForm, LoginForm, LogoutForm, QRForm, AccountForm, AccountFormPlus, SendMessageForm, UploadImageForm, OrderCardForm
from django.contrib.auth.models import User
from webservice.models import UserAccount, ListOfEducation, ListOfCareer, ListOfPlaces, Friends, Messages, Images, Cards, CardsActivationHistory
#from webservice.models import UserAuth

from django.core.validators import validate_email, ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models import Q

from django.template import RequestContext

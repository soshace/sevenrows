# -*- coding: utf-8 -*-
from django import forms
from webservice.models import ListOfEducation, ListOfCareer, ListOfPlaces

class RegForm(forms.Form):
	email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Enter email','class': 'form-control'}))
	
class LoginForm(forms.Form):
	email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Enter email','class': 'form-control'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Input password','class': 'form-control'}), label="Your password")

class LogoutForm(object):
	pass

class QRForm(forms.Form):
	hash_code = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter code','class': 'form-control'}), label='Your code')

class AccountForm(forms.Form):
	username = forms.CharField(label="Your nickname", help_text="Your nickname in the end of URL")
	first_name = forms.CharField(label="Your name", help_text="Name")
	second_name = forms.CharField(label="Your family name", help_text="Family name")
	eye_color = forms.CharField(label="Eye color")
	date_of_birth = forms.DateField(widget=forms.DateInput(), label="Date of Birth", help_text="Enter your birthday in yyyy.mm.dd format")
	growth = forms.IntegerField(label="Your growth")
	about = forms.CharField(label="About you")
	personal_field = forms.CharField(widget=forms.widgets.Textarea(), label="Personal field: notes")

class AccountFormPlus(forms.Form):	
	education = forms.CharField(label="Education")
	career = forms.CharField(label="Career")
	places = forms.CharField(label="Places")

class SendMessageForm(forms.Form):
	text = forms.CharField(widget=forms.widgets.Textarea(attrs={'cols': 80, 'rows': 5}), label="Message")

class UploadImageForm(forms.Form):
	image = forms.ImageField(label='Select a image file', help_text='max. ololo megabytes')
	description = forms.CharField(label="Description")

class OrderCardForm(forms.Form):
	label = forms.CharField(label='Enter label here!', help_text='label')
	design_no = forms.IntegerField(label='design_no')
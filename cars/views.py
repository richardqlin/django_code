# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,render_to_response,get_object_or_404

# Create your views here.
from datetime import datetime
from django.http import HttpResponse, Http404, HttpResponseRedirect

from django.contrib import auth
from django.contrib.auth.models import User
#from django.core.context_processors import csrf
from django.template.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
from .models import Rental
from .forms import RentalForm

from django import forms

def login(request):
	c={}
	c.update(csrf(request))
	print 'c:',c
	return render_to_response('login.html',c)

def auth_view(request):
	username=request.POST.get('username','')
	password=request.POST.get('password','')
	user=auth.authenticate(username=username,password=password)
	if user is not None:
		auth.login(request,user)
		return HttpResponseRedirect('/rental/loggedin')
	else:
		return HttpResponseRedirect('/rental/invalid')
def loggedin(request):
	return render_to_response('loggedin.html',{'full_name':request.user.username})

def invalid_login(request):
	auth.logout(request)
	return render_to_response('invalid_login.html')

def logout(request):
	auth.logout(request)
	return render_to_response('logout.html')

def register(request):
	if request.method =='POST':
		form=UserCreationForm(request.POST)
		#print 'form=',form
		if form.is_valid():
			form.save()

		return HttpResponseRedirect('/rental/register_success')

	args={}
	args.update(csrf(request))
	args['form']=UserCreationForm()

	return render_to_response('register.html',args)


def register_success(request):
	return render_to_response('register_success.html')

def menu(request):
	time=datetime.now()
	day=time.strftime('%A')
	return render(request,'menu.html',{'full_name':request.user,'time':time,'day':day})


def update(request):
	time=datetime.now()
	day=time.strftime('%A')
	name=request.user
	if request.method=='POST':
		form=RentalForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/rental/success')
		else:
			return render(request,'update.html',{'user':request.user,'rental':form,'time':time,'day':day})
	form=RentalForm()
	return render(request,'update.html',{'user':request.user,'rental':form,'time':time,'day':day})

def list(request):
	time=datetime.now()
	day=time.strftime('%A')
	rental=Rental.objects.filter(username=request.user)
	context=[]
	for r in rental:
		r_username=str(r.username)
		request_user=str(request.user)
		context_str=[]
		r_rental_car=str(r.rental_car)
		context_str.append(r_rental_car)
		r_available=str(r.available)
		context_str.append(r_available)
		r_reserve=str(r.reserve)
		context_str.append(r_reserve)
		context.append(context_str)
	return render(request,'list.html',{'full_name':request.user,'context':context,'time':time,'day':day})

def delete(request):
	rental=Rental.objects.filter(username=request.user)	
	page=Rental.objects.filter(username=request.user)
	query=request.GET.get('q')
	if query:
		page=page.get(pk=query)
		page.delete()
	return render(request,'delete.html',{'full_name':request.user,'rental':rental,'q':page})

def success(request):
	rental=Rental.objects.filter(username=request.user)
	return render_to_response('success.html',{'user':request.user})
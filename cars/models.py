# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django import forms
from datetime import datetime

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from django.utils.encoding import python_2_unicode_compatible


class Rental(models.Model):
	username=models.ForeignKey(User)
	rental_car=models.CharField(max_length=50)
	available=models.DateTimeField(blank=True)#default=datetime.now(), blank=True)
	reserve=models.BooleanField(default=False)#default=datetime.now(),blank=True)

	def __str__(self):
		return '%s %s %s %s' %(self.username,self.rental_car,self.available,self.reserve)


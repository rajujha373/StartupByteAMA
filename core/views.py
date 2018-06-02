# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Speaker, Tag, Question

from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.db import IntegrityError

# Create your views here.

def signup(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		raw_password = request.POST.get('password')
		
		try:
			user = User.objects.create_user(username=username, password=raw_password)

			user.save()

			user = authenticate(request, username=username, password=raw_password)

			if user is not None:
				if user.is_active:
					login(request, user)
		except IntegrityError as e:
			print('sorry username already exist')
		return redirect('home')

	else:
		context={}
		return render(request, "core/signup.html", context)

def signin(request):
	if request.method == "POST":
		username = request.POST.get("username")
		password = request.POST.get("password")

		user = authenticate(username=username, password=password)

		if user is not None:
			if user.is_active:
				login(request, user)

		return redirect('home')
	else:
		context={}
		return render(request, 'core/signin.html', context)		

def signout(request):
	logout(request)

	return redirect('home')

def homeview(request):
	context = {
		'speakers' : Speaker.objects.all(),
		'tags': Tag.objects.all(),
	}	
	return render(request, 'core/home.html', context)

def detailview(request, speaker_id):
	speaker = Speaker.objects.get(id=speaker_id)
	questions = Question.objects.all().filter(speaker=speaker)
	context = {
		'speaker': speaker,
		'questions': questions,
	}
	return render(request, 'core/detail.html', context)

def askquestionview(request, speaker_id):
	speaker = Speaker.objects.get(id=speaker_id)
	description = request.POST.get('description')

	question = Question.objects.create(speaker=speaker, posted_by=request.user, description=description)
	question.save()

	return redirect('detail', speaker_id)
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Speaker, Tag, Question, Reply

from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

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

@login_required(login_url='/signin/')
def signout(request):
	logout(request)

	return redirect('home')

@login_required(login_url='/signin/')
def homeview(request):
	context = {
		'speakers' : Speaker.objects.all(),
		'tags': Tag.objects.all(),
	}	
	return render(request, 'core/home.html', context)

@login_required(login_url='/signin/')
def detailview(request, speaker_id):
	speaker = Speaker.objects.get(id=speaker_id)
	questions = Question.objects.all().filter(speaker=speaker)
	replies = Reply.objects.all()
	context = {
		'speaker': speaker,
		'questions': questions,
		'replies': replies,
	}
	return render(request, 'core/detail.html', context)

@login_required(login_url='/signin/')
def askquestionview(request, speaker_id):
	speaker = Speaker.objects.get(id=speaker_id)
	description = request.POST.get('description')

	question = Question.objects.create(speaker=speaker, posted_by=request.user, description=description)
	question.save()

	return redirect('detail', speaker_id)

@login_required(login_url='/signin/')
def replyquestionview(request, question_id, speaker_id):
	question = Question.objects.get(id=question_id)
	text = request.POST.get('reply_text')

	reply = Reply.objects.create(question=question, posted_by=request.user, reply_text=text)
	reply.save()

	return redirect('detail', speaker_id)
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Tag(models.Model):
	word = models.CharField(max_length=35)
	slug = models.CharField(max_length=250)
	created_at = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.word

class Speaker(models.Model):
	name = models.CharField(max_length=100)
	photo = models.ImageField()
	brief = models.CharField(max_length=1000)
	description = models.TextField()
	tagline = models.CharField(max_length=1000)
	tags = models.ManyToManyField(Tag, related_name="speakers")
	available_from = models.DateTimeField()
	available_to = models.DateTimeField()
	created_at = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.name

class Question(models.Model):
	speaker = models.ForeignKey(Speaker, on_delete=models.CASCADE, related_name="questions")
	posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
	description = models.TextField()
	answered = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.description

class Reply(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	reply_text = models.TextField()
	posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.reply_text
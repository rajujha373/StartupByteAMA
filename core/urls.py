from django.conf.urls import url
from core import views

urlpatterns = [ 
	url(r'^$', views.homeview, name="home"),
	url(r'^(?P<speaker_id>[0-9]+)/$', views.detailview, name="detail"),

	url(r'^(?P<speaker_id>[0-9]+)/ask/$', views.askquestionview, name="askquestion"),
	url(r'^(?P<speaker_id>[0-9]+)/reply/(?P<question_id>[0-9]+)$', views.replyquestionview, name="replyquestion"),

	url(r'^signup/$', views.signup, name="signup"),
	url(r'^signin/$', views.signin, name="signin"),
	url(r'^signout/$', views.signout, name="signout"),
	

]
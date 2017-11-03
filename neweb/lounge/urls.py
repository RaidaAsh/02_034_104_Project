from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from .views import *

urlpatterns = [
    url(r'^$', loungeHome),
    url(r'^search/$', search),
    url(r'^addLounge/$', addLounge),
    url(r'^delete/success/$', deleteLng),
    url(r'^update/success/$', updateLounge),
    url(r'^details/(.{1,30})/$', getDetails),
	url(r'^add/game/success/(.{1,30})/$', addGame),
    url(r'^add/game/(.{1,30})/$', addGamePage),
    
    url(r'^add/$', addLoungePage),
    url(r'^delete/(.{1,30})/$', deleteLounge),
    url(r'^update/(.{1,30})/$', updateLoungePage),
]

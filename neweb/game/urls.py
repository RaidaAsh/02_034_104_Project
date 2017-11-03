from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from .views import *

urlpatterns = [
    url(r'^$', gameHome),
    url(r'^add/$', addGamePage),
    url(r'^success/$', addGame),
    url(r'^delete/success/$', deleteSuccess),
    url(r'^delete/(.{1,30})/$', deleteGame),
    url(r'^update/success/$', updateGame),
    url(r'^update/(.{1,30})/$', updateGamePage),
    url(r'^details/(.{1,30})/$', getDetails),
	url(r'^book/(.{1,30})/$', book),
    url(r'^bookSuccess/(.{1,30})/$', bookTable),
]

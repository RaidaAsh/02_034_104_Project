from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from .views import *

urlpatterns = [
    url(r'^$', memberHome),
    url(r'^details/(.{1,30})/$', getDetails),
    url(r'^search/$', search),
    url(r'^custom-search/$', customSearch),
    url(r'^addMember/$', addMember),
    url(r'^memberForm/$', addMem),
    url(r'^deleteMember/$', deleteMemberPage),
    url(r'^delete/(.{1,30})/$', deleteMember),
    url(r'^updateMember/(.{1,30})/$', updateMemberPage),
    url(r'^update/(.{1,30})/$', updateMember),
    url(r'^deleteMem/$', deleteMem),
]

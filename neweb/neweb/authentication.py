from django.shortcuts import HttpResponseRedirect, redirect
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from neweb import settings
from neweb.views import *

import abc, six
class AuthRequiredMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not request.user.is_authenticated():
            if not request.path == 'login':
                return response
            else:
                return response
        else:
            return response


#@six.add_metaclass(abc.ABCMeta)
#class State:
    
    #@abc.abstractmethod
    #def respond(self, request, response):
        #pass
    
#class NormalState(State):
    
    #def respond(self, request, response):
        #if not request.user.is_authenticated():
            #return response

#class LoginState(State):
    #def respond(self, request, response):
        
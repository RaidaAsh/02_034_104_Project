# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.generic.base import TemplateView
from django.template import RequestContext
from django.core.mail import EmailMessage
import MySQLdb
import abc, six
from django.shortcuts import render

# Create your views here.

def mailHome(request):
    return render(request, "mail/mailHome.html")
###################################################################3
def sendMail(request):
   email = EmailMessage('IMPORTANT', 'kisuparina', to=["raidanahian@gmail.com","abidnazirisami@gmail.com","sdp02342017@gmail.com"])
   email.send()

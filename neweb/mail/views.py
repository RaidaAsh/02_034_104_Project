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
from members.views import *
import threading
import time
from smtplib import SMTPException
exitFlag = 0
# Create your views here.

def mailHome(request):
    memberList=getMembers('')
    membersJSON = {}
    for member in memberList:
        membersJSON[member.name]=0
    return render(request, "mail/mailHome.html",context= {'members':membersJSON})
###################################################################
def sendMail(request):
   member = request.POST.get('member_name', None)
   subject = request.POST.get('subject', None)
   body = request.POST.get('message', None)
   exitFlag = 0
   conn = Singleton.dbase()
   cursor = conn.getCursor()
   cursor.execute ('select email from Accounts where MemberName like "'+member+'"')
   row = cursor.fetchone()
   mailingThread = MailingThread(1, "mailSender",30,subject,body,request,row[0])
   mailingThread.start()
   return render(request, "mail/sent.html")

######################################################################
class MailingThread (threading.Thread):
   def __init__(self, threadID, name, counter,subject,body,request,email):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
      self.subject = subject
      self.body = body
      self.request = request
      self.email = email
   def run(self):
      mailSender(self, self.name, self.counter, 10,self.subject,self.body,self.request,self.email)
#############################################################################      
def mailSender(mailingThread, threadName, counter, delay,subject,body,request,email):
    flag = 0   
    while counter > 0: 
        if sendMail2(subject,body,request,email) == 1 :
            counter = -1
            flag = 1	  
        time.sleep(delay)    
        counter += 1
###########################################################################
def sendMail2(subject,body,request,emailAddress):    
   try:
       email = EmailMessage(subject, body,'jensenshephard@gmail.com',[emailAddress])
       email.content_subtype = "html"
       email.send()
       return 1
   except:
       print('There was an error sending an email: ')
   return 0
   

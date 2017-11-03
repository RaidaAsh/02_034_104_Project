# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.generic.base import TemplateView
from django.template import RequestContext
from neweb.views import *
import MySQLdb
import abc, six

###############################################################################
class Game:
    def __init__(self, id, name):
        self.name = name
        self.id = id
        self.available="Available"
        self.loungeList=[]
	def addLounge(self,lounge_name):
		self.loungeList.append(lounge_name)
    def addFee(self,fee):
		self.fee = fee
###############################################################################
def gameHome(request):
    conn = Singleton.dbase()
    cursor = conn.getCursor()
    s = cursor.callproc("getAllGames", [])
    gameList=[]
    row = cursor.fetchall()
    for i in row:
        newGame = Game(i[0], i[1])
        gameList.append(newGame)
    return render(request, "game/game.html" ,  context={'games': gameList})
################################################################################
def addGamePage(request):
    return render(request, "game/gameForm.html", context={'warning':""})
################################################################################
def deleteLoungePage(request,name):
    return render(request, "lounge/deleteLounge.html", context={'warning':"",'id': name})
###############################################################
def addGame(request):
    name = request.POST.get('gamename', None)
    fee = request.POST.get('gamefee', None)
    conn = Singleton.dbase()
    cursor = conn.getCursor()
    args = [name,fee,]
    s = cursor.callproc("addGame", args)
    conn.commit()    
    cursor.close()
    
    return render(request, "game/gameSuccess.html", context = {'name': name, 'fee': fee})
###############################################################
###############################################################

def deleteGame(request, gameid):
    newGame = generateDetails(gameid)
    return render(request, "game/confirm.html", context = {'game': newGame})
##########################################################
def deleteSuccess(request):
    gameid=request.POST.get('gameid', None)
    print(gameid)
    conn = Singleton.dbase()
    cursor = conn.getCursor()
    args = [gameid,]
    s = cursor.callproc("deleteGame", args)
    conn.commit()    
    cursor.close()
    
    return render(request, "game/deleteSuccess.html")
################################################################################
def updateGamePage(request,gameid):
    newGame=generateDetails(gameid)
    return render(request, "game/updateForm.html", context={'warning':"", 'game' : newGame})

#################################################################
def updateGame(request):
    gameid = request.POST.get('gameid', None)
    oldGame = generateDetails(gameid)
    name = request.POST.get('gamename', None)
    fee = request.POST.get('gamefee', None)
    if not name:
        name = oldGame.name
    if not fee:
        fee = oldGame.name
    args = [gameid,name,fee,]
    conn = Singleton.dbase()
    cursor = conn.getCursor()
    s = cursor.callproc("updateGame", args)
    conn.commit()    
    cursor.close()
    newGame=generateDetails(gameid)
    return render(request, "game/details.html", context = {'game': newGame, 'message': "Updated Successfully"})
######################################################################
def generateDetails(gameid):
    conn = Singleton.dbase()
    cursor = conn.getCursor ()
    cursor.execute ("select * from GameTable where GameID = "+gameid)
    row = cursor.fetchone()
    newGame = Game(row[0],row[1])
    newGame.addFee(row[2])
    return newGame
################################################################
def getDetails(request, id):
    newGame=generateDetails(id)    
    return render(request, "game/details.html", context = {'game':newGame, 'message':" "})
######################################################################
def book(request, id):
    newGame=generateDetails(id)
    conn = Singleton.dbase()
    cursor = conn.getCursor()
    cursor.execute("select LoungeName from Lounge")
    row = cursor.fetchall()
    lounge=[]
    for i in row:
        lounge.append(i[0])
    return render(request, "game/book.html", context = {'game': newGame, 'message': "", 'lounge': lounge})
#####################################################################
def bookTable(request, id):
    newGame=generateDetails(id)
    conn = Singleton.dbase()
    cursor = conn.getCursor()
    cursor.execute("select * from GameBooking where LoungeID = "+str(id))
    row = cursor.fetchall()
    loungename = request.POST.get('loungename', None)
    start = request.POST.get('startdate', None)
    end = request.POST.get('enddate', None)
    free=1
    for i in row:
        if start >= i[3] and start <= i[4]:
            free=0
        if end >= i[3] and end <= i[4]:
            free=0
        if start <= i[3] and end >= i[4]:
            free=0
    cursor.execute("select LoungeName from Lounge")
    row_2 = cursor.fetchall()
    lounge=[]
    for j in row_2:
        lounge.append(j[0])
    if free==0:
        cursor.close()
        return render(request, "game/book.html", context = {'game': newGame, 'message': "The slot is not available", 'lounge': lounge})
    else:
        cursor.execute("select LoungeID from Lounge where LoungeName = '"+loungename+"'")
        loungeID = cursor.fetchone()
        args = [id, loungeID[0], start, end,]
        s=cursor.callproc("booktable", args)
        conn.commit()
        cursor.close()
        return render(request, "game/book.html", context = {'game': newGame, 'message': "Added successfully", 'lounge': lounge})



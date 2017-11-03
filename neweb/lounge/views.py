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
class Lounge:
    def __init__(self, id, name):
        self.name = name
        self.id = id
        self.available="Available"
        self.games=[] 
    def addGames(self, gameid):
        conn = Singleton.dbase()
        cursor = conn.getCursor()
        cursor.execute("select GameName from GameTable where GameID = "+str(gameid))
        row = cursor.fetchone()
        game = row[0]
        self.games.append(game)
###############################################################################
def loungeHome(request):
    conn = Singleton.dbase()
    cursor = conn.getCursor()
    s = cursor.callproc("getAllLounge", [])
    loungeList=[]
    row = cursor.fetchall()
    for i in row:
        newLounge = Lounge(i[0], i[1])
        loungeList.append(newLounge)
    return render(request, "lounge/loungeHome.html" ,  context={'lounge': loungeList})
################################################################################
def addLoungePage(request):
    return render(request, "lounge/loungeForm.html", context={'warning':""})
################################################################################
def deleteLoungePage(request,name):
    return render(request, "lounge/deleteLounge.html", context={'warning':"",'id': name})
################################################################################
def updateLoungePage(request,loungeid):
    newLounge=generateDetails(loungeid)
    return render(request, "lounge/updatelounge.html", context={'warning':"", 'lounge' : newLounge})
###############################################################
################### Strategy Pattern ##########################
###############################################################
###############################################################
class Context:

    def __init__(self, strategy):
        self._strategy = strategy

    def context_interface(self, request, search_id):
        return self._strategy.searchLng(request, search_id)

###############################################################
@six.add_metaclass(abc.ABCMeta)
class SearchClass():


    @abc.abstractmethod
    def searchLng(self, request, search_id):
        pass
###############################################################

class SearchWithName(SearchClass):


    def searchLng(self, request, search_id):
        conn = Singleton.dbase()
        cursor = conn.getCursor ()
        cursor.execute ("select LoungeID, LoungeName from Lounge where LoungeName like '%%%s%%'" %search_id)
        return cursor.fetchall() 

###############################################################
class SearchWithID(SearchClass):

     def searchLng(self, request, search_id):
        conn = Singleton.dbase()
        cursor = conn.getCursor ()
        cursor.execute ("select LoungeID, LoungeName from Lounge where LoungeID = '%s'" %search_id)
        return cursor.fetchall()

###############################################################
class SearchAll(SearchClass):

     def searchLng(self, request, search_id):
        conn = Singleton.dbase()
        cursor = conn.getCursor ()
        cursor.execute ("select LoungeID, LoungeName from Lounge")
        return cursor.fetchall()
########################################################################################################
def search(request):
    loungeList = []

    name_strategy = SearchWithName()
    id_strategy = SearchWithID()
    all_strategy = SearchAll()
    if request.method == 'POST':
        search_id = request.POST.get('textfield', None)
        if not search_id:
            context = Context(all_strategy)
        elif search_id[0] <= '9' and search_id[0] >= '0':
            context = Context(id_strategy)
        else:
            context = Context(name_strategy)
        
        row = context.context_interface(request, search_id)
        for i in row:
            loungeList.append(Lounge(i[0],i[1]))
        return render(request, "lounge/loungeHome.html",context={'lounge':loungeList})    
##################################################################################################################
################################################################
###############################################################
###############################################################
def addLounge(request):
    name = request.POST.get('loungename', None)
    if not name:
        return render(request, "lounge/loungeForm.html", context={'warning': "Please enter the name of the lounge"})
    conn = Singleton.dbase()
    cursor = conn.getCursor()
    args = [name,]
    s = cursor.callproc("addLounge", args)
    conn.commit()    
    cursor.close()
    
    return render(request, "lounge/loungeSuccess.html", context = {'name': name})
###############################################################
###############################################################

def deleteLounge(request, loungeid):
    newLounge = generateDetails(loungeid)
    return render(request, "lounge/confirmLounge.html", context = {'lounge': newLounge})
##########################################################
def deleteLng(request):
    loungeid=request.POST.get('loungeid', None)
    conn = Singleton.dbase()
    cursor = conn.getCursor()
    args = [loungeid,]
    s = cursor.callproc("deletelounge", args)
    conn.commit()    
    cursor.close()
    
    return render(request, "lounge/deleteSuccess.html")
#################################################################
def updateLounge(request):
    loungeid = request.POST.get('loungeid', None)
    conn = Singleton.dbase()
    cursor = conn.getCursor()
    cursor.execute ("select * from Lounge where loungeID = "+loungeid)
    if cursor.rowcount == 0:
        return render(request, "lounge/updatelounge.html", context={'warning': "Please enter a valid ID"})
    row = cursor.fetchone()
    name = request.POST.get('loungename', None)
    if not name:
        name = row[1]
    args = [loungeid,name,]
    s = cursor.callproc("updateLounge", args)
    conn.commit()    
    cursor.close()
    newLounge=generateDetails(loungeid)
    return render(request, "lounge/details.html", context = {'lounge': newLounge, 'message': "Updated Successfully"})
######################################################################
def generateDetails(loungeid):
    conn = Singleton.dbase()
    cursor = conn.getCursor ()
    cursor.execute ("select * from Lounge where loungeID = "+loungeid)
    row = cursor.fetchone()
    newLounge = Lounge(row[0],row[1])
    cursor.execute("select GameID from LoungeGames where LoungeID = "+str(newLounge.id))
    row_2 = cursor.fetchall()
    for i in row_2:
        newLounge.addGames(i[0])
    return newLounge
######################################################################
def getDetails(request, name):
    newLounge=generateDetails(name)    
    return render(request, "lounge/details.html", context = {'lounge':newLounge, 'message':" "})
######################################################################
def addGamePage(request, id):
    conn = Singleton.dbase()
    cursor = conn.getCursor()
    cursor.execute("select GameID from LoungeGames where LoungeID = "+id)
    row = cursor.fetchall()
    newLounge = generateDetails(id)
    for i in row:
        newLounge.addGames(i[0])
    cursor.execute("select GameName from GameTable")
    row_2 = cursor.fetchall()
    gameList=[]
    for j in row_2:
        boolean = 1
        for k in newLounge.games:
            if(k==j[0]):
                boolean=0
        if(boolean==1):
            gameList.append(j[0])
    return render(request, "lounge/addGame.html", context= {'lounge':newLounge,'gameList':gameList})
######################################################################
def addGame(request, loungeid):
    newgames = request.POST.getlist('game')
    oldLounge = generateDetails(loungeid)
    oldgames = oldLounge.games
    conn = Singleton.dbase()
    cursor = conn.getCursor()
    # For adding
    for newgame in newgames:
        exists=0
        for oldgame in oldgames:
            if oldgame is newgame:
                exists = 1
        if exists == 0:
            cursor.execute('select GameID from GameTable where GameName = "'+newgame+'"')
            row = cursor.fetchone()
            args = [row[0],loungeid,]
            s = cursor.callproc('addGameToLounge', args)
    # For removing
    for oldgame in oldgames:
        exists=0
        for newgame in newgames:
            if oldgame is newgame:
                exists = 1
        if exists == 0:
            cursor.execute('select GameID from GameTable where GameName = "'+newgame+'"')
            row = cursor.fetchone()
            args = [row[0],loungeid,]
            s = cursor.callproc('deleteGameFromLounge', args)
    newLounge = generateDetails(loungeid)
    return render(request, "lounge/details.html", context = {'lounge': newLounge, 'message': "Game added Successfully"})
######################################################################################
def getLoungeList():
    conn = Singleton.dbase()
    cursor = conn.getCursor ()
    cursor.execute ("select * from Lounge")
    row = cursor.fetchall()
    loungeList=[]
    for lounge in row:
        loungeList.append(Lounge(lounge[0], lounge[1]))
    return loungeList

from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.generic.base import TemplateView
from django.template import RequestContext
import datetime
import MySQLdb
import abc, six
from neweb.views import *
###########################################################################
#################Iterator Pattern##########################################
###########################################################################
class IteratorObject(object):
    def __init__(self, iterable_object,start):
        self.list = iterable_object
        self.index = start
        self.count = 0

    def __iter__(self):
        return self

    def next(self):
        if (self.count == len(self.list)):
            raise StopIteration
        self.index = self.index + 1
        self.index = self.index % len(self.list)
        self.count = self.count + 1
        return self.list[self.index]


class ReverseIterator(object):
    def __init__(self, iterable_object):
        self.list = iterable_object
        self.index = len(iterable_object)

    def __iter__(self):
        return self

    def next(self):
        if (self.index == 0):
            raise StopIteration
        self.index = self.index - 1
        return self.list[self.index]
    
class Days(object):

    def __init__(self):
        self.days = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    def forward_iter(self,start):
        return IteratorObject(self.days,start)
    def rev_iter(self):
        return ReverseIterator(self.days)
    
class Times(object):

    def __init__(self):
        self.times = ['Breakfast','Lunch','Snacks','Dinner']
    def forward_iter(self,start):
        return IteratorObject(self.times,start)
    def rev_iter(self):
        return ReverseIterator(self.times)
#########################################################################
############################# NULL Pattern ##############################
#########################################################################
@six.add_metaclass(abc.ABCMeta)
class abstractFood:
    day = Days()
    time = Times()
    weekDayList = Days().days
    dayTimeList = Times().times
    @abc.abstractmethod
    def __init__(self, name, price):
        pass
#########################################################################      
    
    def getWeekdays(self, bitMask):
        bitMask -= 90000000
        weekdays=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'] # This is for the datetime.datetime.today.weekday[] function
        for day in self.day.rev_iter():
            if bitMask%2==1:
                self.days.append(day)
                if day==weekdays[datetime.datetime.today().weekday()]:
                    self.available="Available"
            bitMask = bitMask/10
        self.days.reverse()
        return self.days
#########################################################################    
    def getHours(self, bitMask):
        bitMask -= 90000
        for time in self.time.rev_iter():
            if bitMask%2==1:
                self.times.append(time)
            bitMask = bitMask/10
        self.times.reverse()
        return self.times
#########################################################################    
    def getWeekBitMask(self, days):
        mask = 90000000
        for day in days:
            counter = 0
            for weekDay in self.day.forward_iter(0):
                if weekDay in day:
                    mask+=(10**(6-counter))
                counter+=1
        self.weekBitmask=mask
        return self.weekBitmask
#########################################################################
    def getTimeBitMask(self, times):
        mask = 90000
        for time in times:
            counter = 0
            for dayTime in self.time.forward_iter(0):
                if dayTime in time:
                    mask+=(10**(3-counter))
                counter+=1
        self.timeBitmask=mask
        return self.timeBitmask
#########################################################################    
    def setID(self, ID):
        self.ID = ID
#########################################################################
    def isAvailable(self, target):
        for day in self.day.forward_iter(0):
            if day==target or day=='All':
                return 1
        return 0
#########################################################################
class Food(abstractFood):
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.days=[]
        self.times=[]
        self.available="Not Available"

#########################################################################
class NullFood(abstractFood):
    def __init__(self):
        pass
#########################################################################
#########################################################################
#########################################################################
def generateDetails(name):
    conn = Singleton.dbase()
    cursor = conn.getCursor ()
    args = [name,]
    cursor.callproc ("searchFoodWithName", args)
    row = cursor.fetchone()
    newFood = Food(row[1],row[2])
    days = newFood.getWeekdays(row[3])
    times = newFood.getHours(row[4])
    newFood.setID(row[0])
    return newFood
################################################################
def getDetails(request, name):
    newFood=generateDetails(name)    
    return render(request, "food/details.html", context = {'food':newFood, 'message':" "})
###################################################################
def getEditForm(request, name):
    newFood = generateDetails(name)
    return render(request, "food/editForm.html", context = {'food':newFood})
###################################################################
def getEditResponse(request, name):
    if request.method == 'POST':
        newName = request.POST.get('food_name', None)
        price = request.POST.get('food_price', None)
        days=[]
        times=[]
        days=request.POST.getlist('day')
        times=request.POST.getlist('time')
        weekBitmask=Food(newName,price).getWeekBitMask(days)
        timeBitMask=Food(newName,price).getTimeBitMask(times)
        newFood = generateDetails(name)
        conn = Singleton.dbase()
        cursor=conn.getCursor()
        args=[newFood.ID,newName,price,weekBitmask,timeBitMask,]
        cursor.callproc("updateFood", args)
        conn.commit()
        newFood = generateDetails(newName)
    return render(request, "food/details.html", context = {'food':newFood, 'message':"Updated Successfully"})
##########################################################################
def getFoodList(day):
    conn = Singleton.dbase()
    cursor = conn.getCursor ()
    cursor.execute ("select FoodName, FoodPrice, weekBitmask from FoodItem")
    foodList=[]
    weekList={}
    for days in Food.weekDayList:
        weekList[days]=0
    weekList['All']=0
    row = cursor.fetchall()
    for i in row:
        newFood = Food(i[0], i[1])
        dayList = newFood.getWeekdays(i[2])
        weekList['All']+=1
        for days in dayList:
            weekList[days]+=1
        if newFood.isAvailable(day)==1 or day=='All':
            foodList.append(newFood)
    return {'food':foodList, 'week':weekList, 'currentDay':day}
##########################################################################
def getWeeklyList(request, day):
    foodDict=getFoodList(day)
    return render(request, "food/food.html", context = foodDict) 
#########################################################################

def getAddForm(request):
    newFood = NullFood()
    return render(request, "food/addForm.html", context = {'food':newFood})
###################################################################
def getAddResponse(request):
    newFood = Food("","")
    if request.method == 'POST':
        newName = request.POST.get('food_name', None)
	if newName == "":
            return render(request, "food/addForm.html", context = {'food':newFood,'warning':"Please give a name"})
        price = request.POST.get('food_price', None)
        if price == "":
            return render(request, "food/addForm.html", context = {'food':newFood,'warning':"Place add a price"})
        days=[]
        times=[]
        days=request.POST.getlist('day')
        times=request.POST.getlist('time')
        weekBitmask=Food(newName,price).getWeekBitMask(days)
        timeBitMask=Food(newName,price).getTimeBitMask(times)
        conn = Singleton.dbase()
        cursor=conn.getCursor()
        args=[newName,price,weekBitmask,timeBitMask,]
        cursor.callproc("addFoodItem", args)
        conn.commit()
        newFood = generateDetails(newName)
    return render(request, "food/details.html", context = {'food':newFood, 'message':"Added Successfully"})
###################################################################
def deletePrompt(request, name):
    newFood = generateDetails(name)
    return render(request, "food/confirmDelete.html", context = {'food': newFood})
###################################################################
def deleteFood(request):
    foodName = request.POST.get('foodname', None)
    conn = Singleton.dbase()
    cursor = conn.getCursor()
    args = [foodName,]
    s = cursor.callproc("deleteFood", args)
    conn.commit()    
    cursor.close()
    return render(request, "food/deleteSuccess.html")





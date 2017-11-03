# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.generic.base import TemplateView
from django.template import RequestContext
from neweb.views import *
import MySQLdb
import abc, six
from django.contrib.auth.decorators import permission_required


###############################################################
################### Strategy Pattern ##########################
###############################################################
###############################################################
class Context:

    def __init__(self, strategy):
        self._strategy = strategy

    def context_interface(self, search_id):
        return self._strategy.searchMem(search_id)

###############################################################
@six.add_metaclass(abc.ABCMeta)
class SearchClass():


    @abc.abstractmethod
    def searchMem(self, search_id):
        pass
###############################################################

class SearchWithName(SearchClass):


    def searchMem(self, search_id):
        conn = Singleton.dbase()
        cursor = conn.getCursor()
        args = [search_id,]
        s = cursor.callproc("searchMemWithName", args)
        return cursor.fetchall() 

###############################################################
class SearchWithID(SearchClass):

     def searchMem(self,search_id):
        conn = Singleton.dbase()
        cursor = conn.getCursor()
        args = [search_id,]
        s = cursor.callproc("searchMemWithID", args)
        return cursor.fetchall() 

###############################################################
class SearchAll(SearchClass):

     def searchMem(self, search_id):
        conn = Singleton.dbase()
        cursor = conn.getCursor()
        s = cursor.callproc("searchMemAll")
        return cursor.fetchall() 

class Member:
    subject_instance = Singleton.dbase()
    def __init__(self, id, name):
        self.subject = self.subject_instance.getSubject()
        self.name = name
        self.id = id
    def addDept(self, dept):
        self.subject.notify_all(["", dept])
        self.department=dept
    def addDesignation(self, designation):
        self.subject.notify_all([designation, ""])
        self.designation = designation
    def makeMember(self,id, name,contact,presentAdress,permanentAdress,designation,dept,status,email,type):
        self.name = name
        self.id = id
        self.contact = contact
        self.presentAdress = presentAdress
        self.permanentAdress = permanentAdress
        self.designation = designation
        self.dept = dept
        self.status = status
        self.email = email
        self.type = type
########################################################################################################
def getMembers(search_id):
    if not search_id:
        context = Context(SearchAll())
    elif search_id[0] <= '9' and search_id[0] >= '0':
        context = Context(SearchWithID())
    else:
        context = Context(SearchWithName())
    memberList = []
    row = context.context_interface(search_id)
    for i in row:
        memberList.append(Member(i[0],i[1]))
    return memberList
################################################################################################
def search(request):
    
    if request.method == 'POST':
        search_id = request.POST.get('textfield', None)
        memberList = getMembers(search_id)
        return render(request, "members/members.html",context={'member':memberList})    
################################################################################################
def getDepts(cursor):
    cursor.execute("select department from DeptObserver")
    row2 = cursor.fetchall()
    departments=[]
    for i2 in row2:
        departments.append(i2[0])
    return departments
    
def getDesignations(cursor):
    cursor.execute("select designation from DesignationObserver")
    row3 = cursor.fetchall()
    designations=[]
    for i3 in row3:
        designations.append(i3[0])
    return designations
################################################################################################

def memberHome(request):
    conn = Singleton.dbase()
    cursor = conn.getCursor ()
    cursor.execute ("select MemberID, MemberName, department, designation from Accounts")
    memberList=[]
    row = cursor.fetchall()
    for i in row:
        newMember = Member(i[0], i[1])
        newMember.addDept(i[2])
        newMember.addDesignation(i[3])
        memberList.append(newMember)
    departments=getDepts(cursor)
    designations=getDesignations(cursor)
    cursor.close()
    return render(request, "members/members.html", context={'member': memberList, 'departments':departments, 'designations':designations})
################################################################
###############################################################
###############################################################
def addMember(request):
    name = request.POST.get('username', None)
    if not name:
        return render(request, "members/memberForm.html", context={'warning': "Please enter the name of the member"})
    mail = request.POST.get('usermail', None)
    if not mail:
        return render(request, "members/memberForm.html", context={'warning': "Please enter the E-mail address of the member"})
    cell_no = request.POST.get('contactno', None)
    if not cell_no:
        return render(request, "members/memberForm.html", context={'warning': "Please enter the Contact No. of the member"})
    present_ad = request.POST.get('userprad', None)
    permanent_ad = request.POST.get('userpmad', None)
    dept = request.POST.get('userdept', None)
    if not dept:
        return render(request, "members/memberForm.html", context={'warning': "Please enter the name of the Department of the member"})
    designation = request.POST.get('userdesignation', None)
    if not designation:
        return render(request, "members/memberForm.html", context={'warning': "Please enter the Designation of the member"})
    status = request.POST.get('userstat', None)
    member_type = request.POST.get('usertype', None)
    if not member_type:
        return render(request, "members/memberForm.html", context={'warning': "Please enter the type of the member"})
    conn = Singleton.dbase()
    cursor = conn.getCursor() 
    subject_instance=Singleton.dbase()
    subject = subject_instance.getSubject()
    subject.notify_all([designation,dept])
    args = [name,cell_no,present_ad,permanent_ad,designation,dept,status,mail,member_type,]
    s = cursor.callproc("addMember", args)
    conn.commit()    
    cursor.close()
    return render(request, "members/memberSuccess.html", context = {'name': name, 'mail':mail, 'cell_no':cell_no,'present_ad':present_ad,'permanent_ad':permanent_ad,'dept':dept,'designation':designation, 'status': status,'member_type':member_type})
###############################################################
def addMem(request):
    return render(request, "members/memberForm.html", context={'warning': ""})

####################################################################
def deleteMemberPage(request):
    return render(request, "members/deleteMember.html", context={'warning':""})
####################################################################
def updateMemberPage(request, memberid):
    newMember=generateDetails(memberid)
    return render(request, "members/updateForm.html", context={'warning':"", 'member':newMember})
####################################################################
def deleteMember(request, memberid): 
    conn = Singleton.dbase()
    cursor = conn.getCursor()
    cursor.execute ("select * from Accounts where memberID = "+memberid)
    row = cursor.fetchone()
    return render(request, "members/confirmDelete.html", context = {'name': row[1], 'memberid':row[0],'designation':row[5],'dept':row[6]})
##########################################################
def deleteMem(request):
    memberid = request.POST.get('memberid', None)
    conn = Singleton.dbase()
    cursor = conn.getCursor()
    args = [memberid,]
    s = cursor.callproc("deleteMember", args)
    conn.commit()    
    cursor.close()
    return render(request, "members/deleteSuccess.html")
###################################################################


###########################################################################
def generateDetails(memberid):
    conn = Singleton.dbase()
    cursor = conn.getCursor ()
    cursor.execute ("select * from Accounts where memberID = "+memberid)
    row = cursor.fetchone()
    mem = Member(row[0],row[1]);
    mem.makeMember(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[10])
    cursor.close()
    return mem
################################################################
def getDetails(request, id):
    newMember=generateDetails(id)    
    return render(request, "members/details.html", context = {'member':newMember, 'message':" "})	
###############################################################################
############################# Decorator Pattern ###############################
###############################################################################

def customSearch(request):
    queryObject = ConcreteMemberComponent()
    name=request.POST.get('custom_search', None)
    if name is not None:
        queryObject = ConcreteDecoratorName(queryObject,name)
    department=request.POST.get('dept', None)
    print(department)
    if department is not "":
        queryObject = ConcreteDecoratorDepartment(queryObject,department)
    designation=request.POST.get('designation', None)
    if designation is not "":
        queryObject = ConcreteDecoratorDesignation(queryObject,designation)
    query = queryObject.operation()
    conn = Singleton.dbase()
    cursor = conn.getCursor ()
    cursor.execute (query)
    memberList=[]
    row = cursor.fetchall()
    for i in row:
        newMember = Member(i[0], i[1])
        memberList.append(newMember)
    departments=getDepts(cursor)
    designations=getDesignations(cursor)
    cursor.close()
    return render(request, "members/members.html", context={'member': memberList, 'departments':departments, 'designations':designations})

#########################################################################
#########################################################################
#########################################################################
#########################################################################
@six.add_metaclass(abc.ABCMeta)
class Component():
    @abc.abstractmethod
    def operation(self):
        pass
@six.add_metaclass(abc.ABCMeta)
class Decorator(Component):
    def __init__(self, component, attribute):
        self._component = component
        self.attribute = attribute

    @abc.abstractmethod
    def operation(self, attribute):
        pass


class ConcreteDecoratorName(Decorator):
    def operation(self):
        return self._component.operation() + ' and MemberName like "%' + self.attribute +'%"'


class ConcreteDecoratorDepartment(Decorator):
    def operation(self):
        return self._component.operation() + ' and department like "' + self.attribute +'"'

class ConcreteDecoratorDesignation(Decorator):
    def operation(self):
        return self._component.operation() + ' and designation like "' + self.attribute +'"'

class ConcreteMemberComponent(Component):
    def operation(self):
        return 'select * from Accounts where 1 = 1'
##########################################################################





        
class UpdateClass(AbstractTemplate):        
    def execute(self):
        self.cursor.execute ("select * from Accounts where memberID = "+self.generalid)
        self.row = self.cursor.fetchone()
        row = self.row
        request = self.request
        name = request.POST.get('username', None)
        if not name:
            name = row[1]
        mail = request.POST.get('usermail', None)
        if not mail:
            mail = row[8]
        cell_no = request.POST.get('contactno', None)
        if not cell_no:
            cell_no = row[2]
        present_ad = request.POST.get('userprad', None)
        if not present_ad:
                present_ad = row[3]
        permanent_ad = request.POST.get('userpmad', None)
        if not permanent_ad:
                permanent_ad = row[4]
        dept = request.POST.get('userdept', None)
        if not dept:
            dept = row[6]
        designation = request.POST.get('userdesignation', None)
        if not designation:
            designation = row[5]
        status = request.POST.get('userstat', None)
        if not status:
            status = row[7]
        member_type = request.POST.get('usertype', None)
        if not member_type:
            member_type = row[10]
        args = [self.generalid,name,cell_no,present_ad,permanent_ad,designation,dept,status,mail,member_type,]
        
        subject_instance=Singleton.dbase()
        subject = subject_instance.getSubject()
        subject.notify_all([designation,dept])
        s = self.cursor.callproc("updateMember", args)

def updateMember(request, memberid):
    concrete_class = UpdateClass()
    concrete_class.process(request,memberid)
    
    newMember=generateDetails(memberid)
    return render(request, "members/details.html", context = {'member':newMember, 'message':"Updated Successfully"})
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.generic.base import TemplateView
from django.template import RequestContext
import MySQLdb
import abc, six


################################################################
##################### Observer Pattern #########################
################################################################
class Subject:
    def __init__(self):
        self._observers = set()
        self._subject_state = None

    def attach(self, observer):
        print("Observer added")
        observer._subject = self
        self._observers.add(observer)

    def detach(self, observer):
        observer._subject = None
        self._observers.discard(observer)

    def _notify(self):
        for observer in self._observers:
            observer.update(self._subject_state)

    
    def notify_all(self, arg):
        self._subject_state = arg
        #print(str(self._subject_state))
        self._notify()


################################################################
@six.add_metaclass(abc.ABCMeta)
class Observer:
    def __init__(self):
        self._subject = None
        self._observer_state = None

    @abc.abstractmethod
    def update(self, arg):
        pass


class DepartmentObserver(Observer):
    def update(self, arg):
        self._observer_state = arg
        
        if self._observer_state[1] is not "" and self._observer_state[1] is not None:
            
            conn = Singleton.dbase()
            cursor = conn.getCursor()
            cursor.execute("select department from DeptObserver")
            row = cursor.fetchall()
            isDuplicate=0
            for i in row:
                if self._observer_state[1] == i[0]:
                    isDuplicate=1
            if isDuplicate==0:
                args = [self._observer_state[1],]
                cursor.callproc("addDeptObserver", args)
                conn.commit()
                cursor.close()
class DesignationObserver(Observer):
    def update(self, arg):
        self._observer_state = arg
        if self._observer_state[0] is not "" and self._observer_state[0] is not None:
            conn = Singleton.dbase()
            cursor = conn.getCursor()
            cursor.execute("select designation from DesignationObserver")
            row = cursor.fetchall()
            isDuplicate=0
            for i in row:
                if self._observer_state[0] == i[0]:
                    isDuplicate=1
            if isDuplicate==0:
                args = [self._observer_state[0],]
                cursor.callproc("addDesignationObserver", args)
                conn.commit()
                cursor.close()


##################################################################################
########################### Singleton Pattern ####################################
##################################################################################
class Singleton:
    
    __instance = None
    __conn = MySQLdb.connect (host = "localhost",
                                user = "root",
                                passwd = "ostad21",
                                db = "duclub")
    __subject = Subject()
    dept_observer = DepartmentObserver()
    designation_observer = DesignationObserver()
    __subject.attach(dept_observer)
    __subject.attach(designation_observer)
    @staticmethod
    def dbase():
        if Singleton.__instance == None:
            Singleton()
        return Singleton.__instance 
    def subject():
        if Singleton.__instance == None:
            Singleton()
        return Singleton.__instance 
    def __init__(self):
        if Singleton.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Singleton.__instance = self

    def getCursor(self):
        cursor = self.__conn.cursor()
        return cursor
    def getSubject(self):
        return self.__subject
    def commit(self):
        self.__conn.commit()
        
#########################################################################
@six.add_metaclass(abc.ABCMeta)
class AbstractTemplate():
    conn = None
    cursor = None
    row = None
    generalid = None
    request = None
    def process(self,request,ID):
        self.getMemID(request,ID)
        self.makeConnection()
        self.execute()
        self.closeConnection()
    def getMemID(self,request,ID):
        self.request = request
        self.generalid = ID
    def makeConnection(self):
        self.conn = Singleton.dbase()
        self.cursor = self.conn.getCursor()
        
    @abc.abstractmethod
    def execute(self):
        pass
    def closeConnection(self):
        self.conn.commit()    
        self.cursor.close()
#################################################################################
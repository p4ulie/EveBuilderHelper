'''
Created on Oct 13, 2013

@author: paulie
'''

from Config import *

from EveManufacturingTask import EveManufacturingTask
from EveManufacturingMaterial import EveManufacturingMaterial

class EveManufacturingProject(object):
    '''
    Class for manufacturing projects in Eve Online
    '''

    __id = None
    __name = None
    __description = None
    __notes = None
    __productList = {}
    __stockMaterialList = {} # material in stock, assigned to project
    __taskList = []
    
    def __init__(self, name):
        '''
        Constructor
        '''
        self.__name = name

    def getName(self):
        '''
        Get name of project
        '''
        return self.__name

    def setName(self, name):
        '''
        Set name of project
        '''
        if name != '':
            self.__name = name
        return self.__name
    
    def getMaterialList(self):
        '''
        Colllect and return material list for all tasks
        '''

        projectMaterialObjList = []
        
        listOfTaskMaterialLists = [task.getMaterialList() for task in self.__taskList]

        for taskMaterialList in listOfTaskMaterialLists:
            for taskMaterial in taskMaterialList:

                newMaterialFound = True
                for projMaterial in projectMaterialObjList:
                    if projMaterial.typeID == taskMaterial.typeID:
                        newMaterialFound = False
                        projMaterial.quantity += taskMaterial.quantity
                
                if newMaterialFound:
                    projectMaterialObjList.append(EveManufacturingMaterial(typeID=taskMaterial.typeID, quantity=taskMaterial.quantity))
                
        return projectMaterialObjList

    def getTaskCount(self):
        '''
        Return list of tasks
        '''
        return len(self.__taskList)
    
    def getTaskNamesList(self):
        '''
        Return list of task names
        '''
        return [task.getName() for task in self.__taskList]

    def getTaskList(self):
        '''
        Return list of tasks
        '''
        return self.__taskList

    def getTask(self, name):
        '''
        Return reference to task object
        '''
        return [(task if task.getName() == name else None) for task in self.__taskList][0]
        
    def addTask(self, name=None, blueprint=None, quantity=None):
        '''
        Add new task
        '''
        if not name:
            taskCount = self.getTaskCount()
            name = "Task-%s" % format(taskCount + 1, "04d")
            
        task = EveManufacturingTask(name, blueprint=blueprint)
        self.__taskList.append(task)
        
        return task
        
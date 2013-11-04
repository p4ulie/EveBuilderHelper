'''
Created on Oct 13, 2013

@author: paulie
'''

from Config import *

from EveModules.EveInvBlueprintType import EveInvBlueprintType
from EveManufacturingTask import EveManufacturingTask
from EveManufacturingMaterial import EveManufacturingMaterial

class EveManufacturingProject(object):
    '''
    Class for manufacturing projects in Eve Online
    '''

    projectID = None
    name = None
    description = None
    notes = None
    productList = {}
    stockMaterialList = {} # material in stock, assigned to project
    __taskList = []
    
    def __init__(self, name):
        '''
        Constructor
        '''
        self.__name = name

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
        
    def addTask(self, name=None, blueprint=None, quantity=None, parent=None, recursive=False):
        '''
        Add new task
        '''
        if not name:
            taskCount = self.getTaskCount()
            name = "Task-%s" % format(taskCount + 1, "04d")
            
        task = EveManufacturingTask(name,
                                    blueprint=blueprint,
                                    quantity=quantity,
                                    parent=parent)
        if parent is not None:
            task.taskPriority = parent.taskPriority + 1
        self.__taskList.append(task)
        
        if recursive:
            self.addSubTasks(task, recursive)

        return task

    def addSubTasks(self, parentTask, recursive=False):
        '''
        Add subtasks of a task, automatically recurse deeper if specified
        '''
#        print task.getMaterialList()
        for subTaskMaterial in [mat for mat in parentTask.getMaterialList()]:
            if subTaskMaterial.blueprintTypeID is not None:
                bp = None
                bp = EveInvBlueprintType(blueprintTypeID = subTaskMaterial.blueprintTypeID, ResearchLevelME = 0, ResearchLevelPE = 0)
                newTask = self.addTask(name=subTaskMaterial.typeName,
                                       blueprint=bp,
                                       quantity=subTaskMaterial.quantity, 
                                       parent=parentTask)
                if recursive:
                    self.addSubTasks(newTask, recursive)
                
        
    def deleteTask(self, task=None, taskID=None, name=None):
        '''
        Delete task
        '''
        if task == None:
            if taskID is not None:
                task = [task for task in self.__taskList if task.taskID == taskID]
            elif name is not None:
                task = [task for task in self.__taskList if task.name == name]

        if task is not None:
            children = [child for child in self.__taskList if child.parentTask == task]

            # recursively delete all children tasks
            for child in children:
                self.deleteTask(child)             

            self.__taskList.remove(task)
        
        
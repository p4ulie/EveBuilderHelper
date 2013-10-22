'''
Created on Oct 13, 2013

@author: paulie
'''

from EveManufacturingTask import EveManufacturingTask

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
    
    def getProjectMaterialList(self):
        '''
        Colllect and return material list for all tasks
        '''
        projectMaterialList = {}
        
        listOfMaterialLists = [task.getMaterialList() for task in self.__taskList]

        for list in listOfMaterialLists:
            for material,quantity in list.iteritems():
                if material in projectMaterialList.keys():
                    projectMaterialList[material] += quantity
                else:
                    projectMaterialList[material] = quantity

        return projectMaterialList
    

    def getTaskCount(self):
        '''
        Return list of tasks
        '''
        return len(self.__taskList)
    
    def getTaskList(self):
        '''
        Return list of tasks
        '''
        return [task.getName() for task in self.__taskList]
        
    def addTask(self, name=None, typeID=None):
        '''
        Add new task
        '''
        if not name:
            taskCount = self.getTaskCount()
            name = "Task-%s" % format(taskCount + 1, "03d")
            
        task = EveManufacturingTask(name, typeID=typeID)
        self.__taskList.append(task)
        
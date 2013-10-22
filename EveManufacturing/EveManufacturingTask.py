'''
Created on Oct 13, 2013

@author: paulie
'''

class EveManufacturingTask(object):
    '''
    Class for manufacturing tasks in Eve Online
    '''

    __id = None
    __name = None
    __typeID = None
    __blueprint = None # placeholder for blueprint object
    __taskType = None # manufacturing, invention
    __taskTime = None # duration of task
    __startDate = None
    __finishDate = None
    __taskLevel = None # to determine priority of building
    
    __materialList = {}

    def __init__(self,name=None, typeID=None):
        '''
        Constructor
        '''
        self.__name = name
        self.__typeID = typeID

    def getName(self):
        '''
        Return task name
        '''
        return self.__name     
        
    def getMaterialList(self):
        '''
        Return material list for task
        '''
        return self.__materialList     

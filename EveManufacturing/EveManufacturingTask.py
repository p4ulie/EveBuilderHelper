'''
Created on Oct 13, 2013

@author: paulie
'''

from Config import *

from EveManufacturingMaterial import EveManufacturingMaterial

class EveManufacturingTask(object):
    '''
    Class for manufacturing tasks in Eve Online
    '''

    __id = None
    __name = None
    __manufacturingQuantity = 1
    __typeID = None
    __blueprint = None # blueprint object (not DB blueprintID)
    __blueprintNecessaryRuns = None # blueprint runs needed to manufacture specified quantity
    __taskType = None # manufacturing, invention
    __taskTime = None # duration of task
    __startDate = None
    __finishDate = None
    __taskLevel = None # to determine priority of building
    
    def __init__(self, name, blueprint=None, quantity=1):
        '''
        Constructor
        '''
        self.__name = name
        self.__quantity = quantity 
        self.setBlueprint(blueprint) 

    def getName(self):
        '''
        Return task name
        '''
        return self.__name     

    def setName(self, name=None):
        '''
        Set task name
        '''
        if name:
            self.__name = name

        return self.__name     

    def getQuantity(self):
        '''
        Return task name
        '''
        return self.__manufacturingQuantity     

    def setQuantity(self, quantity=None):
        '''
        Set task name
        '''
        if quantity:
            self.__manufacturingQuantity = quantity

        return self.__manufacturingQuantity     

    def getBlueprint(self):
        '''
        Return blueprint object
        '''
        return self.__blueprint     

    def setBlueprint(self, blueprint=None):
        '''
        Set blueprint
        '''
        if blueprint:
            self.__blueprint = blueprint
            self.__blueprintNecessaryRuns = (int(self.__quantity) / int(self.__blueprint.portionSize)) + 1

        return self.__blueprint     

    def getMaterialList(self,skillPE=5):
        '''
        Return material list for task
        '''
        materialList = []
        if self.__blueprint:
            materialListUnit = self.__blueprint.getManufacturingMaterialsList(skillPE=skillPE)
            for material,quantity in materialListUnit.iteritems():
                materialList.append(EveManufacturingMaterial(DB, typeID=material, quantity=quantity * self.__manufacturingQuantity))
#                materialList[material] = quantity * self.__manufacturingQuantity
             
        return materialList     

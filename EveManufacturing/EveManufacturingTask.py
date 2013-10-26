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

    id = None
    name = None
    manufacturingQuantity = 1
    typeID = None
    __blueprint = None # blueprint object (not DB blueprintID)
    blueprintNecessaryRuns = None # blueprint runs needed to manufacture specified quantity
    taskType = None # manufacturing, invention
    taskTime = None # duration of task
    startDate = None
    finishDate = None
    taskLevel = None # to determine priority of building
    
    def __init__(self, name, blueprint=None, quantity=1):
        '''
        Constructor
        '''
        self.name = name
        self.manufacturingQuantity = quantity 
        self.__blueprint = blueprint 

    @property
    def blueprint(self):
        '''
        Set blueprint
        '''
        return self.__blueprint     

    @blueprint.setter
    def blueprint(self, blueprint):
        '''
        Set blueprint
        '''
        if blueprint:
            self.__blueprint = blueprint
            self.blueprintNecessaryRuns = (int(self.quantity) / int(self.__blueprint.portionSize)) + 1

        return self.blueprint     

    def getMaterialList(self, skillPE=5):
        '''
        Return material list for task
        '''
        materialList = []
        if self.blueprint:
            materialListUnit = self.blueprint.getManufacturingMaterialsList(skillPE=skillPE)
            for material,quantity in materialListUnit.iteritems():
                materialList.append(EveManufacturingMaterial(typeID=material, quantity=(quantity * self.manufacturingQuantity)))
             
        return materialList     

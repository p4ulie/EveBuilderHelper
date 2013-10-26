'''
Created on 25.10.2013

@author: ridb10157

'''

from Config import *

from EveModules.EveInvType import EveInvType

class EveManufacturingMaterial(EveInvType):
    '''
    Class for material, used in manufacturing projects
    '''
    
    quantity = None
    
    def __init__(self, typeID=None, name=None, quantity=None):
        '''
        Constructor, initial data load
        '''
        self.DB = DB

        if typeID:
            self.loadItemByID(typeID)
        else:
            if name:
                self.loadItemByName(name)
        
        if quantity:
            self.quantity = quantity
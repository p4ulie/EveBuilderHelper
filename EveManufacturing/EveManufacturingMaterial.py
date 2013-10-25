'''
Created on 25.10.2013

@author: ridb10157
'''

from EveModules.EveInvType import EveInvType

class EveManufacturingMaterial(EveInvType):
    '''
    Class for material, used in manufacturing projects
    '''
    
    __quantity = None
    
    def getQuantity(self):
        '''
        Return quantity
        '''
        return self.__quantity     

    def setQuantity(self, quantity):
        '''
        Set quantity
        '''
        if quantity:
            self.__quantity = quantity

        return self.__quantity     
 
    def __init__(self, DB, typeID=None, name=None, quantity=None):
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
            self.setQuantity(quantity)
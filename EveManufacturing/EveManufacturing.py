'''
Created on Sep 15, 2014

@author: paulie
'''

import math

from EveMath.EveMathConstants import *

from EveModules import EveDB

class EveManufacturing(EveDB):
    '''
    Class for manufacturing in Eve Online
    '''

    buildList = {}
    buyList = {}
    
    assetList = {}

    def __init__(self, params):
        '''
        Constructor
        '''

    def build(self, blueprintTypeID):
        '''
        Method for calculating amounts of components and materials
        to build an item 
        '''
        
        if blueprintTypeID is not None:
            materials = self.getMaterialsForBlueprint(blueprintTypeID,
                                                      activityID=EVE_ACTIVITY_MANUFACTURING)

    facilityBonus = eDB.getActivityBonusForRamAssemblyLineType(assemblyLineTypeName="Advanced Medium Ship Assembly Array",
                                                                 activityID=EVE_ACTIVITY_MANUFACTURING)['baseMaterialMultiplier']

    facilityBonusComponents = eDB.getActivityBonusForRamAssemblyLineType(assemblyLineTypeName="Component Assembly Array",
                                                                         activityID=EVE_ACTIVITY_MANUFACTURING)['baseMaterialMultiplier']

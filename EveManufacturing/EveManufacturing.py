'''
Created on Sep 15, 2014

@author: paulie
'''


import math

from EveModules.EveItem import EveItem
from EveMath.EveMathConstants import *
from EveMath import EveMathIndustry


class EveManufacturing(EveItem):
    '''
    Class for manufacturing in Eve Online
    '''

    buildList = {}
    buyList = {}

    def __init__(self, dbAccessObj, typeID=None, typeName=None):
        '''
        Constructor
        '''

        self.dbAccessObj = dbAccessObj

        self.getItem(typeID=typeID, typeName=typeName)

    def calcBBList(self, blueprintTypeID=None,
                    activityID=EVE_ACTIVITY_MANUFACTURING,
                    facilityBonus=1,
                    blueprintME=0,
                    runs=1):
        '''
        Method for calculating Build and Buy list with amounts of components
        and materials to build an item
        '''

        self.buildList = {}
        self.buyList = {}

        if blueprintTypeID is not None:
            baseMaterialList = self.getMaterialsForBlueprint(blueprintTypeID,
                                                             activityID=activityID)
        elif self.blueprintTypeID is not None:
            baseMaterialList = self.getMaterialsForBlueprint(self.blueprintTypeID,
                                                             activityID=activityID)
        if baseMaterialList is not None:
            for m in baseMaterialList.itervalues():
                materialID = self.getInvItem(typeID=m["materialTypeID"])["typeID"]
                quantity = m["quantity"]

                #did we actually find an item?
                if materialID is not None:
                    materialBlueprintID = self.getBlueprintIDForItem(typeID=materialID,
                                                                     activityID=activityID)

                    adjustedQuantity = math.ceil(quantity * \
                                                 EveMathIndustry.calculateMEMultiplier(blueprintME,
                                                                                            facilityBonus)) * \
                                                                                            runs

                    # is it player buildable?
                    if materialBlueprintID is not None:
                        self.buildList[materialID] = adjustedQuantity
                    else:
                        self.buyList[materialID] = adjustedQuantity

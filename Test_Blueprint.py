'''
Created on 17.6.2014

@author: Pavol Antalik
'''

import math

from DBAccessSQLite import DBAccessSQLite

from EveMath.EveMathConstants import *

from EveModules import EveDB, EveItem
from EveMath import EveMathIndustry

DB = 'data/eve.db'

BUILD_PRODUCT_NAME = 'Kronos'
BUILD_PRODUCT_COUNT = 1
BUILD_PRODUCT_ME = 9
BUILD_PRODUCT_PE = 18

def main():
    eDB = EveDB.EveDB(dbAccess)
    
    eItem = EveItem.EveItem(dbAccess, typeName=BUILD_PRODUCT_NAME)

    materials = eDB.getMaterialsForBlueprint(eItem.blueprintTypeID,
                                             activityID=EVE_ACTIVITY_MANUFACTURING)

    blueprintME = BUILD_PRODUCT_ME
    blueprintPE = BUILD_PRODUCT_PE
    
    facilityBonusShip = eDB.getActivityBonusForRamAssemblyLineType(assemblyLineTypeName="Advanced Medium Ship Assembly Array",
                                                                 activityID=EVE_ACTIVITY_MANUFACTURING)['baseMaterialMultiplier']

    facilityBonusComponents = eDB.getActivityBonusForRamAssemblyLineType(assemblyLineTypeName="Component Assembly Array",
                                                                         activityID=EVE_ACTIVITY_MANUFACTURING)['baseMaterialMultiplier']

    totalMaterialList = {}

    print "Build list:\n"
    
    for m in materials.itervalues():
        mat = eDB.getInvItem(typeID=m['materialTypeID'])
        myMat = math.ceil(m['quantity'] * EveMathIndustry.calculateMEMultiplier(blueprintME,
                                                                                facilityBonusShip)) * BUILD_PRODUCT_COUNT
        print "%s\t%i" % (mat['typeName'],
                          myMat)

        componentBP = eDB.getBlueprintIDForItem(typeID=m['materialTypeID'])

        if componentBP is None:
            if totalMaterialList.has_key(m['materialTypeID']):
                totalMaterialList[m['materialTypeID']] += myMat
            else:
                totalMaterialList[m['materialTypeID']] = myMat
        else:
            componentMaterials = eDB.getMaterialsForBlueprint(componentBP,
                                                              activityID=EVE_ACTIVITY_MANUFACTURING)
            for cm in componentMaterials.itervalues():
                compMat = eDB.getInvItem(typeID=cm['materialTypeID'])
                myCompMat = math.ceil(cm['quantity'] * EveMathIndustry.calculateMEMultiplier(10, facilityBonusShip)) * myMat
                                                    
                #===============================================================
                # print "\t%s\t%i" % (compMat['typeName'],
                #                     myCompMat)
                #===============================================================
                
                if totalMaterialList.has_key(cm['materialTypeID']):
                    totalMaterialList[cm['materialTypeID']] += myCompMat
                else:
                    totalMaterialList[cm['materialTypeID']] = myCompMat

    print "\nMaterial shopping list:\n"
            
    for m,q in totalMaterialList.iteritems():
        matName = eDB.getInvItem(typeID=m)
        print "%s\t%i" % (matName['typeName'],q)
        

if __name__ == '__main__':
    dbAccess = DBAccessSQLite(DB)

    main()

    dbAccess.close()

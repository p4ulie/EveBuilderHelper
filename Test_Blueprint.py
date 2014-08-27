'''
Created on 17.6.2014

@author: Pavol Antalik
'''

import math

from DBAccessSQLite import DBAccessSQLite

from EveMath.EveMathConstants import * 

from EveModules import EveDB
from EveMath import EveMathIndustry 

DB = 'data/eve.db'

def main():
    
    eDB = EveDB.EveDB(dbAccess)

    # get only 1st row of result, then second value from tuple 
    item =  eDB.getInvItem(typeName = 'Guardian').items()[0][1]
    itemTypeID = item['typeID']
    
    blueprintTypeID = eDB.getBlueprintIDForItem(itemTypeID) 
    
    materials = eDB.getMaterialsForBlueprint(blueprintTypeID, activityID = EVE_ACTIVITY_MANUFACTURING)

    for ramAssemblyLineTypes in eDB.getListOfRamAssemblyLineTypes().values():
        print ramAssemblyLineTypes
            
    for i,m in materials.iteritems():
        mat = eDB.getInvItem(typeID = m['materialTypeID']).items()[0][1]
        print "Quantity %i (%i) of %s" % (m['quantity'],
                                        math.ceil(m['quantity'] * EveMathIndustry.calculateMEMultiplier(8, FACILITY_ME_BONUS_POS_ASSEMBLY_ARRAY)),
                                        mat['typeName'])

    print eDB.getActivityBonusForRamAssemblyLineType(assemblyLineTypeName = "Medium Ship Assembly Array")
    
if __name__ == '__main__':
    dbAccess = DBAccessSQLite(DB)

    main()
    
    dbAccess.close()    
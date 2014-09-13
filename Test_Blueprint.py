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
    item = eDB.getInvItem(typeName='Guardian')
    itemTypeID = item['typeID']

    blueprintTypeID = eDB.getBlueprintIDForItem(itemTypeID)

    materials = eDB.getMaterialsForBlueprint(blueprintTypeID,
                                             activityID=EVE_ACTIVITY_MANUFACTURING)

    facilityBonuses = eDB.getActivityBonusForRamAssemblyLineType(assemblyLineTypeName="Advanced Medium Ship Assembly Array",
                                                                 activityID=EVE_ACTIVITY_MANUFACTURING)

    for m in materials.itervalues():
        mat = eDB.getInvItem(typeID=m['materialTypeID'])
        print "Quantity %i (%i) of %s" % (m['quantity'],
                                        math.ceil(m['quantity'] * EveMathIndustry.calculateMEMultiplier(8,
                                                                                                        facilityBonuses['baseMaterialMultiplier'])),
                                        mat['typeName'])

if __name__ == '__main__':
    dbAccess = DBAccessSQLite(DB)

    main()

    dbAccess.close()

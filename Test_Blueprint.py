'''
Created on 17.6.2014

@author: Pavol Antalik
'''

#import math

from DBAccessSQLite import DBAccessSQLite

from EveMath.EveMathConstants import *

#from EveModules import EveDB, EveItem
#from EveMath import EveMathIndustry
from EveManufacturing import EveManufacturing

DB = 'data/eve.db'

BUILD_PRODUCT_NAME = 'Kronos'
BUILD_PRODUCT_COUNT = 1
BUILD_PRODUCT_ME = 9
BUILD_PRODUCT_PE = 18


def main():
    blueprintME = BUILD_PRODUCT_ME
#    blueprintPE = BUILD_PRODUCT_PE

    eMnf = EveManufacturing.EveManufacturing(dbAccess, typeName=BUILD_PRODUCT_NAME)

    facilityBonusShip = eMnf.getActivityBonusForRamAssemblyLineType(assemblyLineTypeName="Advanced Medium Ship Assembly Array",
                                                                 activityID=EVE_ACTIVITY_MANUFACTURING)['baseMaterialMultiplier']

    eMnf.calcBBList(activityID=EVE_ACTIVITY_MANUFACTURING,
                    blueprintME=blueprintME,
                    facilityBonus=facilityBonusShip,
                    runs=BUILD_PRODUCT_COUNT)

    print "Building: %s" % eMnf.typeName

    for buildTypeID, buildQuantity in eMnf.buildList.iteritems():
        buildName = eMnf.getInvItem(typeID=buildTypeID)
        if buildName is not None:
            print "Build %s\t%d" % (buildName["typeName"], buildQuantity)

    print

    for buyTypeID, buyQuantity in eMnf.buyList.iteritems():
        buyName = eMnf.getInvItem(typeID=buyTypeID)
        if buyName is not None:
            print "Buy %s\t%d" % (buyName["typeName"], buyQuantity)


if __name__ == '__main__':
    dbAccess = DBAccessSQLite(DB)

    main()

    dbAccess.close()

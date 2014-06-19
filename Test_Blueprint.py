'''
Created on 17.6.2014

@author: Pavol Antalik
'''

from DBAccessSQLite import DBAccessSQLite

from EveModules import EveDB
from EveModules import EveItem
from EveModules import EveBlueprint

def main():
    DB = 'Data/ody100-sqlite3-v1.db'
    dbAccess = DBAccessSQLite(DB)
    eDB = EveDB.EveDB(dbAccess)
    
    item = EveItem.EveItem(dbAccess, typeName="Ishtar")

    bp = EveBlueprint.EveBlueprint(dbAccess,
                                   productTypeID=item.typeID,
                                   ResearchLevelME = -4,
                                   ResearchLevelTE = -4)


    print "Manufactured item: %s\n" % item.typeName
    
#    matList = bp.getListOfBaseMaterials()
#    matList = bp.getListOfExtraMaterials()
    matList = bp.getListOfManufacturingMaterials(characterTEskillLevel = 5)
    
    for material, quantity in matList.iteritems():
        matItem = EveItem.EveItem(dbAccess,
                                  typeID=material)
        print "%s: %s" % (matItem.typeName,
                          quantity)
    
if __name__ == '__main__':
    main()
'''
Created on 17.6.2014

@author: Pavol Antalik
'''

from DBAccessSQLite import DBAccessSQLite

from EveModules import EveDB
from EveModules import EveItem
from EveModules import EveBlueprint

def main():
#    DB = 'Data/ody100-sqlite3-v1.db'
#    DB = 'Data/rub110-sqlite3-v1.db'
    DB = 'Data/sqlite-latest.sqlite'
    
    dbAccess = DBAccessSQLite(DB)
    eDB = EveDB.EveDB(dbAccess)
    
    item = EveItem.EveItem(dbAccess, typeName="Guardian")

    bp = EveBlueprint.EveBlueprint(dbAccess,
                                   productTypeID=item.typeID,
                                   ResearchLevelME = -2,
                                   ResearchLevelTE = -1)


    print "Manufactured item: %s\n" % item.typeName
    
    matList = bp.getListOfManufacturingMaterials(characterTEskillLevel = 5)
    
    for material, quantity in matList.iteritems():
        matItem = EveItem.EveItem(dbAccess,
                                  typeID=material)

        print "%s: %s" % (matItem.typeName,
                          quantity)

        # if the part is buildable, list the materials
        if matItem.blueprintTypeID:
            bpOfPart = EveBlueprint.EveBlueprint(dbAccess,
                                                 blueprintTypeID=matItem.blueprintTypeID)
            partMatList = bpOfPart.getListOfManufacturingMaterials(characterTEskillLevel = 5)

            for materialPart, quantityPart in partMatList.iteritems():
                partMatItem = EveItem.EveItem(dbAccess,
                                              typeID=materialPart)
                print "\t %s: %s" % (partMatItem.typeName,
                                     quantityPart)
    
if __name__ == '__main__':
    main()
'''
Created on 14.1.2014

@author: Administrator
'''

from EveModules.EveInvType import * 
from EveModules.EveInvBlueprintType import * 

def main():
    DB = 'Data/ody100-sqlite3-v1.db'
    item = EveInvType(DB, name='Ishtar')
    bp = EveInvBlueprintType(DB, productID = item.typeID, ResearchLevelME=-4, ResearchLevelPE=-4)
    materialList = bp.getManufacturingMaterialsList(skillPE=5)
    
    for material,quantity in materialList.iteritems():
        matItem = EveInvType(DB, typeID=material)
        print "%s: %s" % (matItem.typeName, quantity)
    
if __name__ == '__main__':
    main()
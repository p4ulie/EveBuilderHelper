'''
Created on 9.10.2013

@author: Pavol Antalik
'''

from Config import *
from EveModules.EveItem import *
from EveModules.EveBlueprint import *
from EveModules.EveCharacter import *

ME = -4
PE = -4

def getMaterialList(itemID, blueprintME=0, blueprintPE=0, skillPE=5):
    '''
    Get list of materials for specified item
    '''
    materialList = None
    
    bp = EveBlueprint(DB, productID = itemID, ResearchLevelME = blueprintME, ResearchLevelPE = blueprintPE)
    if bp.blueprintID is not None:
        materialList = bp.getManufacturingMaterials(skillPE=skillPE)

    return materialList 

def main():
    character = EveCharacter('Whalt Thisney')
    character.addSkill('Production Efficiency', 5) 
    
    item = EveItem(DB, name='Ishtar')
    print "Name of item: %s, Meta: %s" % (item.name, item.getMetaGroup())

    materialList = getMaterialList(item.itemID, blueprintME=ME, blueprintPE=PE, skillPE=character.getSkillLevel('Production Efficiency'))    

    buyList = {}
    buildList = {}
    
    # look up components for this item    
    for material, quantity in materialList.iteritems():
        itemMaterial = EveItem(DB, itemID = material)
#        print "Material %s (meta %s): %s units" % (itemMaterial.name, itemMaterial.getMetaGroup(), quantity)

        # doest the component have materials, is it buildable?
        materialListComponent = getMaterialList(itemMaterial.itemID, blueprintME=0, blueprintPE=0, skillPE=character.getSkillLevel('Production Efficiency'))    

        if materialListComponent is not None:
#            print "\tBuild list for %s:" % itemMaterial.name

            if material in buildList.keys():
                buildList[material] += quantity
            else:
                buildList[material] = quantity

            # look up materials for this omponent
            for matComp, quantComp in materialListComponent.iteritems():
                itemMaterialComponent = EveItem(DB, itemID = matComp)
#                print "\t\tMaterial %s: %s units" % (itemMaterialComponent.name, quantComp*quantity)

                # buy the needd amount
                if matComp in buyList.keys():
                    buyList[matComp] += quantComp*quantity
                else:
                    buyList[matComp] = quantComp*quantity

        # if its not buildable, buy it
        else:
            if material in buildList.keys():
                buyList[material] += quantity
            else:
                buyList[material] = quantity

    for m, q in buildList.iteritems():
        i = EveItem(DB, itemID=m)
        print "Build %s of %s" % (q, i.name)

    print
    
    for m, q in buyList.iteritems():
        i = EveItem(DB, itemID=m)
        print "Buy %s of %s" % (q, i.name)

if __name__ == '__main__':
    main()
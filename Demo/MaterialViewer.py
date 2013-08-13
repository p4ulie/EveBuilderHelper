'''
Created on Aug 13, 2013

@author: paulie
'''

from Config import *
from EveModules.EveItem import *
from EveModules.EveBlueprint import *

ME = 0
characterPESkillLvl = 5


def main():
    item = EveItem(DB, name='Anshar')
    bp = item.getBlueprintObject()

    print("Name of item: %s") % (item.name)

    materialList = bp.getManufacturingMaterials(characterPESkillLvl=characterPESkillLvl)
    for material, quantity in materialList.iteritems():
        it = EveItem(DB, itemID = material)
        print("Material %s: %s units") % (it.name, quantity)

if __name__ == '__main__':
    main()
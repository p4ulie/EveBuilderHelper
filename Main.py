
'''
Created on 6.7.2012

@author: PA
'''

from EveItem import *
from EveBlueprint import *
import EveCentral
import locale
from Config import *
import sys

if (sys.platform == 'win32'):
    locale.setlocale(locale.LC_ALL, "us_us.1250")
elif (sys.platform == 'darwin'):
    locale.setlocale(locale.LC_ALL, "en_US")
elif (sys.platform == 'linux2'):
    locale.setlocale(locale.LC_ALL, "en_US.UTF-8")

ME = 0
skillLevelProdEff = 5


def main():
    item1 = EveItem(DB, typeName='Anshar')
    blueprint1 = EveBlueprint(DB, productTypeID = item1.typeID)

    ec = EveCentral.EveCentral()
    print 'Product Name: %s, ID: %s' % (item1.typeName, item1.typeID)
    print 'Parent  BlueprintTypeID: %s' % (blueprint1.blueprintTypeID)

    materialList = blueprint1.getManufacturingMaterials(skillLevelProdEff)

#    ECresult = ec.getItemDataByTypeID(materialList)

    for materialType, materialAmount in materialList:
        material = EveItem(DB, materialType)
        print "Amount of %s-%s: %s" % (material.typeID, material.typeName, locale.format("%d", materialAmount, True))

if __name__ == '__main__':
    main()

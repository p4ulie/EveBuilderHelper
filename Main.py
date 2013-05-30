
'''
Created on 6.7.2012

@author: PA
'''

import EveItem
import EveCentral
import locale
from Config import *

locale.setlocale(locale.LC_ALL, "us_us.1250")

ME = 0
productionEfficiency = 5


def main():
#    invType1 = EveItem.EveItem(DB, 0, typeName='Abaddon')
    invType1 = EveItem.EveItem(DB, 0, typeName='Anshar')
#    invType1 = EveItem.EveItem(DB, 0, typeName='Orca')
#    invType1 = EveItem.EveItem(DB, 24692, typeName='')

    ec = EveCentral.EveCentral()
    print 'Product Name: %s, ID: %s' % (invType1.typeName, invType1.typeID)
    print 'Parent  BlueprintTypeID: %s' % (invType1.parentBlueprintTypeID)

    materialList = invType1.getProduceMaterialIDList()
    materialAmountList = invType1.getManufacturingMaterialAmountList(ME, productionEfficiency)

#    ECresult = ec.getItemDataByTypeID(materialList)

    for materialType, materialAmount in materialAmountList:
        material = EveItem.EveItem(DB, materialType)
        print "Amount of %s-%s: %s" % (material.typeID, material.typeName, locale.format("%d", materialAmount, True))
        #=======================================================================
        # if material.blueprintTypeID:
        #    subMaterialAmountList = material.getManufacturingMaterialAmountList(ME, productionEfficiency)
        #    for subMaterialType, subMaterialAmount in subMaterialAmountList:
        #        subMaterial = EveItem.EveItem(DB, subMaterialType)
        #        print ".... Amount of %s-%s: %s" % (subMaterial.typeID, subMaterial.typeName, locale.format("%d", subMaterialAmount, True))
        #=======================================================================

#        print "buy max: %s" % locale.format("%d", ec.parseItemData(ECresult, materialType, 'buy', 'max'), True)


if __name__ == '__main__':
    main()

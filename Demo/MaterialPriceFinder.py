'''
Created on Aug 18, 2013

@author: paulie
'''

from Config import *
from EveModules.EveItem import *
from EveModules.EveBlueprint import *

from EveModules.EveMapRegion import *
from EveModules.EveMapSolarSystem import *

from EveModules.EveCentral import *

ME = 0
characterPESkillLvl = 5

tradeHubList = {'The Forge': 'Jita IV - Moon 4 - Caldari Navy Assembly Plant',
                'Domain': 'Amarr VIII (Oris) - Emperor Family Academy',
                'Heimatar': 'Rens VI - Moon 8 - Brutor Tribe Treasury',
                'Metropolis': 'Hek VIII - Moon 12 - Boundless Creation Factory',
                'Sinq Laison': 'Dodixie IX - Moon 20 - Federation Navy Assembly Plant'
                }

stationJita = 'Jita IV - Moon 4 - Caldari Navy Assembly Plant'

               
def main():
    item = EveItem(DB, name='Caldari Fuel Block')
    bp = item.getBlueprintObject()
    bp.researchLevelME = 40

    print("Name of item: %s\n") % (item.name)

    regionIDList = []
    for regName in tradeHubList.keys():
        region = EveMapRegion(DB, regionName=regName)
        regionIDList.append(region.regionID) 

    solarSys = EveMapSolarSystem(DB, solarSystemName='Jita')

    ec = EveCentral()

    materialList = bp.getManufacturingMaterials(characterPESkillLvl=characterPESkillLvl)
    for material in materialList.keys():
        # Get Jita price
        matItem = EveItem(DB, itemID=material)
        print "Getting Jita price for item %s..." % matItem.name
        resultJita = ec.marketstatGet(material, useSystem=solarSys.solarSystemID)
        priceJitaBuyMax = float(ec.marketstatParse(resultJita, material, 'buy', 'max'))
        print "Jita price for item %s is %s (max buy)\n" % (matItem.name, priceJitaBuyMax)
        
        print "Getting trade hub prices for item %s..." % matItem.name
        result = ec.quicklookGetList(material, regionLimit=regionIDList, orderType='sell_orders')
    
        for line in result:
            if line[4] in tradeHubList.values():
                if float(line[7]) < priceJitaBuyMax:
                    print "Item: %s, station: %s, price: %f, quantity: %s" % (line[1], line[4], float(line[7]), line[8])

        print "\n"
    

if __name__ == '__main__':
    main()
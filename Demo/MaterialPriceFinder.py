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
        result = ec.marketstatGet(material, useSystem=solarSys.solarSystemID)
        jita_buy_max = ec.marketstatParse(result, material, 'buy', 'max')
        
        # self, typeIDList, setHours, regionLimit, useSystem, setMinQ, orderType    
        result = ec.quicklookGetList(material, regionLimit=regionIDList, orderType='sell_orders')
    
        for line in result:
            if line[4] in tradeHubList.values():
                print line
    

if __name__ == '__main__':
    main()
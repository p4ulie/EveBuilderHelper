'''
Created on Aug 18, 2013

@author: paulie
'''

import sqlite3
import sys
import locale

if (sys.platform == 'win32'):
    locale.setlocale(locale.LC_ALL, "us_us.1250")
elif (sys.platform == 'darwin'):
    locale.setlocale(locale.LC_ALL, "en_US")
elif (sys.platform == 'linux2'):
    locale.setlocale(locale.LC_ALL, "en_US.UTF-8")

from Config import *
from EveModules.EveItem import *
from EveModules.EveBlueprint import *

from EveModules.EveMapRegion import *
from EveModules.EveMapSolarSystem import *

from EveModules.EveCentral import *

con = sqlite3.connect(":memory:")
con.text_factory = str
cur = con.cursor()
cur.executescript("""
    create table prices(
        itemID integer,
        itemName text,
        regionID integer,
        stationID integer,
        stationName text,
        security real,
        range integer,
        price real,
        volRemain integer,
        minVolume integer,
        expires text,
        reportedTime text,
        orderType text,
        jitaBuyMax real
    );
    """)

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
    item = EveInvType(DB, name='Caldari Fuel Block')
    bp = item.getBlueprintObject()
    bp.researchLevelME = 40

    materialList = bp.getManufacturingMaterials(characterPESkillLvl=characterPESkillLvl)

    #===========================================================================
    # item = EveInvType(DB, name='Robotics')
    # materialList = {}
    # materialList[item.itemID] = 0
    #===========================================================================

    print("Name of item: %s\n") % (item.name)

    regionIDList = []
    for regName in tradeHubList.keys():
        region = EveMapRegion(DB, regionName=regName)
        regionIDList.append(region.regionID) 

    solarSys = EveMapSolarSystem(DB, solarSystemName='Jita')

    ec = EveCentral()

    priceListJita = {}
        
    for material in materialList.keys():
        # Get Jita price
        matItem = EveInvType(DB, itemID=material)
        print "Getting Jita price for item %s..." % matItem.name
        resultJita = ec.marketstatGet(material, useSystem=solarSys.solarSystemID)
        priceJitaBuyMax = float(ec.marketstatParse(resultJita, material, 'buy', 'max'))
        priceListJita[material] = priceJitaBuyMax 
        
        print "Getting trade hub prices for item %s..." % matItem.name
        result = ec.quicklookGetList(material, regionLimit=regionIDList, orderType='sell_orders')
    
        for line in result:
            if line[4] in tradeHubList.values():
                cur.execute("""INSERT INTO prices
                                (itemID,
                                itemName,
                                regionID,
                                stationID,
                                stationName,
                                security,
                                range,
                                price,
                                volRemain,
                                minVolume,
                                expires,
                                reportedTime,
                                orderType,
                                jitaBuyMax)
                                values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'sell', ?)
                """, (matItem.typeID, matItem.name, line[2], line[3], line[4], line[5], line[6], line[7],
                      line[8], line[9], line[10], line[11], priceJitaBuyMax)
                )

    print "\nList of items:\n"

    for material in materialList.keys():
        matItem = EveInvType(DB, itemID=material)
        print "\nItem: %s (Jita buy max: %s)\n" % (matItem.name, priceListJita[matItem.typeID])
        for order in cur.execute('''SELECT itemName, price, volRemain, stationName, (jitaBuyMax - price) * volRemain as savings
                                    FROM prices WHERE price < jitaBuyMax AND itemID = ?
                                    AND security > 0.4 AND volRemain > 1
                                    AND orderType = "sell"
                                    ORDER BY price''',
                                    (material,)):
            print 'Sell %s: %s units for %s (%s) - saving %s' % (order[0], order[2], order[1], order[3], locale.currency( order[4], symbol=False, grouping=True))

    print "\nList of items for trade hubs:\n"

    for tradeHub in tradeHubList.values():
        if tradeHub != 'Jita IV - Moon 4 - Caldari Navy Assembly Plant':
            print "\n%s:\n" % tradeHub
            for order in cur.execute('''SELECT itemName, price, volRemain, stationName, (jitaBuyMax - price) * volRemain as savings
                                        FROM prices WHERE price < jitaBuyMax 
                                        AND stationName = ?
                                        AND security > 0.4 AND volRemain > 1
                                        AND orderType = "sell"
                                        ORDER BY itemName, price''',
                                        (tradeHub,)):
                print "Sell %s: %s units for %s - saving %s" % (order[0], order[2], order[1], locale.currency( order[4], symbol=False, grouping=True))

    print "\n"
                
if __name__ == '__main__':
    main()
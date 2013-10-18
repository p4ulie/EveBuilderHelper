'''
Created on 27.9.2013

@author: RIDB10157
'''

import sys
import locale

if (sys.platform == 'win32'):

    locale.setlocale(locale.LC_ALL, "us_us.1250")

elif (sys.platform == 'darwin'):

    locale.setlocale(locale.LC_ALL, "en_US")

elif (sys.platform == 'linux2'):

    locale.setlocale(locale.LC_ALL, "en_US.UTF-8")


from EveModules.EveItem import * 
from EveModules.EveGroup import * 
from EveModules.EveMarketData import *

if __name__ == '__main__':
    Tritanium_ID = 34
    Strong_Blue_Pill_Booster_ID = 10156

    itemID = Tritanium_ID
#    itemID = Strong_Blue_Pill_Booster_ID

    emd = EveMarketData()

#    emd.deleteAllOrders()

    DB = '../../data/ody100-sqlite3-v1.db'
    eGroup = EveGroup(DB, groupName = 'Mineral')
    eItem = EveInvType(DB)
    
    for item in eItem.getItemsList(eGroup.groupID):
        itemID = item[0]
        print "Getting data for %s..." % item[2]
    
        result = emd.getMinSellOrderPrice(itemID = itemID, stationName=JITA_STATION_NAME)
        print "Min sell order Jita: %s" % result
    
        jitaMaxBuy = emd.getMaxBuyOrderPrice(itemID = itemID, stationName=JITA_STATION_NAME)
        print "Max buy order Jita: %s" % jitaMaxBuy
    
        query = '''
        select itemName, stationName, price, volRemain, round((? - price) * volRemain) as saving
        from prices
        where
        orderType = 'sell_orders' and
        itemID = ? and
        price < ? and
        security > 0 and
        saving > 10000000
        order by saving desc
        '''
        param = (jitaMaxBuy, itemID, jitaMaxBuy)
        
        orders = emd.execQuery(query, param)
    
        print "List of sell orders (low and highsec) lower than Jita buy:"
            
        for order in orders:
            #print "Price: %.2f, Saving: '%s' for amount: '%s' in station: %s" % (order[2], locale.format('%d', order[4], 1), locale.format('%d', order[3], 1), order[1])
            print "Price: %.2f, Saving: '%s' for amount: '%s' in station: %s" % (order[2], locale.currency(order[4], symbol=False, grouping=True), locale.format('%d', order[3], 1), order[1])

        print
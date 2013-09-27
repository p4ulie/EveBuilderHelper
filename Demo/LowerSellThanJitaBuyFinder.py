'''
Created on 27.9.2013

@author: RIDB10157
'''

import locale
locale.setlocale(locale.LC_ALL, '')

from EveModules.EveMarketData import *

if __name__ == '__main__':
    Tritanium_ID = 34
    Strong_Blue_Pill_Booster_ID = 10156

    itemID = Tritanium_ID
#    itemID = Strong_Blue_Pill_Booster_ID

    emd = EveMarketData()

#    emd.deleteAllOrders()
    
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
        print "Price: %.2f, Saving: '%s' for amount: '%s' in station: %s" % (order[2], locale.format('%d', order[4], 1), locale.format('%d', order[3], 1), order[1])

'''
Class for Eve Market data fetching and storing 
Using sqlite as storage

Created on 12.9.2013

@author: PA
'''

import sqlite3 as lite
import time
import math
import sys
from EveModules.EveCentral import *

OLDER_THAN_MINUTES_DEFAULT = 60

defaultDBFile = 'marketdata.db'
marketDataSources = ('EveCentral')

JITA_STATION_NAME = r'Jita IV - Moon 4 - Caldari Navy Assembly Plant'
JITA_STATION_ID = r'60003760'

class EveMarketData(object):
    '''
    Class for Eve Market data fetching and storing 
    '''

    DB = ''
    
    def execQuery(self, query, param=None, executemany=False, commit=False):
        '''
        Main method for accessing the DB
        '''
        dbcon = ''
        
        try:
            dbcon = lite.connect(self.DB)
            cur = dbcon.cursor()

            if executemany and param:
                cur.executemany(query, param)
            else:
                if param and not executemany:
                    cur.execute(query, param)
                else:
                    cur.execute(query)

            if commit:
                dbcon.commit()

            rows = cur.fetchall()
        except lite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)
        finally:
            if dbcon:
                dbcon.close()
        return rows
    
    def fetchOrdersFromEveCentral(self, **kwargs):
        '''
        Fetch data from Eve-Central  
        '''

        ec = EveCentral()
        result = ec.quicklookGetList(**kwargs)

        ts = time.time()

        data = []
        for line in result:
            data.append((line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8], line[9], line[10], line[11], line[12], ts)
                        )
#        for line in result:
        query = """INSERT INTO prices
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
                        timeStampFetch)
                        values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        data = self.execQuery(query, data=data, executemany=True, commit=True)
            
        return result

    def deleteAllOrders(self):
        query = """DELETE FROM prices"""
        self.execQuery(query, commit=True)
        
    def deleteOrdersOlderThanMinutes(self, **kwargs):
        ts = time.time()
        if kwargs['ifOlderThanMinutes']:
            minutesThreshold = kwargs['ifOlderThanMinutes']
        else:
            minutesThreshold = OLDER_THAN_MINUTES_DEFAULT
            
        olderThanMinutes = math.floor(ts - (minutesThreshold * 60))
        
        if kwargs['itemID']:
            query = """DELETE FROM prices WHERE itemID = ? AND timeStampFetch < ?"""
            params = (kwargs['itemID'], olderThanMinutes)
        else:
            query = """DELETE FROM prices WHERE timeStampFetch < ?"""
            param = (olderThanMinutes, )
        self.execQuery(query, params, commit=True)

    def areOrdersTooOld(self, itemID, **kwargs):
        if itemID:
            ts = time.time()
            if 'ifOlderThanMinutes' in kwargs.keys():
                minutesThreshold = kwargs['ifOlderThanMinutes']
            else:
                minutesThreshold = OLDER_THAN_MINUTES_DEFAULT

            olderThanMinutes = math.floor(ts - (minutesThreshold * 60))
            
            query = """SELECT max(timeStampFetch) FROM prices WHERE itemID = ?"""
            param = (itemID,)
            data = self.execQuery(query, param)[0][0]

            if data < olderThanMinutes:
                return True
            else:
                return False
        return False
    
    def fetchOrders(self, **kwargs):
        '''
        Fetch data from various Market pages (Eve-Central, Eve market Data, ...)  
        '''
        # if not defined, set Eve-Central as default data source
        if not 'marketDataSource' in kwargs.keys():
            kwargs['marketDataSource'] = 'Eve-Central'

        if kwargs['marketDataSource'] == 'Eve-Central':
            if self.fetchOrdersFromEveCentral(**kwargs):
                pass
        elif kwargs['marketDataSource'] == 'Eve-MarketData':
                pass

#         # if we have some new data, delete all older
#         self.deleteOrdersOlderThanMinutes(**kwargs)
            
    def getMinSellOrder(self, itemID, **kwargs):
        '''
        Get sell order with minimum price
        '''
        # only update data if DB entries got older than threshold
        if self.areOrdersTooOld(itemID, **kwargs):
            print "Old data detected, fetching current orders..."
#            self.fetchOrders(**kwargs)

        param = []

        query = """SELECT min(price) FROM prices WHERE orderType = 'sell_orders' AND itemID = ?"""
        param.append(itemID)
         
        if 'regionID' in kwargs.keys():
            query += """ AND regionID = ?"""
            param.append(kwargs['regionID'])
        if 'stationID' in kwargs.keys():
            query += """ AND stationID = ?"""
            param.append(kwargs['stationID'])
        if 'stationName' in kwargs.keys():
            query += """ AND stationName = ?"""
            param.append(kwargs['stationName'])

        result = self.execQuery(query, param)
        return result

    def getMaxBuyOrder(self, itemID, **kwargs):
        '''
        Get buy order with maximum price
        '''
        # only update data if DB entries got older than threshold
        if self.areOrdersTooOld(**kwargs):
            print "Old data detected, fetching current orders..."
#            self.fetchOrders(**kwargs)

        param = []
            
        query = """SELECT max(price) FROM prices WHERE orderType = 'buy_orders' AND itemID = ?"""
        param.append(itemID)
         
        if 'regionID' in kwargs.keys():
            query += """ AND regionID = ?"""
            param.append(kwargs['regionID'])
        if 'stationID' in kwargs.keys():
            query += """ AND stationID = ?"""
            param.append(kwargs['stationID'])
        if 'stationName' in kwargs.keys():
            query += """ AND stationName = ?"""
            param.append(kwargs['stationName'])

        result = self.execQuery(query,param)
        return result

    def getOrders(self, itemID, **kwargs):
        '''
        Get orders. If older, get new list from external source 
        '''
        # only update data if DB entries got older than threshold
        if self.areOrdersTooOld(**kwargs):
            print "Old data detected, fetching current orders..."
            self.fetchOrders(**kwargs)

        param = []
        
        query = """SELECT * FROM prices WHERE itemID = ?"""
        param.append(itemID)
         
        if kwargs['regionID']:
            query += """ AND regionID = ?"""
            param.append(kwargs['regionID'])
        if kwargs['stationID']:
            query += """ AND stationID = ?"""
            param.append(kwargs['stationID'])
        if kwargs['stationName']:
            query += """ AND stationName = ?"""
            param.append(kwargs['stationName'])
        if kwargs['orderType']:
            query += """ AND orderType = ?"""
            param.append(kwargs['orderType'])

        result = self.execQuery(query, param)
        return result
    
    def __init__(self, dbFile=defaultDBFile):
        '''
        Create a DB connection
        '''

        self.DB = dbFile
        
        query = """
            create table if not exists prices(
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
                timeStampFetch real
            );
            """
        self.execQuery(query)
    
if __name__ == '__main__':
    Tritanium_ID = 34
    Strong_Blue_Pill_Booster_ID = 10156

    itemID = Tritanium_ID
#    itemID = Strong_Blue_Pill_Booster_ID
    
    emd = EveMarketData()
        
    print "Min sell order Jita: %s" % emd.getMinSellOrder(itemID = itemID, stationName=JITA_STATION_NAME)

#===============================================================================
#     select itemName, stationName, price, volRemain, round(((4.88 - price) * volRemain)/1000000) as savings, (volRemain * 0.01) as logi from prices
# where
# orderType = 'sell_orders' and
# itemName = 'Tritanium' and
# price <
# (select max(price) from prices
# where
# itemName = 'Tritanium' and
# stationName = 'Jita IV - Moon 4 - Caldari Navy Assembly Plant'
# and orderType = 'buy_orders')
# and
# security > 0
# order by savings desc
# ;
#===============================================================================

    
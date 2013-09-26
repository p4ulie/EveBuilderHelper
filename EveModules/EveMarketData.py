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
    
    def execQuery(self, query, data=None, executemany=True, commit=False):
        '''
        Main method for accessing the DB
        '''
        dbcon = ''
        
        try:
            dbcon = lite.connect(self.DB)
            cur = dbcon.cursor()

            if executemany and data:
                cur.executemany(query, data)
            else:
                if data and not executemany:
                    cur.execute(query, data)
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
            query = """DELETE FROM prices WHERE itemID = %s AND timeStampFetch < %s""" % (kwargs['itemID'], olderThanMinutes)
        else:
            query = """DELETE FROM prices WHERE timeStampFetch < %s""" % olderThanMinutes
        self.execQuery(query, commit=True)

    def areOrdersTooOld(self, itemID, **kwargs):
        if itemID:
            ts = time.time()
            if kwargs['ifOlderThanMinutes']:
                minutesThreshold = kwargs['ifOlderThanMinutes']
            else:
                minutesThreshold = OLDER_THAN_MINUTES_DEFAULT

            olderThanMinutes = math.floor(ts - (minutesThreshold * 60))
            
            query = """SELECT max(timeStampFetch) FROM prices WHERE itemID = ?"""
            data = self.execQuery(query, itemID)[0][0]

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
        if not 'marketDataSource' in kwargs:
            kwargs['marketDataSource'] = 'EveCentral'
        if kwargs['marketDataSource'] == 'EveCentral':
            if self.fetchOrdersFromEveCentral(**kwargs):
                # if we have some new data, delete all older
                self.deleteOrdersOlderThanMinutes(**kwargs)

    def getMinSellOrder(self, itemID, regionID=None, stationID=None, stationName=None):
        query = """SELECT min(price) FROM prices WHERE orderType = 'sell_orders' AND itemID = %s""" % itemID 
        if regionID:
            query += """ AND regionID = %s""" % regionID
        if stationID:
            query += """ AND stationID = %s""" % stationID
        if stationName:
            query += """ AND stationID = %s""" % stationName

        result = self.execQuery(query)
        return result

    def getOrders(self, itemID, **kwargs):
        '''
        Get orders. If older, get new list from external source 
        '''
        # only update data if DB entries got older than threashhold
        if self.areOrdersTooOld(**kwargs):
            print "Old data detected, fetching current orders..."
            self.fetchOrders(**kwargs)
            
        query = """SELECT * FROM prices WHERE itemID = %s""" % itemID 
        if kwargs['regionID']:
            query += """ AND regionID = %s""" % kwargs['regionID']
        if kwargs['stationID']:
            query += """ AND stationID = %s""" % kwargs['stationID']
        if kwargs['stationName']:
            query += """ AND stationID = %s""" % kwargs['stationName']
        if kwargs['orderType']:
            query += """ AND orderType = %s""" % kwargs['orderType']

        result = self.execQuery(query)
        return result

    def getMaxBuyOrder(self, itemID, regionID=None, stationID=None, stationName=None):
        query = """SELECT max(price) FROM prices WHERE orderType = 'buy_orders' AND  itemID = %s""" % itemID 
        if regionID:
            query += """ AND regionID = %s""" % regionID
        if stationID:
            query += """ AND stationID = %s""" % stationID
        if stationName:
            query += """ AND stationID = %s""" % stationName

        result = self.execQuery(query)
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

#    itemID = Tritanium_ID
    itemID = Strong_Blue_Pill_Booster_ID
    
    emd = EveMarketData()
#    emd.deleteOrdersOlderThanMinutes(OLDER_THAN_MINUTES_DEFAULT)
#    emd.deleteOrdersOlderThanMinutes(itemID, 1)
#    emd.deleteAllOrders()
        
    print "Fetching orders..."
    emd.fetchOrders(itemID = itemID, orderType = 'sell_orders', ifOlderThanMinutes = OLDER_THAN_MINUTES_DEFAULT)
    print "Done"
    
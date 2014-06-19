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

            if executemany:
                cur.executemany(query, param)
            else:
                if param:
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

        if result:
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
            data = self.execQuery(query, param=data, executemany=True, commit=True)
            
        return result

    def deleteAllOrders(self):
        '''
        DB cleanup - delete all entries 
        '''
        query = """DELETE FROM prices"""
        self.execQuery(query, commit=True)
        
    def deleteOrdersOlderThanMinutes(self, **kwargs):
        '''
        Delete market orders older than specified amount of minutes
        '''
        ts = time.time()
        if 'ifOlderThanMinutes' in kwargs.keys():
            minutesThreshold = kwargs['ifOlderThanMinutes']
        else:
            minutesThreshold = OLDER_THAN_MINUTES_DEFAULT
            
        olderThanMinutes = math.floor(ts - (minutesThreshold * 60))

        param = []
        
        if kwargs['itemID']:
            query = """DELETE FROM prices WHERE itemID = ? AND timeStampFetch < ?"""
            param.append(kwargs['itemID'])
            param.append(olderThanMinutes)
        else:
            query = """DELETE FROM prices WHERE timeStampFetch < ?"""
            param.append(olderThanMinutes)
        self.execQuery(query, param, commit=True)

    def areOrdersTooOld(self, **kwargs):
        '''
        Determine whether there are only orders older than speciefied
        amount of minutes for specific itemID
        (i.e. we need to refresh the cache)
        '''
        if 'itemID' in kwargs.keys():
            param = []
            ts = time.time()
            if 'ifOlderThanMinutes' in kwargs.keys():
                minutesThreshold = kwargs['ifOlderThanMinutes']
            else:
                minutesThreshold = OLDER_THAN_MINUTES_DEFAULT

            olderThanMinutes = math.floor(ts - (minutesThreshold * 60))
            
            query = """SELECT max(timeStampFetch) FROM prices WHERE itemID = ?"""
            param.append(kwargs['itemID'])

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
        if 'itemID' in kwargs.keys():
            # if not defined, set Eve-Central as default data source
            if not 'marketDataSource' in kwargs.keys():
                kwargs['marketDataSource'] = 'Eve-Central'

            newDataObtained = False
    
            if kwargs['marketDataSource'] == 'Eve-Central':
                if self.fetchOrdersFromEveCentral(**kwargs):
                    newDataObtained = True
            elif kwargs['marketDataSource'] == 'Eve-MarketData':
                pass
#                 if self.fetchOrdersFromEveMarketData(**kwargs):
#                     newDataObtained = True

            if newDataObtained:
                # if we have some new data, delete all older
                print "Cleaning up old market orders"
                self.deleteOrdersOlderThanMinutes(**kwargs)
            
    def getMinSellOrderPrice(self, **kwargs):
        '''
        Get sell order with minimum price
        '''

        if 'itemID' in kwargs.keys():
            param = []
            param.append(kwargs['itemID'])

            # only update data if DB entries got older than threshold
            if self.areOrdersTooOld(**kwargs):
                print "Old data detected, fetching current orders..."
                self.fetchOrders(**kwargs)
                
            query = """SELECT min(price) FROM prices WHERE orderType = 'sell_orders' AND itemID = ?"""
             
            if 'regionID' in kwargs.keys():
                query += """ AND regionID = ?"""
                param.append(kwargs['regionID'])
            if 'stationID' in kwargs.keys():
                query += """ AND stationID = ?"""
                param.append(kwargs['stationID'])
            if 'stationName' in kwargs.keys():
                query += """ AND stationName = ?"""
                param.append(kwargs['stationName'])
            if 'orderType' in kwargs.keys():
                query += """ AND orderType = ?"""
                param.append(kwargs['orderType'])
                        
        result = self.execQuery(query, param)[0][0]
        return result

    def getMaxBuyOrderPrice(self, **kwargs):
        '''
        Get buy order with maximum price
        '''
        if 'itemID' in kwargs.keys():
            param = []
            param.append(kwargs['itemID'])

            # only update data if DB entries got older than threshold
            if self.areOrdersTooOld(**kwargs):
                print "Old data detected, fetching current orders..."
                self.fetchOrders(**kwargs)
    
            query = """SELECT max(price) FROM prices WHERE orderType = 'buy_orders' AND itemID = ?"""
             
            if 'regionID' in kwargs.keys():
                query += """ AND regionID = ?"""
                param.append(kwargs['regionID'])
            if 'stationID' in kwargs.keys():
                query += """ AND stationID = ?"""
                param.append(kwargs['stationID'])
            if 'stationName' in kwargs.keys():
                query += """ AND stationName = ?"""
                param.append(kwargs['stationName'])
            if 'orderType' in kwargs.keys():
                query += """ AND orderType = ?"""
                param.append(kwargs['orderType'])


        result = self.execQuery(query,param)[0][0]
        return result

    def getOrders(self, **kwargs):
        '''
        Get market orders. If older, get new list from external source 
        '''
        if 'itemID' in kwargs.keys():
            param = []
            param.append(kwargs['itemID'])

            # only update data if DB entries got older than threshold
            if self.areOrdersTooOld(**kwargs):
                print "Old data detected, fetching current orders..."
                self.fetchOrders(**kwargs)
            
            query = """SELECT * FROM prices WHERE itemID = ?"""
             
            if 'regionID' in kwargs.keys():
                query += """ AND regionID = ?"""
                param.append(kwargs['regionID'])
            if 'stationID' in kwargs.keys():
                query += """ AND stationID = ?"""
                param.append(kwargs['stationID'])
            if 'stationName' in kwargs.keys():
                query += """ AND stationName = ?"""
                param.append(kwargs['stationName'])
            if 'orderType' in kwargs.keys():
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
    pass
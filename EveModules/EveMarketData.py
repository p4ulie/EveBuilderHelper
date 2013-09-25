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

class EveMarketData(object):
    '''
    Class for Eve Market data fetching and storing 
    '''

    DB = ''
    
    def execQuery(self, query):
        '''
        Main method for accessing the DB
        '''
        dbcon = ''
        
        try:
            dbcon = lite.connect(self.DB)
            cur = dbcon.cursor()
            cur.execute(query)
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
        for line in result:
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
                            values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')
            """ % (line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8], line[9], line[10], line[11], kwargs['orderType'], ts)
            data = self.execQuery(query)
        data = self.execQuery('commit')
            
#        self.con.commit()
        
        return result

    def deleteAllOrders(self):
        query = """DELETE FROM prices"""
        self.execQuery(query)
        
    def deleteOlderThan(self, minutes=OLDER_THAN_MINUTES_DEFAULT):
        ts = time.time()
        olderThanMinutes = ts - (minutes * 60)
        query = """DELETE FROM prices WHERE timeStampFetch < %s""" % olderThanMinutes
        self.execQuery(query)

    def areThereOrderOlderThanMinutes(self, **kwargs):
        if 'itemID' in kwargs:
            ts = time.time()
            olderThanMinutes = math.floor(ts - (kwargs['ifOlderThanMinutes'] * 60))
#            query = """SELECT * FROM prices WHERE itemID = %s AND max(timeStampFetch) < %s""" % (kwargs['itemID'], olderThanMinutes)
            query = """SELECT max(timeStampFetch) FROM prices WHERE itemID = %s""" % (kwargs['itemID'])
            data = self.execQuery(query)[0][0]

            if data < olderThanMinutes:
                return True
            else:
                return False
        return False
    
    def fetchOrders(self, **kwargs):
        '''
        Fetch data from various Market pages (Eve-Central, Eve market Data, ...)  
        '''
        
        # only update data if DB entries got older than ifOlderThanMinutes
        if self.areThereOrderOlderThanMinutes(**kwargs):
            # if not defined, set Eve-Central as default data source
            if not 'marketDataSource' in kwargs:
                kwargs['marketDataSource'] = 'EveCentral'
            if kwargs['marketDataSource'] == 'EveCentral':
                if self.fetchOrdersFromEveCentral(**kwargs):
                    # if we have some new data, delete all older
                    self.deleteOlderThan(kwargs['ifOlderThanMinutes'])


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

    emd = EveMarketData()
#    emd.deleteOlderThan(OLDER_THAN_MINUTES_DEFAULT)
    emd.deleteOlderThan(0)
    
    print "Fetching orders..."
    emd.fetchOrders(itemID = Tritanium_ID, orderType = 'sell_orders', ifOlderThanMinutes = OLDER_THAN_MINUTES_DEFAULT)
    print "Done"
    
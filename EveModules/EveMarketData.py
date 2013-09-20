'''
Class for Eve Market data fetching and storing 
Using sqlite as storage

Created on 12.9.2013

@author: PA
'''

import sqlite3
import time
from EveModules.EveCentral import *

OLDER_THAN_MINUTES_DEFAULT = 60

defaultDBFile = 'marketdata.db'
marketDataSources = ('EveCentral')

class EveMarketData(object):
    '''
    Class for Eve Market data fetching and storing 
    '''
    
    def fetchOrdersFromEveCentral(self, **kwargs):
        '''
        Fetch data from Eve-Central  
        '''

        ec = EveCentral()
        result = ec.quicklookGetList(**kwargs)

        ts = time.time()
        for line in result:
            self.cur.execute("""INSERT INTO prices
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
            """, (line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7],
                  line[8], line[9], line[10], line[11], kwargs['orderType'], ts)
            )
        self.con.commit()
        
        return result

    def deleteAllOrders(self):
        self.cur.execute("""DELETE FROM prices""")
        self.con.commit()
        
    def deleteOlderThan(self, minutes=OLDER_THAN_MINUTES_DEFAULT):
        ts = time.time()
        olderThanMinutes = ts - (minutes * 60)
        self.cur.execute("""DELETE FROM prices WHERE timeStampFetch < ?""", (olderThanMinutes,))
        self.con.commit()

    def areThereOrderOlderThanMinutes(self, **kwargs):
        if 'itemID' in kwargs:
            ts = time.time()
            olderThanMinutes = ts - (kwargs['ifOlderThanMinutes'] * 60)
            self.cur.execute("""SELECT count(*) FROM prices WHERE itemID = ? AND timeStampFetch < ?""", (kwargs['itemID'], olderThanMinutes))
            result = self.cur.fetchone()[0]
            if result > 0:
                return True
            else:
                return False
        return False
    
    def fetchOrders(self, **kwargs):
        '''
        Fetch data from various Market pages (Eve-Central, Eve market Data, ...)  
        '''
        
        # only update data if DB entries got older than ifOlderThanMinutes
        if not self.areThereOrderOlderThanMinutes(**kwargs):
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
        self.con = sqlite3.connect(dbFile)
        self.con.text_factory = str
        self.cur = self.con.cursor()
        self.cur.executescript("""
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
            """)
        self.con.commit()
    
if __name__ == '__main__':
    Tritanium_ID = 34
    Strong_Blue_Pill_Booster_ID = 10156

    emd = EveMarketData()
    emd.deleteOlderThan(OLDER_THAN_MINUTES_DEFAULT)
    emd.fetchOrders(itemID = Strong_Blue_Pill_Booster_ID, orderType = 'sell_orders', ifOlderThanMinutes = OLDER_THAN_MINUTES_DEFAULT)

    
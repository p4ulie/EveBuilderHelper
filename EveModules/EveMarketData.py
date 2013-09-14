'''
Class for Eve Market data fetching and storing 
Using sqlite as storage

Created on 12.9.2013

@author: PA
'''

import sqlite3
import time
from EveModules.EveCentral import *

defaultDBFile = 'marketdata.db'
marketDataSources = ('EveCentral')

class EveMarketData(object):
    '''
    Class for Eve Market data fetching and storing 
    '''
    
    def fetchOrdersEveCentral(self, itemID, regionLimit='', orderType='sell_orders'):
        '''
        Fetch data from Eve-Central  
        '''

        ec = EveCentral()
        result = ec.quicklookGetList(itemID, regionLimit=regionLimit, orderType=orderType)
        return result

    def fetchOrders(self, itemID='', regionLimit='', orderType='sell_orders', marketDataSource='EveCentral'):
        '''
        Fetch data from various Market pages (Eve-Central, Eve market Data, ...)  
        '''

        if marketDataSource == 'EveCentral':
            result = self.fetchOrdersEveCentral(itemID, regionLimit=regionLimit, orderType=orderType)

        for line in result:
            print format(line)
            ts = time.time()
            print ts
#             self.cur.execute("""INSERT INTO prices
#                             (itemID,
#                             itemName,
#                             regionID,
#                             stationID,
#                             stationName,
#                             security,
#                             range,
#                             price,
#                             volRemain,
#                             minVolume,
#                             expires,
#                             reportedTime,
#                             orderType,
#                             jitaBuyMax)
#                             values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'sell', ?)
#             """, (line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7],
#                   line[8], line[9], line[10], line[11], priceJitaBuyMax)
#             )

    def __init__(self, dbFile=defaultDBFile):
        '''
        Create a DB connection
        '''
#        self.con = sqlite3.connect(":memory:")
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
                jitaBuyMax real,
                timeStampFetch integer
            );
            """)
        self.con.commit()
    
if __name__ == '__main__':
    emd = EveMarketData()
    
    TritaniumID = 34
    emd.fetchOrders(itemID = TritaniumID)
    
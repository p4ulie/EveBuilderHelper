'''
Classes for accessing Eve Online data dump DB

Created on 8.7.2012

@author: Pavol Antalik
'''

import sys
import sqlite3 as lite


class EveDB(object):
    '''
    Base class for interacting with Eve Online data dump Sqlite DB
    '''

    DB = ''

    def fetchData(self, query):
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

    def __init__(self, DB):
        '''
        Constructor
        '''
        self.DB = DB

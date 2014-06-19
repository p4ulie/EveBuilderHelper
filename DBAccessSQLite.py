'''
Created on 18.6.2014

@author: Pavol Antalik
'''

import sys
import sqlite3 as sqlite

class DBAccessSQLite(object):
    '''
    Class for accessing SQlite database
    '''

    def __init__(self, DB):
        '''
        Constructor
        '''
        self.DB = DB

    def fetchData(self, query):
        '''
        Main method for accessing the DB
        '''
        dbcon = ''
        
        try:
            dbcon = sqlite.connect(self.DB)
            cur = dbcon.cursor()
            cur.execute(query)
            rows = cur.fetchall()
        except sqlite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)
        finally:
            if dbcon:
                dbcon.close()
    
        return rows
    

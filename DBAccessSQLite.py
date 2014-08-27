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

    DB = None
    cur = None
    dbcon = None
    
    def __init__(self, DB):
        '''
        Constructor
        '''
        self.DB = DB
        self.connect()
        
    def connect(self):
        '''
        Connect to database
        '''
        try:
            self.dbcon = sqlite.connect(self.DB)
            self.dbcon.text_factory = str
            self.cur = self.dbcon.cursor()
        except sqlite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)
        
    def close(self):
        '''
        Close database connection
        '''
        if self.dbcon:
            self.dbcon.close()

    def fetchData(self, query, *args):
        '''
        Main method for accessing the DB
        '''
        try:
            self.cur.execute(query, args)
            rows = self.cur.fetchall()
        except sqlite.Error, e:
            print "Error %s:" % e.args[0]
            self.close()
            sys.exit(1)
    
        return rows
    

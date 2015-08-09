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

    data_file = None
    cur = None
    dbcon = None

    def __init__(self, db):
        '''
        Constructor
        '''
        self.datafile = db
        self.connect()

    def connect(self):
        '''
        Connect to database
        '''
        try:
            self.dbcon = sqlite.connect(self.datafile)
            self.dbcon.text_factory = str
            self.cur = self.dbcon.cursor()
        except sqlite.Error, error:
            print "Error %s:" % error.args[0]
            sys.exit(1)

    def close(self):
        '''
        Close database connection
        '''
        if self.dbcon:
            self.dbcon.close()

    def fetch_data(self, query, *args):
        '''
        Main method for accessing the DB
        '''
        try:
            self.cur.execute(query, args)
            rows = self.cur.fetchall()
        except sqlite.Error, error:
            print "Error %s:" % error.args[0]
            self.close()
            sys.exit(1)

        return rows

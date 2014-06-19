'''
Classes for accessing Eve Online data dump DB

Created on 8.7.2012

@author: Pavol Antalik
'''

import sys
import sqlite3 as lite

from Config import *

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

    def getItemsList(self, groupID=''):
        '''
        Get list of items, possibly from specific group
        '''
        if groupID != '':
            query = """
                        SELECT *
                        FROM invTypes AS t
                        WHERE t.published = '1'
                        AND t.groupID = '%s'
                    """ % groupID
        else:
            query = """
                        SELECT *
                        FROM invTypes AS t
                        WHERE t.published = '1'
                    """
        data = self.fetchData(query)
        return data

    def getCategoriesList(self):
        '''
        Get list of categories
        '''
        query = """
                    SELECT c.categoryID, c.categoryName, c.description
                    FROM invCategories AS c
                    WHERE c.published = 1
                """
        data = self.fetchData(query)
        return data

    def getGroupsList(self, categoryID=''):
        '''
        Get list of groups
        '''
        if categoryID is '':
            query = """
                        SELECT g.groupID, g.categoryID, g.groupName, g.description
                        FROM invGroups AS g
                        WHERE g.published = '1'
                    """
        else:
            query = """
                        SELECT g.groupID, g.categoryID, g.groupName, g.description
                        FROM invGroups AS g
                        WHERE g.published = '1'
                        and g.categoryID = '%s'
                    """ % categoryID
        data = self.fetchData(query)
        return data

    def __init__(self, DB):
        '''
        Constructor
        '''
        self.DB = DB

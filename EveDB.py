'''
Classes for accessing Eve Online data dump DB

Created on 8.7.2012

@author: PA
'''

import sys
import sqlite3 as lite


class EveDB(object):
    '''
    Base class for interacting with EveDB
    '''

    DB = ''

    def fetchData(self, query):
        '''
        Main method for accessing the DB
        '''
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




class EveSolarSystem(EveDB):
    '''
    Class for Solar System data reading
    '''

    regionID = ''
    constellationID = ''
    solarSystemID = ''
    solarSystemName = ''

    def __getSolarSystemData(self, solarSystemID=0, solarSystemName=''):
        '''
        Get item data from ID (preferred) or name
        '''

        if solarSystemID != 0:
            query = """
                        SELECT *
                        FROM mapSolarSystems AS s
                        WHERE s.solarSystemID = '%s'
                    """ % solarSystemID
        else:
            query = """
                        SELECT *
                        FROM mapSolarSystems AS s
                        WHERE s.solarSystemName = '%s'
                    """ % solarSystemName

        data = self.fetchData(query)
        self.regionID = data[0][0]
        self.constellationID = data[0][1]
        self.solarSystemID = data[0][2]
        self.solarSystemName = data[0][3]

    def __init__(self, DB, solarSystemID=0, solarSystemName=''):
        '''
        Constructor, initial data load
        '''
        self.DB = DB
        self.__getSolarSystemData(solarSystemID, solarSystemName)

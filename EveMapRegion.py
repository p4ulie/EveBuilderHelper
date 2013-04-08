'''
Created on 7.4.2013

@author: Pavol Antalik
'''

from EveDB import EveDB


class EveMapRegion(EveDB):
    '''
    Class for Map Region data reading
    '''

    regionID = ''
    regionName = ''

    def __getMapRegion(self, query):
        '''
        Get Map Region data
        '''

        data = self.fetchData(query)
        if data:
            self.regionID = data[0][0]
            self.regionName = data[0][1]

    def getMapRegionByID(self, regionID=''):
        '''
        Get Map Region data by ID
        '''

        if regionID != '':
            query = """
                        SELECT *
                        FROM mapRegions AS r
                        WHERE r.regionID = '%s'
                    """ % regionID
            self.__getMapRegion(query)

    def getMapRegionByName(self, regionName=''):
        '''
        Get Map Region data by name
        '''

        if regionName != '':
            query = """
                        SELECT *
                        FROM mapRegions AS r
                        WHERE r.regionName = '%s'
                    """ % regionName
            self.__getMapRegion(query)

    def __init__(self, DB, regionID='', regionName=''):
        '''
        Constructor, initial data load
        '''
        self.DB = DB

        if regionID != '':
            self.getMapRegionByID(regionID)
        else:
            if regionName != '':
                self.getMapRegionByName(regionName)

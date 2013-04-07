'''
Created on 7.4.2013

@author: Pavol Antalik
'''

import EveDB


class EveRegion(EveDB):
    '''
    Class for Region data reading
    '''

    regionID = ''
    regionName = ''

    def __getRegionData(self, regionID='', regionName=''):
        '''
        Get item data from ID (preferred) or name
        '''

        if regionID != 0:
            query = """
                        SELECT *
                        FROM mapRegions AS r
                        WHERE r.regionID = '%s'
                    """ % regionID
        else:
            query = """
                        SELECT *
                        FROM mapRegions AS r
                        WHERE r.regionName = '%s'
                    """ % regionName

        data = self.fetchData(query)
        self.regionID = data[0][0]
        self.regionName = data[0][1]

    def __init__(self, DB, regionID='', regionName=''):
        '''
        Constructor, initial data load
        '''
        self.DB = DB
        self.__getRegionData(regionID, regionName)

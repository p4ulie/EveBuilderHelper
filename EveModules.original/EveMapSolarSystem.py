'''
Created on 7.4.2013

@author: Pavol Antalik
'''

from EveDB import EveDB


class EveMapSolarSystem(EveDB):
    '''
    Class for Map Region data reading
    '''

    regionID = ''
    constellationID = ''
    solarSystemID = ''
    solarSystemName = ''

    def __getMapSolarSystem(self, query):
        '''
        Get Map Region data
        '''

        data = self.fetchData(query)
        if data:
            self.regionID = data[0][0]
            self.constellationID = data[0][1]
            self.solarSystemID = data[0][2]
            self.solarSystemName = data[0][3]

    def getMapSolarSystemByID(self, solarSystemID=''):
        '''
        Get item data by ID
        '''

        if solarSystemID != '':
            query = """
                        SELECT *
                        FROM mapSolarSystems AS s
                        WHERE s.solarSystemID = '%s'
                    """ % solarSystemID
            self.__getMapSolarSystem(query)

    def getMapSolarSystemByName(self, solarSystemName=''):
        '''
        Get item data by Name
        '''

        if solarSystemName != '':
            query = """
                        SELECT *
                        FROM mapSolarSystems AS s
                        WHERE s.solarSystemName = '%s'
                    """ % solarSystemName
            self.__getMapSolarSystem(query)

    def __init__(self, DB, solarSystemID='', solarSystemName=''):
        '''
        Constructor, initial data load
        '''
        self.DB = DB

        if solarSystemID != '':
            self.getMapSolarSystemByID(solarSystemID)
        else:
            if solarSystemName != '':
                self.getMapSolarSystemByName(solarSystemName)

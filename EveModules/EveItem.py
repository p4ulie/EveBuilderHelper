'''
Created on 7.4.2013

@author: Pavol Antalik
'''

from EveDB import EveDB
from EveBlueprint import EveBlueprint


class EveItem(EveDB):
    '''
    Class for Item data reading and handling
    '''

    itemID = ''
    groupID = ''
    name = ''
    description = ''
    graphicID = ''
    radius = ''
    mass = ''
    volume = ''
    capacity = ''
    portionSize = ''
    raceID = ''
    basePrice = ''
    published = ''
    marketGroupID = ''
    chanceOfDuplicating = ''

    def __getItem(self, query):
        '''
        Get invType data from DB
        '''
        data = self.fetchData(query)
        if data:
            self.itemID = data[0][0]
            self.groupID = data[0][1]
            self.name = data[0][2]
            self.description = data[0][3]
            self.mass = data[0][4]
            self.volume = data[0][5]
            self.capacity = data[0][6]
            self.portionSize = data[0][7]
            self.raceID = data[0][8]
            self.basePrice = data[0][9]
            self.published = data[0][10]
            self.marketGroupID = data[0][11]
            self.chanceOfDuplicating = data[0][12]

    def getItemByID(self, itemID=''):
        '''
        Get InvType data by ID
        '''
        if itemID != '':
            query = """
                        SELECT *
                        FROM invTypes AS t
                        WHERE t.typeID = '%s'
                    """ % itemID
            self.__getItem(query)

    def getItemByName(self, name=''):
        '''
        Get InvType data by Name
        '''
        if name != '':
            query = """
                        SELECT *
                        FROM invTypes AS t
                        WHERE t.typeName = '%s'
                    """ % name
            self.__getItem(query)

    def getItems(self, groupID=''):
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

    def getBlueprintID(self):
        '''
        Get blueprintID for this item, if it exists
        '''
        query = """
                    SELECT blueprintTypeID
                    FROM invBlueprintTypes AS b
                    WHERE b.productTypeID = %s
                """ % self.itemID
        data = self.fetchData(query)[0]
        return data

    def getBlueprintObject(self):
        '''
        Get blueprintID for this item, if it exists
        create and return an instance of EveBlueprint class
        '''
        blueprint = EveBlueprint(self.DB, blueprintID = self.getBlueprintID())
        return blueprint

    def __init__(self, DB, itemID='', name=''):
        '''
        Constructor, initial data load
        '''
        self.DB = DB

        if itemID != '':
            self.getItemByID(itemID)
        else:
            if name != '':
                self.getItemByName(name)

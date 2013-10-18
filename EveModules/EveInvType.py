'''
Created on 7.4.2013

@author: Pavol Antalik
'''

from EveDB import EveDB

class EveInvType(EveDB):
    '''
    Class for Item data reading and handling
    '''

    typeID = None
    groupID = None
    name = ''
    description = ''
    graphicID = None
    radius = None
    mass = None
    volume = None
    capacity = None
    portionSize = None
    raceID = None
    basePrice = None
    published = None
    marketGroupID = None
    chanceOfDuplicating = None

    def __getItem(self, query):
        '''
        Get invType data from DB
        '''
        data = self.fetchData(query)
        if data:
            self.typeID = data[0][0]
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

    def getMetaGroup(self):
        '''
        Check real meta type of item
        '''
        metaType = 1
        
        if self.typeID:        
            query = """
                    SELECT *
                    FROM invMetaTypes AS m
                    WHERE m.typeID = %s
                """ % self.typeID
    
            result = self.fetchData(query)

            if result:
                metaType = result[0][2]

        return metaType

    def getBlueprintID(self):
        '''
        Get blueprintID for this item, if it exists
        '''
        query = """
                    SELECT blueprintTypeID
                    FROM invBlueprintTypes AS b
                    WHERE b.productTypeID = %s
                """ % self.typeID
        result = self.fetchData(query)

        if result:
            data = result[0] 
        else:
            data = None

        return data

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

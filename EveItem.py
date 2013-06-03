'''
Created on 7.4.2013

@author: Pavol Antalik
'''

from EveDB import EveDB


class EveItem(EveDB):
    '''
    Class for Item data reading and handling
    '''

    typeID = ''
    groupID = ''
    typeName = ''
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
            self.typeID = data[0][0]
            self.groupID = data[0][1]
            self.typeName = data[0][2]
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

    def getItemByID(self, typeID=''):
        '''
        Get InvType data by ID
        '''

        if typeID != '':
            query = """
                        SELECT *
                        FROM invTypes AS t
                        WHERE t.typeID = '%s'
                    """ % typeID
            self.__getItem(query)

    def getItemByName(self, typeName=''):
        '''
        Get InvType data by Name
        '''

        if typeName != '':
            query = """
                        SELECT *
                        FROM invTypes AS t
                        WHERE t.typeName = '%s'
                    """ % typeName
            self.__getItem(query)

    def getBaseMaterialList(self):
        '''
        Get base list of materials for InvType,
        equals amount of materials when recycling item
        (list of lists - [ID, quantity])
        '''
        query = """
                    SELECT t.typeID, m.quantity
                    FROM invTypeMaterials AS m
                     INNER JOIN invTypes AS t
                      ON m.materialTypeID = t.typeID
                    WHERE m.typeID = %s
                """ % self.typeID
        data = self.fetchData(query)
        return data

    def getBlueprintTypeID(self):
        '''
        Get blueprintID for this item, if it exists
        '''
        query = """
                    SELECT blueprintTypeID
                    FROM invBlueprintTypes AS b
                    WHERE b.productTypeID = %s
                """ % self.typeID
        data = self.fetchData(query)
        return data

    def __init__(self, DB, typeID='', typeName=''):
        '''
        Constructor, initial data load
        '''
        self.DB = DB

        if typeID != '':
            self.getItemByID(typeID)
        else:
            if typeName != '':
                self.getItemByName(typeName)

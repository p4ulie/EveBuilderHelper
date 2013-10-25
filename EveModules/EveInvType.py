'''
Created on 7.4.2013

@author: Pavol Antalik
'''

from EveDB import EveDB

class EveInvType(EveDB):
    '''
    Class for Item data reading and handling
    '''

    __typeID = None
    __groupID = None
    __typeName = ''
    __description = ''
    __graphicID = None
    __radius = None
    __mass = None
    __volume = None
    __capacity = None
    __portionSize = None
    __raceID = None
    __basePrice = None
    __published = None
    __marketGroupID = None
    __chanceOfDuplicating = None

    __metaGroup = None
    __blueprintTypeID = None

    def __loadItem(self, query):
        '''
        Get invType data from DB
        '''
        data = self.fetchData(query)
        if data:
            self.__typeID = data[0][0]
            self.__groupID = data[0][1]
            self.__typeName = data[0][2]
            self.__description = data[0][3]
            self.__mass = data[0][4]
            self.__volume = data[0][5]
            self.__capacity = data[0][6]
            self.__portionSize = data[0][7]
            self.__raceID = data[0][8]
            self.__basePrice = data[0][9]
            self.__published = data[0][10]
            self.__marketGroupID = data[0][11]
            self.__chanceOfDuplicating = data[0][12]
            
            self.__metaGroup = self.loadMetaGroup()
            self.__blueprintTypeID = self.loadBlueprintTypeID()

    def loadItemByID(self, typeID=''):
        '''
        Get InvType data by ID
        '''
        if typeID != '':
            query = """
                        SELECT *
                        FROM invTypes AS t
                        WHERE t.typeID = '%s'
                    """ % typeID
            self.__loadItem(query)

    def loadItemByName(self, name=''):
        '''
        Get InvType data by Name
        '''
        if name != '':
            query = """
                        SELECT *
                        FROM invTypes AS t
                        WHERE t.typeName = '%s'
                    """ % name
            self.__loadItem(query)

    def loadMetaGroup(self):
        '''
        Check real meta type of item
        '''
        metaType = 1
        
        if self.__typeID:        
            query = """
                    SELECT *
                    FROM invMetaTypes AS m
                    WHERE m.typeID = %s
                """ % self.__typeID
    
            result = self.fetchData(query)

            if result:
                metaType = result[0][2]

        return metaType

    def loadBlueprintTypeID(self):
        '''
        Get blueprintID for this item, if it exists
        '''
        query = """
                    SELECT blueprintTypeID
                    FROM invBlueprintTypes AS b
                    WHERE b.productTypeID = %s
                """ % self.__typeID
        result = self.fetchData(query)

        if result:
            data = result[0] 
        else:
            data = None

        return data

    def getTypeID(self):
        '''
        Return typeID
        '''
        return self.__typeID     

    def getTypeName(self):
        '''
        Return typeName
        '''
        return self.__typeName     
    
    def __init__(self, DB, typeID='', name=''):
        '''
        Constructor, initial data load
        '''
        self.DB = DB

        if typeID != '':
            self.loadItemByID(typeID)
        else:
            if name != '':
                self.loadItemByName(name)

'''
Created on 18.6.2014

@author: Pavol Antalik
'''

from EveDB import EveDB

class EveItem(EveDB):
    '''
    Class for containing item specific data and methods
    '''

    def __init__(self,
                 dbAccessObj,
                 typeID = None,
                 typeName = None):
        '''
        Constructor
        '''

        self.__dbAccessObj = dbAccessObj

        EveDB.__init__(self, self.__dbAccessObj)

        data = self.getInvItem(typeID, typeName)
        
        if data:
            self.typeID = data[0]
            self.groupID = data[1]
            self.typeName = data[2]
            self.description = data[3]
            self.mass = data[4]
            self.volume = data[5]
            self.capacity = data[6]
            self.portionSize = data[7]
            self.raceID = data[8]
            self.basePrice = data[9]
            self.published = data[10]
            self.marketGroupID = data[11]
            self.chanceOfDuplicating = data[12]

            query = """
                    SELECT *
                    FROM invMetaTypes AS m
                    WHERE m.typeID = %s
                """ % self.typeID
            
            data = self.__dbAccessObj.fetchData(query)
            
            if data:
                self.metaGroup = data[0][2]
            else:
                self.metaGroup = None

            query = """
                        SELECT blueprintTypeID
                        FROM invBlueprintTypes AS b
                        WHERE b.productTypeID = %s
                    """ % self.typeID

            data = self.__dbAccessObj.fetchData(query)
            
            if data:
                self.blueprintTypeID = data[0][0]
            else:
                self.blueprintTypeID = None


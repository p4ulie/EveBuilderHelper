'''
Created on Sep 15, 2014

@author: paulie
'''


from EveModules.EveDB import EveDB


class EveItem(EveDB):
    '''
    Class for data and methods for Items in Eve Online
    '''

    typeID = None
    groupID = None
    typeName = ''
    description = ''
    mass = None
    volume = None
    capacity = None
    portionSize = None
    raceID = None
    basePrice = None
    marketGroupID = None

    graphicID = None
    radius = None
    published = None
    chanceOfDuplicating = None

    metaGroup = None
    blueprintTypeID = None

    def __init__(self, dbAccessObj, typeID=None, typeName=None):
        '''
        Constructor
        '''

        self.dbAccessObj = dbAccessObj

        self.getItem(typeID=typeID, typeName=typeName)

    def getItem(self, typeID=None, typeName=None):
        '''
        Get item by ID or name
        '''

        item = self.getInvItem(typeID=typeID, typeName=typeName)

        if item is not None:
            for n, v in item.iteritems():
                setattr(self, n, v)
            self.blueprintTypeID = self.getBlueprintIDForItem(typeID=self.typeID)
            result = self.typeID
        else:
            self.typeID = None
            self.groupID = None
            self.typeName = ''
            self.description = ''
            self.mass = None
            self.volume = None
            self.capacity = None
            self.portionSize = None
            self.raceID = None
            self.basePrice = None
            self.marketGroupID = None

            self.graphicID = None
            self.radius = None
            self.published = None
            self.chanceOfDuplicating = None

            self.metaGroup = None
            self.blueprintTypeID = None

            result = None

        return result

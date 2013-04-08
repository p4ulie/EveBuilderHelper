'''
Created on 7.4.2013

@author: Pavol Antalik
'''

import EveDB


class EveInvType(EveDB):
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

    def __getInvType(self, query):
        '''
        Get invType data from DB
        '''
        data = self.fetchData(query)
        if data:
            self.typeID = data[0][0]
            self.groupID = data[0][1]
            self.typeName = data[0][2]
            self.description = data[0][3]
            self.graphicID = data[0][4]
            self.radius = data[0][5]
            self.mass = data[0][6]
            self.volume = data[0][7]
            self.capacity = data[0][8]
            self.portionSize = data[0][9]
            self.raceID = data[0][10]
            self.basePrice = data[0][11]
            self.published = data[0][12]
            self.marketGroupID = data[0][13]
            self.chanceOfDuplicating = data[0][14]

    def getInvTypeByID(self, typeID=''):
        '''
        Get InvType data by ID
        '''

        if typeID != '':
            query = """
                        SELECT *
                        FROM invTypes AS t
                        WHERE t.typeID = '%s'
                    """ % typeID
            self.__getInvType(query)

    def getInvTypeByName(self, typeName=''):
        '''
        Get InvType data by Name
        '''

        if typeName != '':
            query = """
                        SELECT *
                        FROM invTypes AS t
                        WHERE t.typeName = '%s'
                    """ % typeName
            self.__getInvType(query)

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

    def getExtraMaterialList(self):
        '''
        Get list of materials for InvType, inclusive R.A.M.
        (list of lists - [ID, quantity])
        '''

        query = """
                    SELECT r.requiredTypeID, r.quantity, r.damagePerJob
                    FROM ramTypeRequirements AS r
                     INNER JOIN invTypes AS t
                      ON r.requiredTypeID = t.typeID
                     INNER JOIN invGroups AS g
                      ON t.groupID = g.groupID
                    WHERE r.typeID = %s
                     AND r.activityID = 1
                     AND g.categoryID != 16;
                """ % self.blueprintTypeID
        data = self.fetchData(query)
        return data

    def __computeWasteFromMEResearchLevel(self, materialAmount, BlueprintMEResearchLevel):
        '''
        Compute waste for specific ME Blueprint Research level
        '''
        if BlueprintMEResearchLevel >= 0:
            waste = round(float(materialAmount) * (float(self.wasteFactor) / 100) * (1 / (float(BlueprintMEResearchLevel) + 1)))
        else:
            waste = round(float(materialAmount) * (float(self.wasteFactor) / 100) * (1 - float(BlueprintMEResearchLevel)))
        return int(waste)

    def __computeWasteFromPESkill(self, materialAmount, PESkillLevel):
        '''
        Compute waste for trained Production Efficiency skill level
        '''
        waste = round(((25 - (5 * float(PESkillLevel))) * float(materialAmount)) / 100)
        return int(waste)

    def getProduceMaterialIDList(self):
        '''
        Generate a list of materials for production,
        returns list of IDs only
        '''
        materialList = []
        materialRecycleList = self.getBaseMaterialList()
        for material in materialRecycleList:
            materialID = material[0]
            materialList.append(materialID)
        return materialList

    def getManufacturingMaterialAmountList(self, ME=0, PE=0):
        '''
        Generate a list of materials for production, IDs and quantities,
        waste is added from researched blueprint ME amount and PE skill level
        '''
        materialList = []
        materialBaseList = self.getBaseMaterialList()
        materialExtraList = self.getExtraMaterialList()
        for material in materialBaseList:
            materialID = material[0]
            wasteME = self.__computeWasteFromMEResearchLevel(material[1], ME)
            wastePE = self.__computeWasteFromPESkill(material[1], PE)
            materialQuantity = material[1] + wasteME + wastePE
            materialList.append([materialID, materialQuantity])
        for material in materialExtraList:
            materialID = material[0]
            materialQuantity = material[1]
            materialList.append([materialID, materialQuantity])
        return materialList

    def getInvTypesList(self, groupID=''):
        '''
        Get list of invTypes, possibly limit it for specific invGroup
        '''
        if groupID is '':
            query = """
                        SELECT t.typeID, t.groupID, t.typeName, t.description
                        FROM invTypes AS t
                        WHERE t.published = '1'
                    """
        else:
            query = """
                        SELECT t.typeID, t.groupID, t.typeName, t.description
                        FROM invTypes AS t
                        WHERE t.published = '1'
                        and t.groupID = '%s'
                    """ % groupID
        data = self.fetchData(query)
        return data

    def __init__(self, DB, typeID='', typeName=''):
        '''
        Constructor, initial data load
        '''

        self.DB = DB

        if typeID != '':
            self.getInvTypeByID(typeID)
        else:
            if typeName != '':
                self.getInvTypeByName(typeName)

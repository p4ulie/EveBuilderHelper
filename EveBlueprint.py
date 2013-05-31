'''
Created on 7.4.2013

@author: Pavol Antalik
'''

from EveDB import EveDB


class EveBlueprint(EveDB):
    '''
    Class for invBlueprintType data reading and handling
    '''

    blueprintTypeID = ''
    parentBlueprintTypeID = ''
    productTypeID = ''
    productionTime = ''
    techLevel = ''
    researchProductivityTime = ''
    researchMaterialTime = ''
    researchCopyTime = ''
    researchTechTime = ''
    productivityModifier = ''
    materialModifier = ''
    wasteFactor = ''
    maxProductionLimit = ''

    # Researched levels of ME and PE
    researchLevelME = 0
    researchLevelPE = 0
    
    def __getBlueprint(self, query):
        '''
        Get invBlueprintType data from DB
        '''

        data = self.fetchData(query)
        if data:
            self.blueprintTypeID = data[0][0]
            self.parentBlueprintTypeID = data[0][1]
            self.productTypeID = data[0][2]
            self.productionTime = data[0][3]
            self.techLevel = data[0][4]
            self.researchProductivityTime = data[0][5]
            self.researchMaterialTime = data[0][6]
            self.researchCopyTime = data[0][7]
            self.researchTechTime = data[0][8]
            self.productivityModifier = data[0][9]
            self.materialModifier = data[0][10]
            self.wasteFactor = data[0][11]
            self.maxProductionLimit = data[0][12]

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
                """ % self.productTypeID
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

    def getManufacturingMaterials(self, characterSkillLevelME=0):
        '''
        Generate a list of materials for production, IDs and quantities,
        waste is added from researched blueprint ME amount and PE skill level
        '''
        materialList = []
        materialBaseList = self.getBaseMaterialList()
        materialExtraList = self.getExtraMaterialList()
        for material in materialBaseList:
            materialID = material[0]
            wasteME = self.__computeWasteFromResearchLevelME(material[1])
            wastePE = self.__computeWasteFromCharacterSkillLevelPE(material[1], characterSkillLevelME)
            materialQuantity = material[1] + wasteME + wastePE
            materialList.append([materialID, materialQuantity])
        for material in materialExtraList:
            materialID = material[0]
            materialQuantity = material[1]
            materialList.append([materialID, materialQuantity])
        return materialList

    def __computeWasteFromResearchLevelME(self, materialAmount):
        '''
        Compute waste for specific ME Blueprint Research level
        '''
        if self.researchLevelME >= 0:
            waste = round(float(materialAmount) * (float(self.wasteFactor) / 100) * (1 / (float(self.researchLevelME) + 1)))
        else:
            waste = round(float(materialAmount) * (float(self.wasteFactor) / 100) * (1 - float(self.researchLevelME)))
        return int(waste)

    def __computeWasteFromCharacterSkillLevelPE(self, materialAmount, PESkillLevel):
        '''
        Compute waste for trained Production Efficiency skill level
        '''
        waste = round(((25 - (5 * float(PESkillLevel))) * float(materialAmount)) / 100)
        return int(waste)

    def __init__(self, DB, blueprintTypeID='', productTypeID = '', ResearchLevelME = 0, ResearchLevelPE = 0):
        '''
        Constructor, initial data load
        '''

        self.DB = DB

        if productTypeID != '':
            query = """
                        SELECT *
                        FROM invBlueprintTypes AS b
                        WHERE b.productTypeID = %s
                    """ % productTypeID

        if blueprintTypeID != '':
            query = """
                        SELECT *
                        FROM invBlueprintTypes AS b
                        WHERE b.blueprintTypeID = %s
                    """ % blueprintTypeID

        self.__getBlueprint(query)

        if ResearchLevelME != 0:
            self.researchLevelME = ResearchLevelME

        if ResearchLevelPE != 0:
            self.researchLevelPE = ResearchLevelPE

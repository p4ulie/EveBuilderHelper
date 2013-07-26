'''
Created on 7.4.2013

@author: Pavol Antalik
'''

from EveDB import EveDB

def addMaterialToList(materialList, material):
    '''
    Add specified amount of material (itemID, quantity) to materialList dictionary
    '''
   
    if material[0] in materialList:
        materialList[material[0]] = materialList[material[0]] + material[1]
    else: 
        materialList[material[0]] = material[1]

def substractMaterialFromList(materialList, material):
    '''
    Substract specified amount of material (itemID, quantity) from materialList dictionary
    '''

    if material[0] in materialList:
        if materialList[material[0]] > material[1]:
            materialList[material[0]] = materialList[material[0]] - material[1]
        else:
            del materialList[material[0]] 

class EveBlueprint(EveDB):
    '''
    Class for invBlueprintType data reading and handling
    '''

    blueprintID = ''
    parentBlueprintID = ''
    productID = ''
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
            self.blueprintID = data[0][0]
            self.parentBlueprintID = data[0][1]
            self.productID = data[0][2]
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

    def getBaseMaterialList(self, itemID = ''):
        '''
        Get base list of materials for InvType,
        equals amount of materials when recycling item
        (list of lists - [ID, quantity])
        '''

        if not itemID:
            itemID = self.productID 

        query = """
                    SELECT t.typeID, m.quantity
                    FROM invTypeMaterials AS m
                     INNER JOIN invTypes AS t
                      ON m.materialTypeID = t.typeID
                    WHERE m.typeID = %s
                """ % itemID

        data = self.fetchData(query)
        return data

    def getExtraMaterialList(self, blueprintID = ''):
        '''
        Get list of materials for InvType, inclusive R.A.M.
        (list of lists - [ID, quantity])
        '''

        if not blueprintID:
            blueprintID = self.blueprintID 

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
                """ % blueprintID

        data = self.fetchData(query)
        return data

    def getT1ItemForT2Blueprint(self, blueprintID = ''):
        '''
        Get ID of T1 item used in manufacturing of T2
        '''

        data = ''
        
        if self.techLevel == 2:
            if not blueprintID:
                blueprintID = self.blueprintID 

            query = """
                        select r.requiredTypeID from ramTypeRequirements as r
                        inner join invTypes as t on r.requiredTypeID = t.typeID
                        inner join invGroups as g on t.groupID = g.groupID
                        and r.activityID = 1
                        and g.categoryID != 16
                        and g.categoryID != 17
                        and r.typeID = %s;
                    """ % blueprintID

            data = self.fetchData(query)[0]

        return data

    def getManufacturingMaterials(self, characterSkillLevelME=0):
        '''
        Generate a list of materials for production, IDs and quantities,
        waste is added from researched blueprint ME amount and PE skill level
        '''
        materialList = {}
        materialBaseList = self.getBaseMaterialList()

        for material in materialBaseList:
            materialID = material[0]
            wasteME = self.__computeWasteFromResearchLevelME(material[1])
            wastePE = self.__computeWasteFromCharacterSkillLevelPE(material[1], characterSkillLevelME)
            materialQuantity = material[1] + wasteME + wastePE
            addMaterialToList(materialList, [materialID, materialQuantity])

        materialExtraList = self.getExtraMaterialList()
        for material in materialExtraList:
            addMaterialToList(materialList, material)

        if self.techLevel == 2:
            itemT1 = self.getT1ItemForT2Blueprint()
            materialT1List = self.getBaseMaterialList(itemT1)
            for material in materialT1List:
#                substractMaterialFromList(materialList, material)
                pass

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

    def __init__(self, DB, blueprintID = '', productID = '', ResearchLevelME = '', ResearchLevelPE = ''):
        '''
        Constructor, initial data load
        '''

        self.DB = DB

        query = ""

        if productID != '':
            query = """
                        SELECT *
                        FROM invBlueprintTypes AS b
                        WHERE b.productTypeID = %s
                    """ % productID

        if blueprintID != '':
            query = """
                        SELECT *
                        FROM invBlueprintTypes AS b
                        WHERE b.blueprintTypeID = %s
                    """ % blueprintID

        self.__getBlueprint(query)

        if ResearchLevelME:
            self.researchLevelME = ResearchLevelME
        elif self.techLevel == 2:
            self.researchLevelME = -4

        if ResearchLevelPE:
            self.researchLevelPE = ResearchLevelPE
        elif self.techLevel == 2:
            self.researchLevelPE = -4

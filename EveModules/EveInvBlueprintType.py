'''
Created on 7.4.2013

@author: Pavol Antalik
'''

from Config import *

from EveDB import EveDB

class EveInvBlueprintType(EveDB):
    '''
    Class for invBlueprintType data reading and handling
    '''

    blueprintTypeID = None
    parentBlueprintTypeID = None
    productTypeID = None
    productionTime = None
    techLevel = None
    researchProductivityTime = None
    researchMaterialTime = None
    researchCopyTime = None
    researchTechTime = None
    productivityModifier = None
    materialModifier = None
    wasteFactor = None
    maxProductionLimit = None
    portionSize = None # amount produced in 1 run

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

            query = """
                        SELECT portionSize
                        FROM invTypes AS t
                        WHERE t.typeID = '%s'
                    """ % self.productTypeID
            data = self.fetchData(query)
            if data:
                self.portionSize = data[0][0]

    def getBaseMaterialList(self, typeID = ''):
        '''
        Get base list of materials for InvType,
        equals amount of materials when recycling item
        (list of lists - [ID, quantity])
        '''

        if not typeID:
            typeID = self.productTypeID 

        query = """
                    SELECT t.typeID, m.quantity
                    FROM invTypeMaterials AS m
                     INNER JOIN invTypes AS t
                      ON m.materialTypeID = t.typeID
                    WHERE m.typeID = %s
                """ % typeID

        data = self.fetchData(query)
        return data

    def getExtraMaterialList(self, blueprintTypeID = ''):
        '''
        Get list of materials for InvType, inclusive R.A.M.
        (list of lists - [ID, quantity])
        '''

        if not blueprintTypeID:
            blueprintTypeID = self.blueprintTypeID 

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
                """ % blueprintTypeID

        data = self.fetchData(query)
        return data

    def __getT1ItemForT2Blueprint(self, blueprintID = ''):
        '''
        Get ID of T1 item used in manufacturing of T2
        '''

        data = ''
        
        if self.techLevel == 2:
            if not blueprintID:
                blueprintID = self.blueprintTypeID 

            query = """
                        select r.requiredTypeID from ramTypeRequirements as r
                        inner join invTypes as t on r.requiredTypeID = t.typeID
                        inner join invGroups as g on t.groupID = g.groupID
                        and r.activityID = 1
                        and g.categoryID != 16
                        and g.categoryID != 17
                        and r.typeID = %s;
                    """ % blueprintID

            result = self.fetchData(query)

            if result:
                data = result[0] 
            else:
                data = None

        return data

    def getManufacturingMaterialsList(self, skillPE=5):
        '''
        Generate a list of materials for production, IDs and quantities,
        waste is added from researched blueprint ME amount and PE skill level.
        Return the list of InvType objects
        '''

        def addMaterialToList(materialList, material):
            '''
            Add specified amount of material (typeID, quantity) to materialList dictionary
            '''
           
            if material[0] in materialList:
                materialList[material[0]] = materialList[material[0]] + material[1]
            else: 
                materialList[material[0]] = material[1]
        
        def subtractMaterialFromList(materialList, material):
            '''
            Substract specified amount of material (typeID, quantity) from materialList dictionary
            '''
        
            if material[0] in materialList:
                if materialList[material[0]] > material[1]:
                    materialList[material[0]] = materialList[material[0]] - material[1]
                else:
                    del materialList[material[0]] 
        
        materialList = {}
        materialBaseList = self.getBaseMaterialList()

        # Add base materials to material list
        for material in materialBaseList:
            addMaterialToList(materialList, material)

        # In case of T2 item, subtract materials of T1 item needed for manufacturing (Wolf - Rifter) 
        if self.techLevel == 2:
            itemT1 = self.__getT1ItemForT2Blueprint()
            if itemT1:
                materialT1List = self.getBaseMaterialList(itemT1)
                for material in materialT1List:
                    subtractMaterialFromList(materialList, material)

        # Compute and add waste to material list
        for materialID, quantity in materialList.iteritems():
            wasteME = self.__computeWasteFromResearchLevelME(quantity)
            wastePE = self.__computeWasteFromCharacterSkillLevelPE(quantity, skillPE)
            addMaterialToList(materialList, [materialID, wasteME + wastePE])

        materialExtraList = self.getExtraMaterialList()
        for material in materialExtraList:
            addMaterialToList(materialList, material)

        materialObjList = {}

        if materialList:
            for material,quantity in materialList.iteritems(): 
                materialObjList[material] = quantity

        return materialObjList

    def __computeWasteFromResearchLevelME(self, materialAmount):
        '''
        Compute waste for specific ME Blueprint Research level
        '''
        if self.researchLevelME >= 0:
            waste = round(float(materialAmount) * (float(self.wasteFactor) / 100) * (1 / (float(self.researchLevelME) + 1)))
        else:
            waste = round(float(materialAmount) * (float(self.wasteFactor) / 100) * (1 - float(self.researchLevelME)))
        return int(waste)

    def __computeWasteFromCharacterSkillLevelPE(self, materialAmount, skillPE):
        '''
        Compute waste for trained Production Efficiency skill level
        '''
        waste = round(((25 - (5 * float(skillPE))) * float(materialAmount)) / 100)
        return int(waste)

    def __init__(self, DB, blueprintTypeID = None, productID = None, ResearchLevelME = None, ResearchLevelPE = None):
        '''
        Constructor, initial data load
        '''

        self.DB = DB

        query = ""

        if productID :
            query = """
                        SELECT *
                        FROM invBlueprintTypes AS b
                        WHERE b.productTypeID = %s
                    """ % productID

        if blueprintTypeID:
            query = """
                        SELECT *
                        FROM invBlueprintTypes AS b
                        WHERE b.blueprintTypeID = %s
                    """ % blueprintTypeID

        if ResearchLevelME:
            self.researchLevelME = ResearchLevelME
        if ResearchLevelPE:
            self.researchLevelPE = ResearchLevelPE
        
        self.__getBlueprint(query)

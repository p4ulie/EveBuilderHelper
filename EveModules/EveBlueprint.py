'''
Created on 17.6.2014

@author: Pavol Antalik
'''

from EveDB import EveDB
import EveMath

class EveBlueprint(EveDB):
    '''
    Class for containing blueprint specific data and methods
    '''

    def __init__(self,
                 dbAccessObj,
                 blueprintTypeID = None,
                 productTypeID = None,
                 ResearchLevelME = None,
                 ResearchLevelTE = None):
        '''
        Constructor
        '''

        self.__dbAccessObj = dbAccessObj

        EveDB.__init__(self, self.__dbAccessObj)

        query = ''
        
        if blueprintTypeID:
            query = """
                        SELECT *
                        FROM invBlueprintTypes AS b
                        WHERE b.blueprintTypeID = %s
                    """ % blueprintTypeID
        else:
            if productTypeID:
                query = """
                            SELECT *
                            FROM invBlueprintTypes AS b
                            WHERE b.productTypeID = %s
                        """ % productTypeID


        if ResearchLevelME:
            self.researchLevelME = ResearchLevelME
        else:
            self.researchLevelME = 0

        if ResearchLevelTE:
            self.researchLevelTE = ResearchLevelTE
        else:
            self.researchLevelTE = 0

        data = self.__dbAccessObj.fetchData(query)

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

            data = self.__dbAccessObj.fetchData(query)
            if data:
                self.portionSize = data[0][0]

    def getListOfBaseMaterials(self):
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

        data = self.__dbAccessObj.fetchData(query)

        if data:
            data = dict((typeID, quantity) for (typeID, quantity) in data)

        return data

    def getListOfExtraMaterials(self):
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

        data = self.__dbAccessObj.fetchData(query)

        if data:
            data = dict((requiredTypeID, quantity) for (requiredTypeID, quantity, damagePerJob) in data)

        return data

    def getT1ItemForT2Blueprint(self):
        '''
        Get ID of T1 item used in manufacturing of T2
        '''
        
        if self.techLevel == 2:
            query = """
                        select r.requiredTypeID from ramTypeRequirements as r
                        inner join invTypes as t on r.requiredTypeID = t.typeID
                        inner join invGroups as g on t.groupID = g.groupID
                        and r.activityID = 1
                        and g.categoryID != 16
                        and g.categoryID != 17
                        and r.typeID = %s;
                    """ % self.blueprintTypeID

            result = self.__dbAccessObj.fetchData(query)

            if result:
                data = result[0] 
            else:
                data = None

        return data
 
    def getListOfManufacturingMaterials(self, characterTEskillLevel=0):
        '''
        Generate a list of materials for production, IDs and quantities,
        waste is added from researched blueprint ME amount and PE skill level.
        Return the list of InvType objects
        '''
        listOfTotalManufacturingMaterials = {}

        # add base materials to list        
        for material, quantity in self.getListOfBaseMaterials().iteritems():
            listOfTotalManufacturingMaterials[material] = listOfTotalManufacturingMaterials.get(material, 0) + quantity

        # In case of T2 item, subtract materials of T1 item needed for manufacturing (Wolf - Rifter)
        # because in T2 base materials there is already the T1 item material amount included
        if self.techLevel == 2:
            itemT1 = self.getT1ItemForT2Blueprint()
            if itemT1:
                bpT1 = EveBlueprint(self.__dbAccessObj, productTypeID=itemT1)
                # subtract base materials of T1 from list        
                for material, quantity in bpT1.getListOfBaseMaterials().iteritems():
                    listOfTotalManufacturingMaterials[material] = listOfTotalManufacturingMaterials.get(material, 0) - quantity

        # Calculate and add waste to list of materials
        for material, quantity in listOfTotalManufacturingMaterials.iteritems():

            wasteME = EveMath.calculateWasteFromBlueprintMELevel(quantity,
                                                                 self.wasteFactor,
                                                                 self.researchLevelME)

            wastePE = EveMath.calculateWasteFromCharacterTEskillLevel(quantity,
                                                                      characterTEskillLevel)

            listOfTotalManufacturingMaterials[material] = listOfTotalManufacturingMaterials[material] + (wasteME + wastePE)

        # add extra materials to list        
        for material, quantity in self.getListOfExtraMaterials().iteritems():
            listOfTotalManufacturingMaterials[material] = listOfTotalManufacturingMaterials.get(material, 0) + quantity

        return listOfTotalManufacturingMaterials
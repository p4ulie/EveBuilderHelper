'''
Classes for accessing Eve Online data dump DB

Created on 8.7.2012

@author: PA
'''

import sys
import sqlite3 as lite


class EveDB(object):
    '''
    Base class for interacting with EveDB
    '''

    DB = ''

    def fetchData(self, query):
        '''
        Main method for accessing the DB
        '''
        try:
            dbcon = lite.connect(self.DB)
            cur = dbcon.cursor()
            cur.execute(query)
            rows = cur.fetchall()
        except lite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)
        finally:
            if dbcon:
                dbcon.close()
        return rows

    def __init__(self, DB):
        '''
        Constructor
        '''
        self.DB = DB


class EveLists(EveDB):
    '''
    Class obtaining lists of entries from EveDB tables (Categories, Groups, ...)
    '''

    def getCategoriesList(self):
        '''
        Get list of categories
        '''
        query = """
                    SELECT c.categoryID, c.categoryName, c.description
                    FROM invCategories AS c
                    WHERE c.published = 1
                """
        data = self.fetchData(query)
        return data

    def getGroupsList(self, category=''):
        '''
        Get list of groups
        '''
        if category is '':
            query = """
                        SELECT g.groupID, g.categoryID, g.groupName, g.description
                        FROM invGroups AS g
                        WHERE g.published = 1
                    """
        else:
            query = """
                        SELECT g.groupID, g.categoryID, g.groupName, g.description
                        FROM invGroups AS g
                        WHERE g.published = 1
                        and g.categoryID = %s
                    """ % category
        data = self.fetchData(query)
        return data


class EveInvType(EveDB):
    '''
    Class for Item and Blueprint data reading and handling
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

    def __geItemData(self, typeID=0, typeName=''):
        '''
        Get item data from ID (preferred) or name
        (supposedly ID can be changed in next DB dump)
        '''

        if typeID != 0:
            query = """
                        SELECT *
                        FROM invTypes AS t
                        WHERE t.typeID = '%s'
                    """ % typeID
        else:
            query = """
                        SELECT *
                        FROM invTypes AS t
                        WHERE t.typeName = '%s'
                    """ % typeName

        data = self.fetchData(query)
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

    def __getBlueprintData(self):
        '''
        Get blueprint data for item
        '''
        query = """
                    SELECT *
                    FROM invBlueprintTypes AS b
                    WHERE b.productTypeID = %s
                """ % self.typeID
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
        Get list of materials for item,
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
        Get list of materials for item,
        equals amount of materials when recycling item
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

    def __computeWasteFromMEResearchLevel(self, materialAmount, ME):
        '''
        Compute waste for specific ME level
        '''
        if ME >= 0:
            waste = round(float(materialAmount) * (float(self.wasteFactor) / 100) * (1 / (float(ME) + 1)))
        else:
            waste = round(float(materialAmount) * (float(self.wasteFactor) / 100) * (1 - float(ME)))
        return int(waste)

    def __computeWasteFromPESkill(self, materialAmount, PE):
        '''
        Compute waste for trained Production Efficiency skill level
        '''
        waste = round(((25 - (5 * float(PE))) * float(materialAmount)) / 100)
        return int(waste)

    def getProduceMaterialIDList(self):
        '''
        Generate a list of materials for production, list of IDs only
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
        waste is added from researched ME amount and PE skill level
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

    def __init__(self, DB, typeID=0, typeName=''):
        '''
        Constructor, initial data load
        '''
        self.DB = DB
        self.__geItemData(typeID, typeName)
        self.__getBlueprintData()


class EveRegion(EveDB):
    '''
    Class for Region data reading
    '''

    regionID = ''
    regionName = ''

    def __getRegionData(self, regionID=0, regionName=''):
        '''
        Get item data from ID (preferred) or name
        '''

        if regionID != 0:
            query = """
                        SELECT *
                        FROM mapRegions AS r
                        WHERE r.regionID = '%s'
                    """ % regionID
        else:
            query = """
                        SELECT *
                        FROM mapRegions AS r
                        WHERE r.regionName = '%s'
                    """ % regionName

        data = self.fetchData(query)
        self.regionID = data[0][0]
        self.regionName = data[0][1]

    def __init__(self, DB, regionID=0, regionName=''):
        '''
        Constructor, initial data load
        '''
        self.DB = DB
        self.__getRegionData(regionID, regionName)


class EveSolarSystem(EveDB):
    '''
    Class for Solar System data reading
    '''

    regionID = ''
    constellationID = ''
    solarSystemID = ''
    solarSystemName = ''

    def __getSolarSystemData(self, solarSystemID=0, solarSystemName=''):
        '''
        Get item data from ID (preferred) or name
        '''

        if solarSystemID != 0:
            query = """
                        SELECT *
                        FROM mapSolarSystems AS s
                        WHERE s.solarSystemID = '%s'
                    """ % solarSystemID
        else:
            query = """
                        SELECT *
                        FROM mapSolarSystems AS s
                        WHERE s.solarSystemName = '%s'
                    """ % solarSystemName

        data = self.fetchData(query)
        self.regionID = data[0][0]
        self.constellationID = data[0][1]
        self.solarSystemID = data[0][2]
        self.solarSystemName = data[0][3]

    def __init__(self, DB, solarSystemID=0, solarSystemName=''):
        '''
        Constructor, initial data load
        '''
        self.DB = DB
        self.__getSolarSystemData(solarSystemID, solarSystemName)

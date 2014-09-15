'''
Created on 18.6.2014

@author: Pavol Antalik
'''

#import syck
from EveMath.EveMathConstants import *


class EveDB(object):
    '''
    Class for containing EVE Online data dump data and methods
    '''

    def __init__(self,
                 dbAccessObj):
        '''
        Constructor
        '''

        self.dbAccessObj = dbAccessObj

    def getListOfInvCategories(self):
        '''
        Get list of categories
        '''
        data = None

        query = """
                    SELECT c.categoryID,
                            c.categoryName,
                            c.description,
                            c.iconID
                    FROM invCategories AS c
                    WHERE c.published = 1
                """
        result = self.dbAccessObj.fetchData(query)

        if result is not None:
            data = {}
            for row in result:
                data[row[0]] = {'categoryID': row[0],
                                 'categoryName': row[1],
                                 'description': row[2],
                                 'iconID': row[3]}

        return data

    def getListOfInvGroups(self, categoryID=None):
        '''
        Get list of groups
        '''
        data = None

        if categoryID is not None:
            query = """
                        SELECT g.groupID,
                                g.categoryID,
                                g.groupName,
                                g.description,
                                g.iconID
                        FROM invGroups AS g
                        WHERE g.published = '1'
                        AND g.categoryID = ?
                    """
            result = self.dbAccessObj.fetchData(query, categoryID)
        else:
            query = """
                        SELECT g.groupID,
                                g.categoryID,
                                g.groupName,
                                g.description,
                                g.iconID
                        FROM invGroups AS g
                        WHERE g.published = '1'
                    """
            result = self.dbAccessObj.fetchData(query)

        if result is not None:
            data = {}
            for row in result:
                data[row[0]] = {'groupID': row[0],
                                 'categoryID': row[1],
                                 'groupName': row[2],
                                 'description': row[3],
                                 'iconID': row[4]}

        return data

    def getListOfInvItems(self, typeName=None, groupID=None):
        '''
        Get list of items by (part of) name or groupID
        '''
        query = ''
        result = None

        if typeName is not None:
            query = """
                        SELECT t.typeID,
                                t.groupID,
                                t.typeName,
                                t.description,
                                t.mass,
                                t.volume,
                                t.capacity,
                                t.portionSize,
                                t.raceID,
                                t.basePrice,
                                t.marketGroupID
                        FROM invtypes AS t
                        WHERE t.published = '1'
                        AND t.typeName like '%?%'
                    """
            result = self.dbAccessObj.fetchData(query, typeName)
        else:
            if groupID is not None:
                query = """
                            SELECT t.typeID,
                                    t.groupID,
                                    t.typeName,
                                    t.description,
                                    t.mass,
                                    t.volume,
                                    t.capacity,
                                    t.portionSize,
                                    t.raceID,
                                    t.basePrice,
                                    t.marketGroupID
                            FROM invtypes AS t
                            WHERE t.published = '1'
                            AND t.groupID = ?
                        """
                result = self.dbAccessObj.fetchData(query, groupID)

        if result is not None:
            data = {}
            for row in result:
                data[row[0]] = {'typeID': row[0],
                                 'groupID': row[1],
                                 'typeName': row[2],
                                 'description': row[3],
                                 'mass': row[4],
                                 'volume': row[5],
                                 'capacity': row[6],
                                 'portionSize': row[7],
                                 'raceID': row[8],
                                 'basePrice': row[9],
                                 'marketGroupID': row[0]}
        else:
            data = None

        return data

    def getInvItem(self, typeID=None, typeName=None, groupID=None):
        '''
        Get item by ID or name
        '''
        query = ''
        result = None

        if typeID is not None:
            query = """
                        SELECT t.typeID,
                                t.groupID,
                                t.typeName,
                                t.description,
                                t.mass,
                                t.volume,
                                t.capacity,
                                t.portionSize,
                                t.raceID,
                                t.basePrice,
                                t.marketGroupID
                        FROM invtypes AS t
                        WHERE t.published = '1'
                        AND t.typeID = ?
                    """
            result = self.dbAccessObj.fetchData(query, typeID)
        else:
            if typeName is not None:
                query = """
                            SELECT t.typeID,
                                    t.groupID,
                                    t.typeName,
                                    t.description,
                                    t.mass,
                                    t.volume,
                                    t.capacity,
                                    t.portionSize,
                                    t.raceID,
                                    t.basePrice,
                                    t.marketGroupID
                            FROM invtypes AS t
                            WHERE t.published = '1'
                            AND t.typeName = ?
                        """
                result = self.dbAccessObj.fetchData(query, typeName)

        if result is not None:
            # take only the first row
            row = result[0]
            data = {'typeID': row[0],
                     'groupID': row[1],
                     'typeName': row[2],
                     'description': row[3],
                     'mass': row[4],
                     'volume': row[5],
                     'capacity': row[6],
                     'portionSize': row[7],
                     'raceID': row[8],
                     'basePrice': row[9],
                     'marketGroupID': row[0]}
        else:
            data = None

        return data

    def getBlueprintIDForItem(self,
                              typeID=None,
                              activityID=EVE_ACTIVITY_MANUFACTURING):
        '''
        Get Blueprint typeID from Item typeID
        '''

        data = None

        if typeID is not None:
            query = """
                        SELECT typeID
                        FROM industryactivityproducts AS i
                        WHERE i.productTypeID = ?
                        and i.activityID = ?
                    """
            result = self.dbAccessObj.fetchData(query, typeID, activityID)
    
            if (result is not None) and (len(result) > 0):
                data = result[0][0]

        return data

    def getMaterialsForBlueprint(self,
                                 blueprintTypeID,
                                 activityID=EVE_ACTIVITY_MANUFACTURING):
        '''
        Get list of materials for specified blueprint typeID and activityID
        '''
        query = """
                    SELECT i.materialTypeID,
                            i.quantity,
                            i.consume
                    FROM industryactivitymaterials AS i
                    WHERE i.typeID = ?
                    and i.activityID = ?
                """
        result = self.dbAccessObj.fetchData(query,
                                              blueprintTypeID,
                                              activityID)

        if result is not None:
            data = {}
            for row in result:
                data[row[0]] = {'materialTypeID': row[0],
                                 'quantity': row[1],
                                 'consume': row[2]}
        else:
            data = None

        return data

    def getTimeForBlueprint(self,
                            blueprintTypeID,
                            activityID=EVE_ACTIVITY_MANUFACTURING):
        '''
        Get time of industry action for specified blueprint typeID
        and activityID
        '''
        query = """
                    SELECT time
                    FROM industryactivity AS i
                    WHERE i.typeID = ?
                    and i.activityID = ?
                """
        result = self.dbAccessObj.fetchData(query,
                                              blueprintTypeID,
                                              activityID)

        if result is not None:
            data = result[0][0]
        else:
            data = None

        return data

    def getListOfRamActivities(self):
        '''
        Get list of ramActivities
        '''
        query = """
                    SELECT r.activityID,
                            r.activityName,
                            r.iconNo,
                            r.description
                    FROM ramActivities AS r
                    WHERE r.published = '1'
                """
        result = self.dbAccessObj.fetchData(query)

        if result is not None:
            data = {}
            for row in result:
                data[row[0]] = {'activityID': row[0],
                                 'activityName': row[1],
                                 'iconNo': row[2],
                                 'description': row[3]}

        else:
            data = None

        return data

    def getListOfRamAssemblyLineTypes(self,
                                      activityID=EVE_ACTIVITY_MANUFACTURING):
        '''
        Get list of ramassemblylinetypes
        '''
        query = """
                    SELECT r.assemblyLineTypeID,
                            r.assemblyLineTypeName,
                            r.description,
                            r.baseTimeMultiplier,
                            r.baseMaterialMultiplier,
                            r.baseCostMultiplier,
                            r.volume,
                            r.activityID,
                            r.minCostPerHour
                    FROM ramassemblylinetypes AS r
                    WHERE r.activityID = ?
                """
        result = self.dbAccessObj.fetchData(query, activityID)

        if result is not None:
            data = {}
            for row in result:
                data[row[0]] = {'assemblyLineTypeID': row[0],
                                 'assemblyLineTypeName': row[1],
                                 'description': row[2],
                                 'baseTimeMultiplier': row[3],
                                 'baseMaterialMultiplier': row[4],
                                 'baseCostMultiplier': row[5],
                                 'volume': row[6],
                                 'activityID': row[7],
                                 'minCostPerHour': row[8]}
        else:
            data = None

        return data

    def getActivityBonusForRamAssemblyLineType(self,
                                               assemblyLineTypeID=None,
                                               assemblyLineTypeName=None,
                                               activityID=EVE_ACTIVITY_MANUFACTURING):
        '''
        Get bonus multiplier for specified activity and assembly line type
        '''
        result = None

        if assemblyLineTypeID is not None:
            query = """
                            SELECT r.baseTimeMultiplier,
                                    r.baseMaterialMultiplier,
                                    r.baseCostMultiplier,
                                    r.volume,
                                    r.activityID,
                                    r.minCostPerHour
                            FROM ramassemblylinetypes AS r
                            WHERE r.activityID = ?
                            AND r.assemblyLineTypeID = ?
                    """
            result = self.dbAccessObj.fetchData(query,
                                                  activityID,
                                                  assemblyLineTypeID)
        else:
            if assemblyLineTypeName is not None:
                query = """
                            SELECT r.baseTimeMultiplier,
                                    r.baseMaterialMultiplier,
                                    r.baseCostMultiplier,
                                    r.volume,
                                    r.activityID,
                                    r.minCostPerHour
                            FROM ramassemblylinetypes AS r
                            WHERE r.activityID = ?
                            AND r.assemblyLineTypeName = ?
                        """
                result = self.dbAccessObj.fetchData(query,
                                                      activityID,
                                                      assemblyLineTypeName)

        if result is not None:
            row = result[0]
            data = {'baseTimeMultiplier': row[0],
                     'baseMaterialMultiplier': row[1],
                     'baseCostMultiplier': row[2],
                     'volume': row[3],
                     'activityID': row[4],
                     'minCostPerHour': row[5]}
        else:
            data = None

        return data

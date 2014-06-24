'''
Created on 18.6.2014

@author: Pavol Antalik
'''

class EveDB(object):
    '''
    Class for containing EVE Online data dump data and methods
    '''

    def __init__(self,
                 dbAccessObj):
        '''
        Constructor
        '''

        self.__dbAccessObj = dbAccessObj
    
    def getListOfInvCategories(self):
        '''
        Get list of categories
        '''
        query = """
                    SELECT c.categoryID, c.categoryName, c.description
                    FROM invCategories AS c
                    WHERE c.published = 1
                """

        data = self.__dbAccessObj.fetchData(query)

        return data
        
    def getListOfInvGroups(self, categoryID = None):
        '''
        Get list of groups
        '''
        query = """
                    SELECT g.groupID, g.categoryID, g.groupName, g.description
                    FROM invGroups AS g
                    WHERE g.published = '1'
                """
        if categoryID:
            query += """
                        AND g.categoryID = '%s'
                    """ % categoryID

        data = self.__dbAccessObj.fetchData(query)

        return data
    
    def getListOfInvItems(self, groupID = None):
        '''
        Get list of items, possibly from specific group
        '''
        query = """
                    SELECT *
                    FROM invtypes AS t
                    WHERE t.published = '1'
                """ % groupID
        if groupID:
            query += """
                        AND t.groupID = '%s'
                    """

        data = self.__dbAccessObj.fetchData(query)

        return data

    def getInvItem(self, typeID = None, typeName = None):
        '''
        Get item by ID or name
        '''
        query = ''
        
        if typeID:
            query = """
                        SELECT *
                        FROM invtypes AS t
                        WHERE t.typeID = '%s'
                    """ % typeID
        else:
            if typeName:
                query = """
                            SELECT *
                            FROM invtypes AS t
                            WHERE t.typeName = '%s'
                        """ % typeName

        if query is not '':
            # only one row of data
            data = self.__dbAccessObj.fetchData(query)[0]
        else:
            data = None

        return data

    def getInvItemIDByName(self, typeName):
        '''
        Get item ID by name
        '''
        return self.getInvItem(typeName = typeName)[0]
    
    def getInvItemNameByID(self, typeID):
        '''
        Get item ID by name
        '''
        return self.getInvItem(typeID = typeID)[2]
    
    
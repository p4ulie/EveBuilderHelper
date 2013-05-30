'''
Created on 7.4.2013

@author: Pavol Antalik
'''

from EveDB import EveDB


class EveInvGroup(EveDB):
    '''
    Class for invGroup data reading and handling
    '''

    groupID = ''
    categoryID = ''
    groupName = ''
    description = ''

    def __getInvGroup(self, query):
        '''
        Get invGroup data from DB
        '''
        data = self.fetchData(query)
        if data:
            self.groupID = data[0][0]
            self.categoryID = data[0][1]
            self.groupName = data[0][2]
            self.description = data[0][3]

    def getInvGroupByID(self, groupID):
        '''
        Get invGroup by ID
        '''
        query = """
                    SELECT g.groupID, g.categoryID, g.groupName, g.description
                    FROM invGroups AS g
                    WHERE g.groupID = %s
                """ % groupID
        self.__getInvGroup(query)

    def getInvGroupByName(self, groupName):
        '''
        Get invGroup by name
        '''
        query = """
                    SELECT g.groupID, g.categoryID, g.groupName, g.description
                    FROM invGroups AS g
                    WHERE g.groupName = '%s'
                """ % groupName
        self.__getInvGroup(query)

    def getInvGroupsList(self, categoryID=''):
        '''
        Get list of groups
        '''
        if categoryID is '':
            query = """
                        SELECT g.groupID, g.categoryID, g.groupName, g.description
                        FROM invGroups AS g
                        WHERE g.published = '1'
                    """
        else:
            query = """
                        SELECT g.groupID, g.categoryID, g.groupName, g.description
                        FROM invGroups AS g
                        WHERE g.published = '1'
                        and g.categoryID = '%s'
                    """ % categoryID
        data = self.fetchData(query)
        return data

    def __init__(self, DB, groupID='', groupName=''):
        '''
        Constructor, initial data load
        '''
        self.DB = DB

        if groupID != '':
            self.getInvGroupByID(groupID)
        else:
            if groupName != '':
                self.getInvGroupByName(groupName)

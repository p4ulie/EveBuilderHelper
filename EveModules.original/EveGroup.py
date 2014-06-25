'''
Created on 7.4.2013

@author: Pavol Antalik
'''

from EveDB import EveDB


class EveGroup(EveDB):
    '''
    Class for invGroup data reading and handling
    '''

    groupID = ''
    categoryID = ''
    groupName = ''
    description = ''

    def __getGroup(self, query):
        '''
        Get invGroup data from DB
        '''
        data = self.fetchData(query)
        if data:
            self.groupID = data[0][0]
            self.categoryID = data[0][1]
            self.groupName = data[0][2]
            self.description = data[0][3]

    def getGroupByID(self, groupID):
        '''
        Get invGroup by ID
        '''
        query = """
                    SELECT g.groupID, g.categoryID, g.groupName, g.description
                    FROM invGroups AS g
                    WHERE g.groupID = %s
                """ % groupID
        self.__getGroup(query)

    def getGroupByName(self, groupName):
        '''
        Get invGroup by name
        '''
        query = """
                    SELECT g.groupID, g.categoryID, g.groupName, g.description
                    FROM invGroups AS g
                    WHERE g.groupName = '%s'
                """ % groupName
        self.__getGroup(query)

    def __init__(self, DB, groupID='', groupName=''):
        '''
        Constructor, initial data load
        '''
        self.DB = DB

        if groupID != '':
            self.getGroupByID(groupID)
        else:
            if groupName != '':
                self.getGroupByName(groupName)


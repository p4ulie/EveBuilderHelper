'''
Created on 7.4.2013

@author: Pavol Antalik
'''

from EveDB import EveDB


class EveInvCategory(EveDB):
    '''
    Class for invCategory data reading and handling
    '''

    categoryID = ''
    categoryName = ''
    description = ''

    def __getInvCategory(self, query):
        '''
        Get invCategory data from DB
        '''
        data = self.fetchData(query)
        if data:
            self.categoryID = data[0][0]
            self.categoryName = data[0][1]
            self.description = data[0][1]

    def getInvCategoryByID(self, categoryID):
        '''
        Get invCategory by ID
        '''
        query = """
                    SELECT c.categoryID, c.categoryName, c.description
                    FROM invCategories AS c
                    WHERE c.categoryID = %s
                """ % categoryID
        self.__getInvCategory(query)

    def getInvCategoryByName(self, categoryName):
        '''
        Get invCategory by name
        '''
        query = """
                    SELECT c.categoryID, c.categoryName, c.description
                    FROM invCategories AS c
                    WHERE c.categoryName = '%s'
                """ % categoryName
        self.__getInvCategory(query)

    def getInvCategoriesList(self):
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

    def __init__(self, DB, categoryID='', categoryName=''):
        '''
        Constructor, initial data load
        '''
        self.DB = DB

        if categoryID != '':
            self.getInvCategoryByID(categoryID)
        else:
            if categoryName != '':
                self.getInvCategoryByName(categoryName)

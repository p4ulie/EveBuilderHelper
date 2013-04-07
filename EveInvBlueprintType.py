'''
Created on 7.4.2013

@author: Pavol Antalik
'''

import EveDB


class EveInvBlueprintType(EveDB):
    '''
    Class for Blueprint data reading and handling
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

    def __getInvBlueprintType(self):
        '''
        Get blueprint data from DB
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

    def __init__(self, DB, blueprintTypeID=''):
        '''
        Constructor, initial data load
        '''

        self.DB = DB

        if blueprintTypeID != '':
            self.__getInvBlueprintType(blueprintTypeID)

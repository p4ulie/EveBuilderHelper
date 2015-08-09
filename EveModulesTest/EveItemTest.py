'''
Created on Nov 25, 2014

@author: paulie
'''
import unittest
from DataAccess.DBAccessSQLite import DBAccessSQLite
from DataAccess.EveDB import EveDB
from EveOnline.EveItem import EveItem


class TestEveItem(unittest.TestCase):
    '''
    Unit test for class EveItem
    '''

    datafile = '../data/eve.db'

    maxDiff = None

    def setUp(self):
        '''
        Set-up of the testing environment
        '''
        self.db_access_object = DBAccessSQLite(self.datafile)
        self.data_access_object = EveDB(self.db_access_object)
        self.eve_item = EveItem(self.data_access_object)

    def tearDown(self):
        '''
        Tear-down of the testing environment
        '''
        self.db_access_object.close()

    def test_get_item_charon(self):
        '''
        Test for loading data to object attributes
        '''
        self.eve_item.get_item(type_name="Charon")
        self.failUnlessEqual("Charon",
                             self.eve_item.type_name)

    def test_get_item_ark(self):
        '''
        Test for loading data to object attributes - Ark
        '''
        self.eve_item.get_item(type_id=28850)
        self.failUnlessEqual("Ark",
                             self.eve_item.type_name)


if __name__ == "__main__":
    unittest.main()

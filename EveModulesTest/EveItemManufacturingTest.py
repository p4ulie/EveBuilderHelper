'''
Created on Nov 25, 2014

@author: paulie
'''
import unittest
from DataAccess.DBAccessSQLite import DBAccessSQLite
from DataAccess.EveDB import EveDB
from EveOnline.EveItemManufacturing import EveItemManufacturing


class Test(unittest.TestCase):
    '''
    Unit test for class EveItemManufacturing
    '''

    DATA_FILE = '../data/eve.db'
    eve_item_manufacturing = None

    BUILD_PRODUCT_NAME = 'Ark'
    BUILD_PRODUCT_RUNS = 1
    BUILD_PRODUCT_ME = 5
    BUILD_PRODUCT_TE = 0

    maxDiff = None

    def setUp(self):
        '''
        Set up of test
        '''
        self.db_access_obj = DBAccessSQLite(self.DATA_FILE)
        self.data_access = EveDB(self.db_access_obj)

        self.eve_item_manufacturing = EveItemManufacturing(self.data_access,
                                                           type_name=self.BUILD_PRODUCT_NAME)

    def tearDown(self):
        '''
        Tear down of test
        '''
        self.db_access_obj.close()

    def test_get_item(self):
        '''
        Get item
        '''
        self.eve_item_manufacturing.get_item(type_name="Providence")
        self.failUnlessEqual("Providence",
                             self.eve_item_manufacturing.type_name)

    def test_get_manufacturing_job_list(self):
        '''
        Obtain list of manufacturing jobs
        '''
        job_list = ['Ark',
                    'Capital Jump Drive',
                    'Capital Radar Sensor Cluster',
                    'Capital Linear Shield Emitter',
                    'Capital Antimatter Reactor Unit',
                    'Capital Nanoelectrical Microprocessor',
                    'Capital Tungsten Carbide Armor Plate',
                    'R.A.M.- Starship Tech',
                    'Providence',
                    'Capital Propulsion Engine',
                    'Capital Cargo Bay',
                    'Capital Construction Parts',
                    'Capital Armor Plates',
                    'Capital Tesseract Capacitor Unit',
                    'Capital Fusion Thruster']

        self.eve_item_manufacturing.get_item(type_name="Ark")
        self.eve_item_manufacturing.blueprint_me_level = self.BUILD_PRODUCT_ME
        self.eve_item_manufacturing.manufacturing_quantity = self.BUILD_PRODUCT_RUNS
        self.eve_item_manufacturing.manufacturing_data_calculate()

        self.failUnlessEqual(job_list,
                             [job.type_name for job in self.eve_item_manufacturing.get_manufacturing_job_list()])

    def test_get_manufacturing_job_list_with_assets(self):
        '''
        Get manufacturing job list, with assets
        '''
        job_list = ['Ark',
                    'Capital Radar Sensor Cluster',
                    'Capital Linear Shield Emitter',
                    'Capital Antimatter Reactor Unit',
                    'Capital Nanoelectrical Microprocessor',
                    'Capital Tungsten Carbide Armor Plate',
                    'R.A.M.- Starship Tech',
                    'Providence',
                    'Capital Propulsion Engine',
                    'Capital Cargo Bay',
                    'Capital Construction Parts',
                    'Capital Armor Plates',
                    'Capital Tesseract Capacitor Unit',
                    'Capital Fusion Thruster']

        assets = {21025: 29}   # 21025: Capital Jump Drive

        self.eve_item_manufacturing.get_item(type_name="Ark")
        self.eve_item_manufacturing.blueprint_me_level = self.BUILD_PRODUCT_ME
        self.eve_item_manufacturing.manufacturing_quantity = self.BUILD_PRODUCT_RUNS
        self.eve_item_manufacturing.asset_list = assets

        self.eve_item_manufacturing.manufacturing_data_calculate()

        self.failUnlessEqual(job_list,
                             [job.type_name for job in self.eve_item_manufacturing.get_manufacturing_job_list()])

    def test_get_material_list(self):
        '''
        Get material list
        '''
        material_list = {16672: 11401167.0, 16678: 2976997.0, 34: 133069643.0, 35: 19441019.0, 36: 7163272.0, 37: 1089400.0, 38: 314014.0, 39: 1, 40: 20618.0, 16681: 40084.0, 16682: 13904.0, 11399: 3563.0, 33360: 44176.0, 16680: 76090.0, 3828: 2138.0, 16679: 1115444.0, 16683: 13673.0, 17317: 16258.0}

        assets = {39: 51732}  # 39: Zydrine

        self.eve_item_manufacturing.get_item(type_name="Ark")
        self.eve_item_manufacturing.blueprint_me_level = self.BUILD_PRODUCT_ME
        self.eve_item_manufacturing.manufacturing_quantity = self.BUILD_PRODUCT_RUNS
        self.eve_item_manufacturing.asset_list = assets

        self.eve_item_manufacturing.manufacturing_data_calculate()

        self.failUnlessEqual(material_list,
                             self.eve_item_manufacturing.get_manufacturing_material_list())

    def test_get_material_list_with_assets(self):
        '''
        Get material list with assets
        '''
        material_list = {16672: 11401167.0, 16678: 2976997.0, 34: 133069643.0, 35: 19441019.0, 36: 7163272.0, 37: 1089400.0, 38: 314014.0, 39: 51733.0, 40: 20618.0, 16681: 40084.0, 16682: 13904.0, 11399: 3563.0, 33360: 44176.0, 16680: 76090.0, 3828: 2138.0, 16679: 1115444.0, 16683: 13673.0, 17317: 16258.0}

        self.eve_item_manufacturing.get_item(type_name="Ark")
        self.eve_item_manufacturing.blueprint_me_level = self.BUILD_PRODUCT_ME
        self.eve_item_manufacturing.manufacturing_quantity = self.BUILD_PRODUCT_RUNS
        self.eve_item_manufacturing.manufacturing_data_calculate()

        self.failUnlessEqual(material_list,
                             self.eve_item_manufacturing.get_manufacturing_material_list())

    def test_get_manufacturing_job_by_id(self):
        '''
        Get manufacturing job by ID
        '''
        self.eve_item_manufacturing.get_item(type_name="Ark")
        self.eve_item_manufacturing.blueprint_me_level = self.BUILD_PRODUCT_ME
        self.eve_item_manufacturing.manufacturing_quantity = self.BUILD_PRODUCT_RUNS
        self.eve_item_manufacturing.manufacturing_data_calculate()

        job_name = "Capital Jump Drive"

        self.failUnlessEqual(job_name,
                             self.eve_item_manufacturing.get_manufacturing_job_by_id(type_id=21025).type_name)

    def test_get_manufacturing_job_by_name(self):
        '''
        Get manufacturing job by manufactured item name
        '''
        self.eve_item_manufacturing.get_item(type_name="Ark")
        self.eve_item_manufacturing.blueprint_me_level = self.BUILD_PRODUCT_ME
        self.eve_item_manufacturing.manufacturing_quantity = self.BUILD_PRODUCT_RUNS
        self.eve_item_manufacturing.manufacturing_data_calculate()

        job_id = 21025

        self.failUnlessEqual(job_id,
                             self.eve_item_manufacturing.get_manufacturing_job_by_name(type_name="Capital Jump Drive").type_id)


if __name__ == "__main__":
    unittest.main()

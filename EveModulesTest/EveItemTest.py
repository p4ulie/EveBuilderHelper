'''
Created on Nov 25, 2014

@author: paulie
'''
import unittest
from DBAccessSQLite import DBAccessSQLite
from EveOnline.EveItem import *


class Test(unittest.TestCase):

    DB = '../data/eve.db'
    eveItem = None

    BUILD_PRODUCT_NAME = 'Ark'
    BUILD_PRODUCT_RUNS = 1
    BUILD_PRODUCT_ME = 5
    BUILD_PRODUCT_TE = 0

    def setUp(self):
        self.dbAccess = DBAccessSQLite(self.DB)
        self.eveItem = EveItem(self.dbAccess,
                               type_name=self.BUILD_PRODUCT_NAME)

    def tearDown(self):
        self.dbAccess.close()

    def test_get_item(self):
        self.eveItem.get_item(type_name="Providence")
        self.failUnlessEqual("Providence",
                             self.eveItem.type_name)

    def test_get_manufacturing_job_list(self):
        job_list = ['Ark', 'Capital Jump Drive', 'Capital Radar Sensor Cluster', 'Capital Linear Shield Emitter', 'Capital Antimatter Reactor Unit', 'Capital Nanoelectrical Microprocessor', 'Capital Tungsten Carbide Armor Plate', 'R.A.M.- Starship Tech', 'Providence', 'Capital Propulsion Engine', 'Capital Cargo Bay', 'Capital Construction Parts', 'Capital Armor Plates', 'Capital Tesseract Capacitor Unit', 'Capital Fusion Thruster']

        self.eveItem.get_item(type_name="Ark")
        self.eveItem.blueprint_me_level = self.BUILD_PRODUCT_ME
        self.eveItem.manufacturing_quantity = self.BUILD_PRODUCT_RUNS
        self.eveItem.manufacturing_data_calculate()

        self.failUnlessEqual(job_list,
                             [job.type_name for job in self.eveItem.get_manufacturing_job_list()])

    def test_get_manufacturing_job_list_with_assets(self):
        job_list = ['Ark', 'Capital Radar Sensor Cluster', 'Capital Linear Shield Emitter', 'Capital Antimatter Reactor Unit', 'Capital Nanoelectrical Microprocessor', 'Capital Tungsten Carbide Armor Plate', 'R.A.M.- Starship Tech', 'Providence', 'Capital Propulsion Engine', 'Capital Cargo Bay', 'Capital Construction Parts', 'Capital Armor Plates', 'Capital Tesseract Capacitor Unit', 'Capital Fusion Thruster']

        assets = {21025: 29}   # 21025: Capital Jump Drive

        self.eveItem.get_item(type_name="Ark")
        self.eveItem.blueprint_me_level = self.BUILD_PRODUCT_ME
        self.eveItem.manufacturing_quantity = self.BUILD_PRODUCT_RUNS
        self.eveItem.asset_list = assets

        self.eveItem.manufacturing_data_calculate()

        self.failUnlessEqual(job_list,
                             [job.type_name for job in self.eveItem.get_manufacturing_job_list()])

    def test_get_material_list(self):
        material_list = {16672: 11401167.0, 16678: 2976997.0, 34: 133069643.0, 35: 19441019.0, 36: 7163272.0, 37: 1089400.0, 38: 314014.0, 39: 1, 40: 20618.0, 16681: 40084.0, 16682: 13904.0, 11399: 3563.0, 33360: 44176.0, 16680: 76090.0, 3828: 2138.0, 16679: 1115444.0, 16683: 13673.0, 17317: 16258.0}

        assets = {39: 51732}  # 39: Zydrine

        self.eveItem.get_item(type_name="Ark")
        self.eveItem.blueprint_me_level = self.BUILD_PRODUCT_ME
        self.eveItem.manufacturing_quantity = self.BUILD_PRODUCT_RUNS
        self.eveItem.asset_list = assets

        self.eveItem.manufacturing_data_calculate()

        self.failUnlessEqual(material_list,
                             self.eveItem.get_material_list())

    def test_get_material_list_with_assets(self):
        material_list = {16672: 11401167.0, 16678: 2976997.0, 34: 133069643.0, 35: 19441019.0, 36: 7163272.0, 37: 1089400.0, 38: 314014.0, 39: 51733.0, 40: 20618.0, 16681: 40084.0, 16682: 13904.0, 11399: 3563.0, 33360: 44176.0, 16680: 76090.0, 3828: 2138.0, 16679: 1115444.0, 16683: 13673.0, 17317: 16258.0}

        self.eveItem.get_item(type_name="Ark")
        self.eveItem.blueprint_me_level = self.BUILD_PRODUCT_ME
        self.eveItem.manufacturing_quantity = self.BUILD_PRODUCT_RUNS
        self.eveItem.manufacturing_data_calculate()

        self.failUnlessEqual(material_list,
                             self.eveItem.get_material_list())

    def test_get_manufacturing_job_by_id(self):
        self.eveItem.get_item(type_name="Ark")
        self.eveItem.blueprint_me_level = self.BUILD_PRODUCT_ME
        self.eveItem.manufacturing_quantity = self.BUILD_PRODUCT_RUNS
        self.eveItem.manufacturing_data_calculate()

        job_name = "Capital Jump Drive"

        self.failUnlessEqual(job_name,
                             self.eveItem.get_manufacturing_job_by_id(type_id=21025).type_name)

    def test_get_manufacturing_job_by_name(self):
        self.eveItem.get_item(type_name="Ark")
        self.eveItem.blueprint_me_level = self.BUILD_PRODUCT_ME
        self.eveItem.manufacturing_quantity = self.BUILD_PRODUCT_RUNS
        self.eveItem.manufacturing_data_calculate()

        job_id = 21025

        self.failUnlessEqual(job_id,
                             self.eveItem.get_manufacturing_job_by_name(type_name="Capital Jump Drive").type_id)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
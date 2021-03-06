'''
Created on 14.1.2014

@author: paulie
'''

import unittest
from DataAccess.DBAccessSQLite import DBAccessSQLite
from DataAccess.EveDB import EveDB


class TestEveDB(unittest.TestCase):
    '''
    Unit test for class EveDB
    '''

    DATA_FILE = '../data/eve.db'

    maxDiff = None

    def setUp(self):
        '''
        Set-up of the testing environment
        '''
        self.db_access_object = DBAccessSQLite(self.DATA_FILE)
        self.data_access_object = EveDB(self.db_access_object)

    def tearDown(self):
        '''
        Tear-down of the testing environment
        '''
        self.db_access_object.close()

    def test_get_list_of_inv_categories(self):
        '''
        Get list of inventory categories
        '''
        categories = [{'icon_id': None, 'category_id': 2, 'category_name': 'Celestial'},
                        {'icon_id': 22, 'category_id': 4, 'category_name': 'Material'},
                        {'icon_id': 33, 'category_id': 5, 'category_name': 'Accessories'},
                        {'icon_id': None, 'category_id': 6, 'category_name': 'Ship'},
                        {'icon_id': 67, 'category_id': 7, 'category_name': 'Module'},
                        {'icon_id': None, 'category_id': 8, 'category_name': 'Charge'},
                        {'icon_id': 21, 'category_id': 9, 'category_name': 'Blueprint'},
                        {'icon_id': 33, 'category_id': 16, 'category_name': 'Skill'},
                        {'icon_id': 0, 'category_id': 17, 'category_name': 'Commodity'},
                        {'icon_id': 0, 'category_id': 18, 'category_name': 'Drone'},
                        {'icon_id': 0, 'category_id': 20, 'category_name': 'Implant'},
                        {'icon_id': 0, 'category_id': 22, 'category_name': 'Deployable'},
                        {'icon_id': 0, 'category_id': 23, 'category_name': 'Starbase'},
                        {'icon_id': 0, 'category_id': 24, 'category_name': 'Reaction'},
                        {'icon_id': None, 'category_id': 25, 'category_name': 'Asteroid'},
                        {'icon_id': None, 'category_id': 30, 'category_name': 'Apparel'},
                        {'icon_id': None, 'category_id': 32, 'category_name': 'Subsystem'},
                        {'icon_id': None, 'category_id': 34, 'category_name': 'Ancient Relics'},
                        {'icon_id': None, 'category_id': 35, 'category_name': 'Decryptors'},
                        {'icon_id': None, 'category_id': 39, 'category_name': 'Infrastructure Upgrades'},
                        {'icon_id': None, 'category_id': 40, 'category_name': 'Sovereignty Structures'},
                        {'icon_id': None, 'category_id': 41, 'category_name': 'Planetary Interaction'},
                        {'icon_id': None, 'category_id': 42, 'category_name': 'Planetary Resources'},
                        {'icon_id': None, 'category_id': 43, 'category_name': 'Planetary Commodities'},
                        {'icon_id': None, 'category_id': 46, 'category_name': 'Orbitals'},
                        {'icon_id': None, 'category_id': 63, 'category_name': 'Special Edition Assets'},
                        {'icon_id': None, 'category_id': 65, 'category_name': 'Structure'},
                        {'icon_id': None, 'category_id': 66, 'category_name': 'Structure Module'}]
        self.failUnlessEqual(categories,
                             self.data_access_object.get_list_of_inv_categories())

    #===============================================================================================
    # def test_get_list_of_inv_groups(self):
    #     '''
    #     Get list of inventory groups
    #     '''
    #     print self.data_access_object.get_list_of_inv_groups(category_id=3)
    #     groups = [{'group_name': 'Cargo Container', 'icon_id': 16, 'group_id': 12, 'description': None, 'category_id': 2}, {'group_name': 'Biomass', 'icon_id': 0, 'group_id': 14, 'description': 'Corpse of human. Can be sold for clone production.', 'category_id': 2}, {'group_name': 'Construction Platform', 'icon_id': 0, 'group_id': 307, 'description': None, 'category_id': 2}, {'group_name': 'Secure Cargo Container', 'icon_id': 0, 'group_id': 340, 'description': None, 'category_id': 2}, {'group_name': 'Audit Log Secure Container', 'icon_id': None, 'group_id': 448, 'description': None, 'category_id': 2}, {'group_name': 'Freight Container', 'icon_id': 1174, 'group_id': 649, 'description': 'Freight Containers are commonly used in Freighter-class ships to accomodate their massive cargobays.', 'category_id': 2}, {'group_name': 'Harvestable Cloud', 'icon_id': 0, 'group_id': 711, 'description': None, 'category_id': 2}, {'group_name': 'Station Upgrade Platform', 'icon_id': 0, 'group_id': 835, 'description': None, 'category_id': 2}, {'group_name': 'Station Improvement Platform', 'icon_id': 0, 'group_id': 836, 'description': None, 'category_id': 2}, {'group_name': 'Flashpoint', 'icon_id': None, 'group_id': 1071, 'description': 'Points of conflict on a planet.', 'category_id': 2}, {'group_name': 'Satellite', 'icon_id': None, 'group_id': 1165, 'description': None, 'category_id': 2}, {'group_name': 'Orbital Target', 'icon_id': None, 'group_id': 1198, 'description': 'Orbital targets are locations on the ground lockable by ships.', 'category_id': 2}]
    #     self.failUnlessEqual(groups,
    #                          self.data_access_object.get_list_of_inv_groups(category_id=2))
    #===============================================================================================

    def test_get_inv_category(self):
        '''
        Get inventory category
        '''
        category = {'icon_id': None, 'category_id': 2, 'category_name': 'Celestial'}
        self.failUnlessEqual(category,
                             self.data_access_object.get_inv_category(category_id=2))

    def test_get_inv_group(self):
        '''
        Get inventory group
        '''
        group = {'group_name': 'Cargo Container', 'anchored': 0, 'group_id': 12, 'anchorable': 0, 'fittable_non_singleton': 0, 'use_base_price': 1, 'icon_id': 16, 'category_id': 2}
        self.failUnlessEqual(group,
                             self.data_access_object.get_inv_group(group_id=12))

    def test_get_list_of_inv_items(self):
        '''
        Get list of inventory items
        '''
        items = [{'market_group_id': 1657, 'description': 'A standard cargo container, used for common freight.', 'type_id': 3293, 'volume': 325.0, 'portion_size': 1, 'capacity': 390.0, 'type_name': 'Medium Standard Container', 'mass': 100000.0, 'race_id': None, 'group_id': 12, 'base_price': 12000}, {'market_group_id': 1657, 'description': 'A standard cargo container, used for common freight.', 'type_id': 3296, 'volume': 650.0, 'portion_size': 1, 'capacity': 780.0, 'type_name': 'Large Standard Container', 'mass': 1000000.0, 'race_id': None, 'group_id': 12, 'base_price': 27000}, {'market_group_id': 1657, 'description': 'A standard cargo container, used for common freight.', 'type_id': 3297, 'volume': 100.0, 'portion_size': 1, 'capacity': 120.0, 'type_name': 'Small Standard Container', 'mass': 10000.0, 'race_id': None, 'group_id': 12, 'base_price': 4400}]
        self.failUnlessEqual(items,
                             self.data_access_object.get_list_of_inv_items(group_id=12))

    def test_get_inv_item(self):
        '''
        Get inventory item
        '''
        item = {'market_group_id': 1657, 'description': 'A standard cargo container, used for common freight.', 'type_id': 3293, 'volume': 325.0, 'portion_size': 1, 'capacity': 390.0, 'type_name': 'Medium Standard Container', 'mass': 100000.0, 'race_id': None, 'group_id': 12, 'base_price': 12000}
        self.failUnlessEqual(item,
                             self.data_access_object.get_inv_type(type_id=3293))

    def test_get_bp_id_for_item(self):
        '''
        Get listblueprint ID for item
        '''
        blueprint = 32860
        self.failUnlessEqual(blueprint,
                             self.data_access_object.get_bp_id_for_type_id(type_id=3293))

    def test_get_lst_mat_for_rfn(self):
        '''
        Get base list of materials obtained by refining of item
        '''
        materials = [{'material_type_id': 34, 'quantity': 107}, {'material_type_id': 35, 'quantity': 213}, {'material_type_id': 36, 'quantity': 107}]
        self.failUnlessEqual(materials,
                             self.data_access_object.get_lst_mat_for_rfn(type_id=18))

    def test_get_lst_mat_for_rfn_adj(self):
        '''
        Get list of materials obtained by refining of item adjusted by skills and facility yield
        '''
        materials = [{'material_type_id': 34, 'quantity': 162}, {'material_type_id': 35, 'quantity': 323}, {'material_type_id': 36, 'quantity': 162}]
        self.failUnlessEqual(materials,
                             self.data_access_object.get_lst_mat_for_rfn_adj(type_id=18,
                                                                             fclt_base_yield=0.54,
                                                                             rprcs_skill_lvl=5,
                                                                             rprcs_eff_skill_lvl=5,
                                                                             mtrl_spcfc_prcs_skill_lvl=5,
                                                                             implant_bonus=1.02))

    def test_get_mat_for_bp(self):
        '''
        Get base list of materials for blueprint
        '''
        material = [{'material_type_id': 34, 'quantity': 1111}, {'material_type_id': 35, 'quantity': 444}]
        self.failUnlessEqual(material,
                             self.data_access_object.get_mat_for_bp(blueprint_type_id=32860))

    def test_get_time_for_bp(self):
        '''
        Get base time of building for blueprint
        '''
        time = 600
        self.failUnlessEqual(time,
                             self.data_access_object.get_time_for_blueprint(blueprint_type_id=32860))

    def test_get_lst_of_act(self):
        '''
        Get list of activities
        '''
        ram_activities = [{'activity_id': 0, 'icon_no': None, 'activity_name': 'None', 'description': 'No activity'}, {'activity_id': 1, 'icon_no': '18_02', 'activity_name': 'Manufacturing', 'description': 'Manufacturing'}, {'activity_id': 3, 'icon_no': '33_02', 'activity_name': 'Researching Time Efficiency', 'description': 'Researching time efficiency'}, {'activity_id': 4, 'icon_no': '33_02', 'activity_name': 'Researching Material Efficiency', 'description': 'Researching material efficiency'}, {'activity_id': 5, 'icon_no': '33_02', 'activity_name': 'Copying', 'description': 'Copying'}, {'activity_id': 7, 'icon_no': '33_02', 'activity_name': 'Reverse Engineering', 'description': 'The process of creating a blueprint from an item.'}, {'activity_id': 8, 'icon_no': '33_02', 'activity_name': 'Invention', 'description': 'The process of creating a more advanced item based on an existing item'}]
        self.failUnlessEqual(ram_activities,
                             self.data_access_object.get_list_of_activities())

    def test_get_lst_ram_asmb_line_types(self):
        '''
        Get list of RAM assembly line types
        '''
        ram_asmbl_line_types = [{'volume': 1.0,
                                 'base_time_multiplier': 1.0,
                                 'activity_id': 1,
                                 'min_cost_per_hour': 333.0,
                                 'description': 'STATION manufacturing',
                                 'assembly_line_type_name': 'STATION manufacturing',
                                 'assembly_line_type_id': 6,
                                 'base_cost_multiplier': 1.0,
                                 'base_material_multiplier': 1.0},
                                {'volume': 1.0,
                                 'base_time_multiplier': 1.0,
                                 'activity_id': 1,
                                 'min_cost_per_hour': None,
                                 'description': 'Capital Ship Assembly',
                                 'assembly_line_type_name': 'Capital Ship Assembly',
                                 'assembly_line_type_id': 10,
                                 'base_cost_multiplier': 1.0,
                                 'base_material_multiplier': 1.0},
                                {'volume': 1.0,
                                 'base_time_multiplier': 1.0,
                                 'activity_id': 1,
                                 'min_cost_per_hour': None,
                                 'description': 'Manufacturing',
                                 'assembly_line_type_name': 'Manufacturing',
                                 'assembly_line_type_id': 13,
                                 'base_cost_multiplier': 1.0,
                                 'base_material_multiplier': 1.0},
                                {'volume': 1.0,
                                 'base_time_multiplier': 0.75,
                                 'activity_id': 1,
                                 'min_cost_per_hour': None,
                                 'description': 'Small Ship Assembly Array\r\n',
                                 'assembly_line_type_name': 'Small Ship Assembly Array',
                                 'assembly_line_type_id': 17,
                                 'base_cost_multiplier': 1.0,
                                 'base_material_multiplier': 0.98},
                                {'volume': 1.0,
                                 'base_time_multiplier': 0.75,
                                 'activity_id': 1,
                                 'min_cost_per_hour': None,
                                 'description': 'Advanced Small Ship Assembly Array\r\n',
                                 'assembly_line_type_name': 'Advanced Small Ship Assembly Array',
                                 'assembly_line_type_id': 18,
                                 'base_cost_multiplier': 1.0,
                                 'base_material_multiplier': 0.98},
                                {'volume': 1.0, 'base_time_multiplier': 0.75, 'activity_id': 1, 'min_cost_per_hour': None, 'description': 'Medium Ship Assembly Array\r\n', 'assembly_line_type_name': 'Medium Ship Assembly Array', 'assembly_line_type_id': 19, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 0.98},
                                {'volume': 1.0, 'base_time_multiplier': 0.75, 'activity_id': 1, 'min_cost_per_hour': None, 'description': 'Advanced Medium Ship Assembly Array\r\n', 'assembly_line_type_name': 'Advanced Medium Ship Assembly Array', 'assembly_line_type_id': 20, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 0.98},
                                {'volume': 1.0, 'base_time_multiplier': 0.75, 'activity_id': 1, 'min_cost_per_hour': None, 'description': 'X Large Ship Assembly Array\r\n', 'assembly_line_type_name': 'X Large Ship Assembly Array', 'assembly_line_type_id': 21, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 0.98},
                                {'volume': 1.0, 'base_time_multiplier': 0.75, 'activity_id': 1, 'min_cost_per_hour': None, 'description': 'Advanced Large Ship Assembly Array\r\n', 'assembly_line_type_name': 'Advanced Large Ship Assembly Array', 'assembly_line_type_id': 22, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 0.98},
                                {'volume': 1.0, 'base_time_multiplier': 0.65, 'activity_id': 1, 'min_cost_per_hour': None, 'description': 'Rapid Equipment Assembly Array\r\n', 'assembly_line_type_name': 'Rapid Equipment Assembly Array', 'assembly_line_type_id': 23, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.05},
                                {'volume': 1.0, 'base_time_multiplier': 0.75, 'activity_id': 1, 'min_cost_per_hour': None, 'description': 'Equipment Assembly Array\r\n', 'assembly_line_type_name': 'Equipment Assembly Array', 'assembly_line_type_id': 24, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 0.98},
                                {'volume': 1.0, 'base_time_multiplier': 0.75, 'activity_id': 1, 'min_cost_per_hour': None, 'description': 'Ammunition Assembly Array', 'assembly_line_type_name': 'Ammunition Assembly Array', 'assembly_line_type_id': 25, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 0.98},
                                {'volume': 1.0, 'base_time_multiplier': 0.75, 'activity_id': 1, 'min_cost_per_hour': None, 'description': 'Drone Assembly Array', 'assembly_line_type_name': 'Drone Assembly Array', 'assembly_line_type_id': 26, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 0.98},
                                {'volume': 1.0, 'base_time_multiplier': 0.75, 'activity_id': 1, 'min_cost_per_hour': None, 'description': 'Component Assembly Array', 'assembly_line_type_name': 'Component Assembly Array', 'assembly_line_type_id': 27, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 0.98},
                                {'volume': 1.0, 'base_time_multiplier': 0.7, 'activity_id': 1, 'min_cost_per_hour': None, 'description': 'Amarr Outpost Manufacturing', 'assembly_line_type_name': 'Amarr Outpost Manufacturing', 'assembly_line_type_id': 31, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.0},
                                {'volume': 1.0, 'base_time_multiplier': 1.0, 'activity_id': 1, 'min_cost_per_hour': 333.0, 'description': 'STATION 0.5+ Manufacturing', 'assembly_line_type_name': 'STATION 0.5+ Manufacturing', 'assembly_line_type_id': 35, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.0},
                                {'volume': 1.0, 'base_time_multiplier': 1.0, 'activity_id': 1, 'min_cost_per_hour': None, 'description': 'Booster Manufacturing', 'assembly_line_type_name': 'Booster Manufacturing', 'assembly_line_type_id': 37, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.0},
                                {'volume': 1.0, 'base_time_multiplier': 0.7, 'activity_id': 1, 'min_cost_per_hour': None, 'description': 'Amarr Outpost w/ Type 1 Tier 1', 'assembly_line_type_name': 'Amarr Outpost Factory1 Tier1', 'assembly_line_type_id': 43, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.0},
                                {'volume': 1.0, 'base_time_multiplier': 0.7, 'activity_id': 1, 'min_cost_per_hour': None, 'description': 'Amarr Outpost w/ Type 1 Tier 1, Type 2 Tier 1', 'assembly_line_type_name': 'Amarr Outpost Factory1(2) Tier1(1)', 'assembly_line_type_id': 45, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.0},
                                {'volume': 1.0, 'base_time_multiplier': 1.0, 'activity_id': 1, 'min_cost_per_hour': None, 'description': '', 'assembly_line_type_name': 'Minmatar Outpost Factory1 Tier1', 'assembly_line_type_id': 46, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.0},
                                {'volume': 1.0, 'base_time_multiplier': 0.7, 'activity_id': 1, 'min_cost_per_hour': None, 'description': 'Amarr Outpost w/ Type 1 Tier 1, Type 2 Tier 2', 'assembly_line_type_name': 'Amarr Outpost Factory1(2) Tier1(2)', 'assembly_line_type_id': 47, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.0},
                                {'volume': 1.0, 'base_time_multiplier': 0.7, 'activity_id': 1, 'min_cost_per_hour': None, 'description': 'Amarr Outpost w/ Type 1 Tier 1, Type 2 Tier 3', 'assembly_line_type_name': 'Amarr Outpost Factory1(2) Tier1(3)', 'assembly_line_type_id': 48, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.0},
                                {'volume': 1.0, 'base_time_multiplier': 1.0, 'activity_id': 1, 'min_cost_per_hour': None, 'description': '', 'assembly_line_type_name': 'Minmatar Outpost Factory1 Tier2', 'assembly_line_type_id': 52, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.0},
                                {'volume': 1.0, 'base_time_multiplier': 0.7, 'activity_id': 1, 'min_cost_per_hour': None, 'description': 'Amarr Outpost w/ Type 1 Tier 2', 'assembly_line_type_name': 'Amarr Outpost Factory1 Tier2', 'assembly_line_type_id': 54, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.0},
                                {'volume': 1.0, 'base_time_multiplier': 0.7, 'activity_id': 1, 'min_cost_per_hour': None, 'description': 'Amarr Outpost w/ Type 1 Tier 2, Type 2 Tier 1', 'assembly_line_type_name': 'Amarr Outpost Factory1(2) Tier2(1)', 'assembly_line_type_id': 56, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.0},
                                {'volume': 1.0, 'base_time_multiplier': 0.7, 'activity_id': 1, 'min_cost_per_hour': None, 'description': 'Amarr Outpost w/ Type 1 Tier 2, Type 2 Tier 2', 'assembly_line_type_name': 'Amarr Outpost Factory1(2) Tier2(2)', 'assembly_line_type_id': 57, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.0},
                                {'volume': 1.0, 'base_time_multiplier': 0.7, 'activity_id': 1, 'min_cost_per_hour': None, 'description': 'Amarr Outpost w/ Type 1 Tier 2, Type 2 Tier 3', 'assembly_line_type_name': 'Amarr Outpost Factory1(2) Tier2(3)', 'assembly_line_type_id': 58, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.0},
                                {'volume': 1.0, 'base_time_multiplier': 0.7, 'activity_id': 1, 'min_cost_per_hour': None, 'description': 'Amarr Outpost w/ Type 1 Tier 3', 'assembly_line_type_name': 'Amarr Outpost Factory1 Tier3', 'assembly_line_type_id': 59, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.0},
                                {'volume': 1.0, 'base_time_multiplier': 0.7, 'activity_id': 1, 'min_cost_per_hour': None, 'description': 'Amarr Outpost w/ Type 1 Tier 3, Type 2 Tier 1', 'assembly_line_type_name': 'Amarr Outpost Factory1(2) Tier3(1)', 'assembly_line_type_id': 60, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.0},
                                {'volume': 1.0, 'base_time_multiplier': 0.7, 'activity_id': 1, 'min_cost_per_hour': None, 'description': 'Amarr Outpost w/ Type 1 Tier 3, Type 2 Tier 2', 'assembly_line_type_name': 'Amarr Outpost Factory1(2) Tier3(2)', 'assembly_line_type_id': 61, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.0},
                                {'volume': 1.0, 'base_time_multiplier': 1.0, 'activity_id': 1, 'min_cost_per_hour': None, 'description': '', 'assembly_line_type_name': 'Minmatar Outpost Factory1 Tier3', 'assembly_line_type_id': 62, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.0},
                                {'volume': 1.0, 'base_time_multiplier': 0.7, 'activity_id': 1, 'min_cost_per_hour': None, 'description': 'Amarr Outpost w/ Type 2 Tier 1', 'assembly_line_type_name': 'Amarr Outpost Factory2 Tier1', 'assembly_line_type_id': 66, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.0},
                                {'volume': 1.0, 'base_time_multiplier': 0.7, 'activity_id': 1, 'min_cost_per_hour': None, 'description': 'Amarr Outpost w/ Type 2 Tier 2', 'assembly_line_type_name': 'Amarr Outpost Factory2 Tier2', 'assembly_line_type_id': 67, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.0},
                                {'volume': 1.0, 'base_time_multiplier': 0.7, 'activity_id': 1, 'min_cost_per_hour': None, 'description': 'Amarr Outpost w/ Type 2 Tier 3', 'assembly_line_type_name': 'Amarr Outpost Factory2 Tier3', 'assembly_line_type_id': 68, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.0},
                                {'volume': 1.0, 'base_time_multiplier': 1.0, 'activity_id': 1, 'min_cost_per_hour': None, 'description': 'Caldari Outpost Tier 1 Factory', 'assembly_line_type_name': 'Caldari Outpost Factory Tier1', 'assembly_line_type_id': 70, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.0},
                                {'volume': 1.0, 'base_time_multiplier': 1.0, 'activity_id': 1, 'min_cost_per_hour': None, 'description': '', 'assembly_line_type_name': 'Caldari Outpost Factory Tier2', 'assembly_line_type_id': 79, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.0},
                                {'volume': 1.0, 'base_time_multiplier': 1.0, 'activity_id': 1, 'min_cost_per_hour': None, 'description': '', 'assembly_line_type_name': 'Caldari Outpost Factory Tier3', 'assembly_line_type_id': 80, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.0},
                                {'volume': 1.0, 'base_time_multiplier': 1.0, 'activity_id': 1, 'min_cost_per_hour': None, 'description': '', 'assembly_line_type_name': 'Gallente Outpost Factory1 Tier1', 'assembly_line_type_id': 93, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.0},
                                {'volume': 1.0, 'base_time_multiplier': 1.0, 'activity_id': 1, 'min_cost_per_hour': None, 'description': '', 'assembly_line_type_name': 'Gallente Outpost Factory1(2) Tier1(1)', 'assembly_line_type_id': 94, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.0},
                                {'volume': 1.0, 'base_time_multiplier': 1.0, 'activity_id': 1, 'min_cost_per_hour': None, 'description': '', 'assembly_line_type_name': 'Gallente Outpost Factory1(2) Tier1(2)', 'assembly_line_type_id': 95, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.0},
                                {'volume': 1.0, 'base_time_multiplier': 1.0, 'activity_id': 1, 'min_cost_per_hour': None, 'description': '', 'assembly_line_type_name': 'Gallente Outpost Factory1(2) Tier1(3)', 'assembly_line_type_id': 96, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.0},
                                {'volume': 1.0, 'base_time_multiplier': 1.0, 'activity_id': 1, 'min_cost_per_hour': None, 'description': '', 'assembly_line_type_name': 'Gallente Outpost Factory1(2) Tier2(1)', 'assembly_line_type_id': 98, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.0},
                                {'volume': 1.0, 'base_time_multiplier': 1.0, 'activity_id': 1, 'min_cost_per_hour': None, 'description': '', 'assembly_line_type_name': 'Gallente Outpost Factory1(2) Tier2(2)', 'assembly_line_type_id': 99, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.0},
                                {'volume': 1.0, 'base_time_multiplier': 1.0, 'activity_id': 1, 'min_cost_per_hour': None, 'description': '', 'assembly_line_type_name': 'Gallente Outpost Factory1(2) Tier2(3)', 'assembly_line_type_id': 100, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.0},
                                {'volume': 1.0, 'base_time_multiplier': 1.0, 'activity_id': 1, 'min_cost_per_hour': None, 'description': '', 'assembly_line_type_name': 'Gallente Outpost Factory1(2) Tier3(1)', 'assembly_line_type_id': 102, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.0},
                                {'volume': 1.0, 'base_time_multiplier': 1.0, 'activity_id': 1, 'min_cost_per_hour': None, 'description': '', 'assembly_line_type_name': 'Gallente Outpost Factory1(2) Tier3(2)', 'assembly_line_type_id': 103, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.0},
                                {'volume': 1.0, 'base_time_multiplier': 1.0, 'activity_id': 1, 'min_cost_per_hour': None, 'description': '', 'assembly_line_type_name': 'Gallente Outpost Factory2 Tier1', 'assembly_line_type_id': 104, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.0},
                                {'volume': 1.0, 'base_time_multiplier': 1.0, 'activity_id': 1, 'min_cost_per_hour': None, 'description': '', 'assembly_line_type_name': 'Gallente Outpost Factory2 Tier2', 'assembly_line_type_id': 105, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.0},
                                {'volume': 1.0, 'base_time_multiplier': 1.0, 'activity_id': 1, 'min_cost_per_hour': None, 'description': '', 'assembly_line_type_name': 'Gallente Outpost Factory2 Tier3', 'assembly_line_type_id': 106, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.0},
                                {'volume': 1.0, 'base_time_multiplier': 1.0, 'activity_id': 1, 'min_cost_per_hour': None, 'description': '', 'assembly_line_type_name': 'Minmatar Outpost Factory1(2) Tier1(1)', 'assembly_line_type_id': 116, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.0},
                                {'volume': 1.0, 'base_time_multiplier': 1.0, 'activity_id': 1, 'min_cost_per_hour': None, 'description': '', 'assembly_line_type_name': 'Minmatar Outpost Factory1(2) Tier1(2)', 'assembly_line_type_id': 117, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.0},
                                {'volume': 1.0, 'base_time_multiplier': 1.0, 'activity_id': 1, 'min_cost_per_hour': None, 'description': '', 'assembly_line_type_name': 'Minmatar Outpost Factory1(2) Tier1(3)', 'assembly_line_type_id': 118, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.0},
                                {'volume': 1.0, 'base_time_multiplier': 1.0, 'activity_id': 1, 'min_cost_per_hour': None, 'description': '', 'assembly_line_type_name': 'Minmatar Outpost Factory1(2) Tier2(1)', 'assembly_line_type_id': 119, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.0},
                                {'volume': 1.0, 'base_time_multiplier': 1.0, 'activity_id': 1, 'min_cost_per_hour': None, 'description': '', 'assembly_line_type_name': 'Minmatar Outpost Factory1(2) Tier2(2)', 'assembly_line_type_id': 120, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.0},
                                {'volume': 1.0, 'base_time_multiplier': 1.0, 'activity_id': 1, 'min_cost_per_hour': None, 'description': '', 'assembly_line_type_name': 'Minmatar Outpost Factory1(2) Tier2(3)', 'assembly_line_type_id': 121, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.0},
                                {'volume': 1.0, 'base_time_multiplier': 1.0, 'activity_id': 1, 'min_cost_per_hour': None, 'description': '', 'assembly_line_type_name': 'Minmatar Outpost Factory1(2) Tier3(1)', 'assembly_line_type_id': 122, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.0},
                                {'volume': 1.0, 'base_time_multiplier': 1.0, 'activity_id': 1, 'min_cost_per_hour': None, 'description': '', 'assembly_line_type_name': 'Minmatar Outpost Factory1(2) Tier3(2)', 'assembly_line_type_id': 123, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.0},
                                {'volume': 1.0, 'base_time_multiplier': 1.0, 'activity_id': 1, 'min_cost_per_hour': None, 'description': '', 'assembly_line_type_name': 'Minmatar Outpost Factory2 Tier1', 'assembly_line_type_id': 124, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.0},
                                {'volume': 1.0, 'base_time_multiplier': 1.0, 'activity_id': 1, 'min_cost_per_hour': None, 'description': '', 'assembly_line_type_name': 'Minmatar Outpost Factory2 Tier2', 'assembly_line_type_id': 125, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.0},
                                {'volume': 1.0, 'base_time_multiplier': 1.0, 'activity_id': 1, 'min_cost_per_hour': None, 'description': '', 'assembly_line_type_name': 'Minmatar Outpost Factory2 Tier3', 'assembly_line_type_id': 126, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.0},
                                {'volume': 1.0, 'base_time_multiplier': 1.0, 'activity_id': 1, 'min_cost_per_hour': None, 'description': '', 'assembly_line_type_name': 'Gallente Outpost Factory1 Tier3', 'assembly_line_type_id': 136, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.0},
                                {'volume': 1.0, 'base_time_multiplier': 1.0, 'activity_id': 1, 'min_cost_per_hour': None, 'description': '', 'assembly_line_type_name': 'Gallente Outpost Factory1 Tier2', 'assembly_line_type_id': 137, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.0},
                                {'volume': 1.0, 'base_time_multiplier': 1.0, 'activity_id': 1, 'min_cost_per_hour': None, 'description': 'ore cap ship asteroid line', 'assembly_line_type_name': 'Ore Capital Ship', 'assembly_line_type_id': 145, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.0},
                                {'volume': 1.0, 'base_time_multiplier': 0.8, 'activity_id': 1, 'min_cost_per_hour': None, 'description': 'ore cap ship manufacture lines', 'assembly_line_type_name': 'Ore Cap Ship Manufacturing', 'assembly_line_type_id': 150, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.0},
                                {'volume': 1.0, 'base_time_multiplier': 0.75, 'activity_id': 1, 'min_cost_per_hour': None, 'description': 'Large ship assembly array for manufacture of battleships, freighters ', 'assembly_line_type_name': 'Large Ship Assembly Array', 'assembly_line_type_id': 155, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 0.98},
                                {'volume': 1.0, 'base_time_multiplier': 1.0, 'activity_id': 1, 'min_cost_per_hour': None, 'description': 'Advanced Subsystem Assembly Array', 'assembly_line_type_name': 'Advanced Subsystem Assembly Array', 'assembly_line_type_id': 159, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.0},
                                {'volume': 1.0, 'base_time_multiplier': 1.0, 'activity_id': 1, 'min_cost_per_hour': None, 'description': 'Subsystem Manufacturing', 'assembly_line_type_name': 'Subsystem Manufacturing', 'assembly_line_type_id': 161, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.0},
                                {'volume': 1.0, 'base_time_multiplier': 0.75, 'activity_id': 1, 'min_cost_per_hour': None, 'description': 'This assembly array is implemented in or around Kronos, in order to buffer lowsec capital producers from the impact of the refining changes. Gives an increased ME bonus, can only be anchored in lowsec.', 'assembly_line_type_name': 'Thukker Component Assembly Array', 'assembly_line_type_id': 171, 'base_cost_multiplier': 1.0, 'base_material_multiplier': 0.85},
                                {'activity_id': 1, 'assembly_line_type_id': 172, 'assembly_line_type_name': 'Thera Manufacturing', 'base_cost_multiplier': 1.0, 'base_material_multiplier': 1.0, 'base_time_multiplier': 1.0, 'description': 'Thera Manufacturing (WH station)', 'min_cost_per_hour': None, 'volume': 1.0}]
        self.failUnlessEqual(ram_asmbl_line_types,
                             self.data_access_object.get_lst_ram_asmb_line_types())

    def test_get_dtl_ram_asmb_line_types(self):
        '''
        Get RAM assembly line type
        '''
        asmbl_line_type = {'volume': 1.0, 'base_time_multiplier': 0.75, 'activity_id': 1, 'assembly_line_type_name': 'Medium Ship Assembly Array', 'min_cost_per_hour': None, 'description': 'Medium Ship Assembly Array\r\n', 'base_material_multiplier': 0.98, 'base_cost_multiplier': 1.0, 'assembly_line_type_id': 19}
        self.failUnlessEqual(asmbl_line_type,
                             self.data_access_object.get_dtl_ram_asmb_line_types(assembly_line_type_name='Medium Ship Assembly Array'))


if __name__ == "__main__":
    unittest.main()

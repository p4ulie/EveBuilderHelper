'''
Created on 14.1.2014

@author: paulie
'''

import unittest
from DBAccessSQLite import DBAccessSQLite
from EveModules.EveDB import *

class TestEveDB(unittest.TestCase):

    DB = '../data/eve.db'
    eveDB = None
    
    def setUp(self):
        self.dbAccess = DBAccessSQLite(self.DB)
        self.eveDB = EveDB(self.dbAccess)

    def tearDown(self):
        self.dbAccess.close()

    def testGetListOfInvCategories(self):
        categories = {2: {'description': '', 'iconID': None, 'categoryID': 2, 'categoryName': 'Celestial'}, 4: {'description': '', 'iconID': 22, 'categoryID': 4, 'categoryName': 'Material'}, 5: {'description': '', 'iconID': 33, 'categoryID': 5, 'categoryName': 'Accessories'}, 6: {'description': '', 'iconID': None, 'categoryID': 6, 'categoryName': 'Ship'}, 7: {'description': '', 'iconID': 67, 'categoryID': 7, 'categoryName': 'Module'}, 8: {'description': '', 'iconID': None, 'categoryID': 8, 'categoryName': 'Charge'}, 9: {'description': '', 'iconID': 21, 'categoryID': 9, 'categoryName': 'Blueprint'}, 16: {'description': 'Where all the skills go under.', 'iconID': 33, 'categoryID': 16, 'categoryName': 'Skill'}, 17: {'description': '', 'iconID': 0, 'categoryID': 17, 'categoryName': 'Commodity'}, 18: {'description': 'Player owned and controlled drones.', 'iconID': 0, 'categoryID': 18, 'categoryName': 'Drone'}, 20: {'description': 'Implant', 'iconID': 0, 'categoryID': 20, 'categoryName': 'Implant'}, 22: {'description': '', 'iconID': 0, 'categoryID': 22, 'categoryName': 'Deployable'}, 23: {'description': 'Player owned structure related objects', 'iconID': 0, 'categoryID': 23, 'categoryName': 'Structure'}, 24: {'description': '', 'iconID': 0, 'categoryID': 24, 'categoryName': 'Reaction'}, 25: {'description': '', 'iconID': None, 'categoryID': 25, 'categoryName': 'Asteroid'}, 30: {'description': '1. clothing, especially outerwear; garments; attire; raiment.\r\n2. anything that decorates or covers.\r\n3. superficial appearance; aspect; guise. ', 'iconID': None, 'categoryID': 30, 'categoryName': 'Apparel'}, 32: {'description': 'Subsystems for tech 3 ships', 'iconID': None, 'categoryID': 32, 'categoryName': 'Subsystem'}, 34: {'description': '', 'iconID': None, 'categoryID': 34, 'categoryName': 'Ancient Relics'}, 35: {'description': '', 'iconID': None, 'categoryID': 35, 'categoryName': 'Decryptors'}, 39: {'description': '', 'iconID': None, 'categoryID': 39, 'categoryName': 'Infrastructure Upgrades'}, 40: {'description': '', 'iconID': None, 'categoryID': 40, 'categoryName': 'Sovereignty Structures'}, 41: {'description': 'Stuff for planetary interaction', 'iconID': None, 'categoryID': 41, 'categoryName': 'Planetary Interaction'}, 42: {'description': 'These are Items that can be extracted from a planet. ', 'iconID': None, 'categoryID': 42, 'categoryName': 'Planetary Resources'}, 43: {'description': '', 'iconID': None, 'categoryID': 43, 'categoryName': 'Planetary Commodities'}, 46: {'description': 'Anchorable/Onlinable objects that operate similar to POS/SOV structures, but do not link to towers or sovereignty. Each class of orbital defines its own valid anchoring locations via Python code.', 'iconID': None, 'categoryID': 46, 'categoryName': 'Orbitals'}, 63: {'description': 'Special Edition Assets', 'iconID': None, 'categoryID': 63, 'categoryName': 'Special Edition Assets'}}
        self.failUnlessEqual(categories,
                             self.eveDB.getListOfInvCategories())

    def testGetListOfInvGroups(self):
        groups = {448: {'groupName': 'Audit Log Secure Container', 'description': '', 'iconID': None, 'groupID': 448, 'categoryID': 2}, 835: {'groupName': 'Station Upgrade Platform', 'description': '', 'iconID': 0, 'groupID': 835, 'categoryID': 2}, 836: {'groupName': 'Station Improvement Platform', 'description': '', 'iconID': 0, 'groupID': 836, 'categoryID': 2}, 711: {'groupName': 'Harvestable Cloud', 'description': '', 'iconID': 0, 'groupID': 711, 'categoryID': 2}, 649: {'groupName': 'Freight Container', 'description': 'Freight Containers are commonly used in Freighter-class ships to accomodate their massive cargobays.', 'iconID': 1174, 'groupID': 649, 'categoryID': 2}, 12: {'groupName': 'Cargo Container', 'description': '', 'iconID': 16, 'groupID': 12, 'categoryID': 2}, 1165: {'groupName': 'Satellite', 'description': '', 'iconID': None, 'groupID': 1165, 'categoryID': 2}, 14: {'groupName': 'Biomass', 'description': 'Corpse of human. Can be sold for clone production.', 'iconID': 0, 'groupID': 14, 'categoryID': 2}, 1071: {'groupName': 'Flashpoint', 'description': 'Points of conflict on a planet.', 'iconID': None, 'groupID': 1071, 'categoryID': 2}, 307: {'groupName': 'Construction Platform', 'description': '', 'iconID': 0, 'groupID': 307, 'categoryID': 2}, 340: {'groupName': 'Secure Cargo Container', 'description': '', 'iconID': 0, 'groupID': 340, 'categoryID': 2}, 1198: {'groupName': 'Orbital Target', 'description': 'Orbital targets are locations on the ground lockable by ships.', 'iconID': None, 'groupID': 1198, 'categoryID': 2}}
        self.failUnlessEqual(groups,
                             self.eveDB.getListOfInvGroups(categoryID = 2))

    def testGetListOfInvItems(self):
        items =  {3296: {'description': 'A standard cargo container, used for common freight.', 'raceID': None, 'marketGroupID': 3296, 'volume': 650.0, 'typeName': 'Large Standard Container', 'typeID': 3296, 'capacity': 780.0, 'mass': 1000000.0, 'basePrice': 27000, 'portionSize': 1, 'groupID': 12}, 3297: {'description': 'A standard cargo container, used for common freight.', 'raceID': None, 'marketGroupID': 3297, 'volume': 100.0, 'typeName': 'Small Standard Container', 'typeID': 3297, 'capacity': 120.0, 'mass': 10000.0, 'basePrice': 4400, 'portionSize': 1, 'groupID': 12}, 3293: {'description': 'A standard cargo container, used for common freight.', 'raceID': None, 'marketGroupID': 3293, 'volume': 325.0, 'typeName': 'Medium Standard Container', 'typeID': 3293, 'capacity': 390.0, 'mass': 100000.0, 'basePrice': 12000, 'portionSize': 1, 'groupID': 12}}
        self.failUnlessEqual(items,
                             self.eveDB.getListOfInvItems(groupID = 12))

    def testGetInvItem(self):
        item =  {3293: {'basePrice': 12000, 'capacity': 390.0, 'description': 'A standard cargo container, used for common freight.', 'groupID': 12, 'marketGroupID': 3293, 'mass': 100000.0, 'portionSize': 1, 'raceID': None, 'typeID': 3293, 'typeName': 'Medium Standard Container', 'volume': 325.0}}
        self.failUnlessEqual(item,
                             self.eveDB.getInvItem(typeID = 3293))

    def testGetBlueprintIDForItem(self):
        blueprint =  32860
        self.failUnlessEqual(blueprint,
                             self.eveDB.getBlueprintIDForItem(typeID = 3293))

    def testGetMaterialsForBlueprint(self):
        material =  {34: {'materialTypeID': 34, 'consume': 1, 'quantity': 1111}, 35: {'materialTypeID': 35, 'consume': 1, 'quantity': 444}}
        self.failUnlessEqual(material,
                             self.eveDB.getMaterialsForBlueprint(blueprintTypeID = 32860))

    def testGetTimeForBlueprint(self):
        time =  600
        self.failUnlessEqual(time,
                             self.eveDB.getTimeForBlueprint(blueprintTypeID = 32860))

    def testGetListOfRamActivities(self):
        ramActivities =  {0: {'activityID': 0, 'iconNo': None, 'description': 'No activity', 'activityName': 'None'}, 1: {'activityID': 1, 'iconNo': '18_02', 'description': 'Manufacturing', 'activityName': 'Manufacturing'}, 3: {'activityID': 3, 'iconNo': '33_02', 'description': 'Researching time efficiency', 'activityName': 'Researching Time Efficiency'}, 4: {'activityID': 4, 'iconNo': '33_02', 'description': 'Researching material efficiency', 'activityName': 'Researching Material Efficiency'}, 5: {'activityID': 5, 'iconNo': '33_02', 'description': 'Copying', 'activityName': 'Copying'}, 7: {'activityID': 7, 'iconNo': '33_02', 'description': 'The process of creating a blueprint from an item.', 'activityName': 'Reverse Engineering'}, 8: {'activityID': 8, 'iconNo': '33_02', 'description': 'The process of creating a more advanced item based on an existing item', 'activityName': 'Invention'}}
        self.failUnlessEqual(ramActivities,
                             self.eveDB.getListOfRamActivities())

    def testGetListOfRamAssemblyLineTypes(self):
        ramAssemblyLineTypes = {155: {'baseMaterialMultiplier': 0.98, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Large Ship Assembly Array', 'description': 'Large ship assembly array for manufacture of battleships, freighters ', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 0.75, 'assemblyLineTypeID': 155, 'minCostPerHour': None}, 150: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Ore Cap Ship Manufacturing', 'description': 'ore cap ship manufacture lines', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 0.8, 'assemblyLineTypeID': 150, 'minCostPerHour': None}, 6: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'STATION manufacturing', 'description': 'STATION manufacturing', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 1.0, 'assemblyLineTypeID': 6, 'minCostPerHour': 333.0}, 136: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Gallente Outpost Factory1 Tier3', 'description': '', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 1.0, 'assemblyLineTypeID': 136, 'minCostPerHour': None}, 137: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Gallente Outpost Factory1 Tier2', 'description': '', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 1.0, 'assemblyLineTypeID': 137, 'minCostPerHour': None}, 10: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Capital Ship Assembly', 'description': 'Capital Ship Assembly', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 1.0, 'assemblyLineTypeID': 10, 'minCostPerHour': None}, 13: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Manufacturing', 'description': 'Manufacturing', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 1.0, 'assemblyLineTypeID': 13, 'minCostPerHour': None}, 17: {'baseMaterialMultiplier': 0.98, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Small Ship Assembly Array', 'description': 'Small Ship Assembly Array\r\n', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 0.75, 'assemblyLineTypeID': 17, 'minCostPerHour': None}, 18: {'baseMaterialMultiplier': 0.98, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Advanced Small Ship Assembly Array', 'description': 'Advanced Small Ship Assembly Array\r\n', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 0.75, 'assemblyLineTypeID': 18, 'minCostPerHour': None}, 19: {'baseMaterialMultiplier': 0.98, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Medium Ship Assembly Array', 'description': 'Medium Ship Assembly Array\r\n', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 0.75, 'assemblyLineTypeID': 19, 'minCostPerHour': None}, 20: {'baseMaterialMultiplier': 0.98, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Advanced Medium Ship Assembly Array', 'description': 'Advanced Medium Ship Assembly Array\r\n', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 0.75, 'assemblyLineTypeID': 20, 'minCostPerHour': None}, 21: {'baseMaterialMultiplier': 0.98, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'X Large Ship Assembly Array', 'description': 'X Large Ship Assembly Array\r\n', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 0.75, 'assemblyLineTypeID': 21, 'minCostPerHour': None}, 22: {'baseMaterialMultiplier': 0.98, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Advanced Large Ship Assembly Array', 'description': 'Advanced Large Ship Assembly Array\r\n', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 0.75, 'assemblyLineTypeID': 22, 'minCostPerHour': None}, 23: {'baseMaterialMultiplier': 1.05, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Rapid Equipment Assembly Array', 'description': 'Rapid Equipment Assembly Array\r\n', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 0.65, 'assemblyLineTypeID': 23, 'minCostPerHour': None}, 24: {'baseMaterialMultiplier': 0.98, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Equipment Assembly Array', 'description': 'Equipment Assembly Array\r\n', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 0.75, 'assemblyLineTypeID': 24, 'minCostPerHour': None}, 25: {'baseMaterialMultiplier': 0.98, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Ammunition Assembly Array', 'description': 'Ammunition Assembly Array', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 0.75, 'assemblyLineTypeID': 25, 'minCostPerHour': None}, 26: {'baseMaterialMultiplier': 0.98, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Drone Assembly Array', 'description': 'Drone Assembly Array', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 0.75, 'assemblyLineTypeID': 26, 'minCostPerHour': None}, 27: {'baseMaterialMultiplier': 0.98, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Component Assembly Array', 'description': 'Component Assembly Array', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 0.75, 'assemblyLineTypeID': 27, 'minCostPerHour': None}, 31: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Amarr Outpost Manufacturing', 'description': 'Amarr Outpost Manufacturing', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 0.7, 'assemblyLineTypeID': 31, 'minCostPerHour': None}, 161: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Subsystem Manufacturing', 'description': 'Subsystem Manufacturing', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 1.0, 'assemblyLineTypeID': 161, 'minCostPerHour': None}, 35: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'STATION 0.5+ Manufacturing', 'description': 'STATION 0.5+ Manufacturing', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 1.0, 'assemblyLineTypeID': 35, 'minCostPerHour': 333.0}, 37: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Booster Manufacturing', 'description': 'Booster Manufacturing', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 1.0, 'assemblyLineTypeID': 37, 'minCostPerHour': None}, 145: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Ore Capital Ship', 'description': 'ore cap ship asteroid line', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 1.0, 'assemblyLineTypeID': 145, 'minCostPerHour': None}, 43: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Amarr Outpost Factory1 Tier1', 'description': 'Amarr Outpost w/ Type 1 Tier 1', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 0.7, 'assemblyLineTypeID': 43, 'minCostPerHour': None}, 159: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Advanced Subsystem Assembly Array', 'description': 'Advanced Subsystem Assembly Array', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 1.0, 'assemblyLineTypeID': 159, 'minCostPerHour': None}, 45: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Amarr Outpost Factory1(2) Tier1(1)', 'description': 'Amarr Outpost w/ Type 1 Tier 1, Type 2 Tier 1', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 0.7, 'assemblyLineTypeID': 45, 'minCostPerHour': None}, 46: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Minmatar Outpost Factory1 Tier1', 'description': '', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 1.0, 'assemblyLineTypeID': 46, 'minCostPerHour': None}, 47: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Amarr Outpost Factory1(2) Tier1(2)', 'description': 'Amarr Outpost w/ Type 1 Tier 1, Type 2 Tier 2', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 0.7, 'assemblyLineTypeID': 47, 'minCostPerHour': None}, 48: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Amarr Outpost Factory1(2) Tier1(3)', 'description': 'Amarr Outpost w/ Type 1 Tier 1, Type 2 Tier 3', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 0.7, 'assemblyLineTypeID': 48, 'minCostPerHour': None}, 52: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Minmatar Outpost Factory1 Tier2', 'description': '', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 1.0, 'assemblyLineTypeID': 52, 'minCostPerHour': None}, 54: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Amarr Outpost Factory1 Tier2', 'description': 'Amarr Outpost w/ Type 1 Tier 2', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 0.7, 'assemblyLineTypeID': 54, 'minCostPerHour': None}, 56: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Amarr Outpost Factory1(2) Tier2(1)', 'description': 'Amarr Outpost w/ Type 1 Tier 2, Type 2 Tier 1', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 0.7, 'assemblyLineTypeID': 56, 'minCostPerHour': None}, 57: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Amarr Outpost Factory1(2) Tier2(2)', 'description': 'Amarr Outpost w/ Type 1 Tier 2, Type 2 Tier 2', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 0.7, 'assemblyLineTypeID': 57, 'minCostPerHour': None}, 58: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Amarr Outpost Factory1(2) Tier2(3)', 'description': 'Amarr Outpost w/ Type 1 Tier 2, Type 2 Tier 3', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 0.7, 'assemblyLineTypeID': 58, 'minCostPerHour': None}, 59: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Amarr Outpost Factory1 Tier3', 'description': 'Amarr Outpost w/ Type 1 Tier 3', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 0.7, 'assemblyLineTypeID': 59, 'minCostPerHour': None}, 60: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Amarr Outpost Factory1(2) Tier3(1)', 'description': 'Amarr Outpost w/ Type 1 Tier 3, Type 2 Tier 1', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 0.7, 'assemblyLineTypeID': 60, 'minCostPerHour': None}, 61: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Amarr Outpost Factory1(2) Tier3(2)', 'description': 'Amarr Outpost w/ Type 1 Tier 3, Type 2 Tier 2', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 0.7, 'assemblyLineTypeID': 61, 'minCostPerHour': None}, 62: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Minmatar Outpost Factory1 Tier3', 'description': '', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 1.0, 'assemblyLineTypeID': 62, 'minCostPerHour': None}, 66: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Amarr Outpost Factory2 Tier1', 'description': 'Amarr Outpost w/ Type 2 Tier 1', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 0.7, 'assemblyLineTypeID': 66, 'minCostPerHour': None}, 67: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Amarr Outpost Factory2 Tier2', 'description': 'Amarr Outpost w/ Type 2 Tier 2', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 0.7, 'assemblyLineTypeID': 67, 'minCostPerHour': None}, 68: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Amarr Outpost Factory2 Tier3', 'description': 'Amarr Outpost w/ Type 2 Tier 3', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 0.7, 'assemblyLineTypeID': 68, 'minCostPerHour': None}, 70: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Caldari Outpost Factory Tier1', 'description': 'Caldari Outpost Tier 1 Factory', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 1.0, 'assemblyLineTypeID': 70, 'minCostPerHour': None}, 79: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Caldari Outpost Factory Tier2', 'description': '', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 1.0, 'assemblyLineTypeID': 79, 'minCostPerHour': None}, 80: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Caldari Outpost Factory Tier3', 'description': '', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 1.0, 'assemblyLineTypeID': 80, 'minCostPerHour': None}, 93: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Gallente Outpost Factory1 Tier1', 'description': '', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 1.0, 'assemblyLineTypeID': 93, 'minCostPerHour': None}, 94: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Gallente Outpost Factory1(2) Tier1(1)', 'description': '', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 1.0, 'assemblyLineTypeID': 94, 'minCostPerHour': None}, 95: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Gallente Outpost Factory1(2) Tier1(2)', 'description': '', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 1.0, 'assemblyLineTypeID': 95, 'minCostPerHour': None}, 96: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Gallente Outpost Factory1(2) Tier1(3)', 'description': '', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 1.0, 'assemblyLineTypeID': 96, 'minCostPerHour': None}, 171: {'baseMaterialMultiplier': 0.85, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Thukker Component Assembly Array', 'description': 'This assembly array is implemented in or around Kronos, in order to buffer lowsec capital producers from the impact of the refining changes. Gives an increased ME bonus, can only be anchored in lowsec.', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 0.75, 'assemblyLineTypeID': 171, 'minCostPerHour': None}, 98: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Gallente Outpost Factory1(2) Tier2(1)', 'description': '', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 1.0, 'assemblyLineTypeID': 98, 'minCostPerHour': None}, 99: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Gallente Outpost Factory1(2) Tier2(2)', 'description': '', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 1.0, 'assemblyLineTypeID': 99, 'minCostPerHour': None}, 100: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Gallente Outpost Factory1(2) Tier2(3)', 'description': '', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 1.0, 'assemblyLineTypeID': 100, 'minCostPerHour': None}, 102: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Gallente Outpost Factory1(2) Tier3(1)', 'description': '', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 1.0, 'assemblyLineTypeID': 102, 'minCostPerHour': None}, 103: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Gallente Outpost Factory1(2) Tier3(2)', 'description': '', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 1.0, 'assemblyLineTypeID': 103, 'minCostPerHour': None}, 104: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Gallente Outpost Factory2 Tier1', 'description': '', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 1.0, 'assemblyLineTypeID': 104, 'minCostPerHour': None}, 105: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Gallente Outpost Factory2 Tier2', 'description': '', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 1.0, 'assemblyLineTypeID': 105, 'minCostPerHour': None}, 106: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Gallente Outpost Factory2 Tier3', 'description': '', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 1.0, 'assemblyLineTypeID': 106, 'minCostPerHour': None}, 116: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Minmatar Outpost Factory1(2) Tier1(1)', 'description': '', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 1.0, 'assemblyLineTypeID': 116, 'minCostPerHour': None}, 117: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Minmatar Outpost Factory1(2) Tier1(2)', 'description': '', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 1.0, 'assemblyLineTypeID': 117, 'minCostPerHour': None}, 118: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Minmatar Outpost Factory1(2) Tier1(3)', 'description': '', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 1.0, 'assemblyLineTypeID': 118, 'minCostPerHour': None}, 119: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Minmatar Outpost Factory1(2) Tier2(1)', 'description': '', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 1.0, 'assemblyLineTypeID': 119, 'minCostPerHour': None}, 120: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Minmatar Outpost Factory1(2) Tier2(2)', 'description': '', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 1.0, 'assemblyLineTypeID': 120, 'minCostPerHour': None}, 121: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Minmatar Outpost Factory1(2) Tier2(3)', 'description': '', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 1.0, 'assemblyLineTypeID': 121, 'minCostPerHour': None}, 122: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Minmatar Outpost Factory1(2) Tier3(1)', 'description': '', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 1.0, 'assemblyLineTypeID': 122, 'minCostPerHour': None}, 123: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Minmatar Outpost Factory1(2) Tier3(2)', 'description': '', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 1.0, 'assemblyLineTypeID': 123, 'minCostPerHour': None}, 124: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Minmatar Outpost Factory2 Tier1', 'description': '', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 1.0, 'assemblyLineTypeID': 124, 'minCostPerHour': None}, 125: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Minmatar Outpost Factory2 Tier2', 'description': '', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 1.0, 'assemblyLineTypeID': 125, 'minCostPerHour': None}, 126: {'baseMaterialMultiplier': 1.0, 'volume': 1.0, 'activityID': 1, 'assemblyLineTypeName': 'Minmatar Outpost Factory2 Tier3', 'description': '', 'baseCostMultiplier': 1.0, 'baseTimeMultiplier': 1.0, 'assemblyLineTypeID': 126, 'minCostPerHour': None}}
        self.failUnlessEqual(ramAssemblyLineTypes,
                             self.eveDB.getListOfRamAssemblyLineTypes())

    def testGetActivityBonusForRamAssemblyLineType(self):
        bonuses = {'baseTimeMultiplier': 0.75, 'volume': 1.0, 'activityID': 1, 'baseCostMultiplier': 1.0, 'baseMaterialMultiplier': 0.98, 'minCostPerHour': None}
        self.failUnlessEqual(bonuses,
                             self.eveDB.getActivityBonusForRamAssemblyLineType(assemblyLineTypeName = 'Medium Ship Assembly Array'))

    
if __name__ == "__main__":
    unittest.main()

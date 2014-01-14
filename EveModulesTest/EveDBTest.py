'''
Created on 14.1.2014

@author: paulie
'''
import unittest
from EveModules.EveDB import *

class TestEveDB(unittest.TestCase):

    DB = 'Data/ody100-sqlite3-v1.db'
    eveDB = None
    
    def setUp(self):
        self.eveDB = EveDB(self.DB)


    def tearDown(self):
        pass

    def testFetchData(self):
        query = """
                    SELECT count(*)
                    FROM invTypes AS t
                    WHERE t.published = '1'
                """
        publishedItemsCount = 13418
        self.failUnlessEqual(publishedItemsCount,
                             self.eveDB.fetchData(query)[0][0])

    def testGetGroupsList(self):
        groups = [(12, 2, u'Cargo Container', u''), (14, 2, u'Biomass', u'Corpse of human. Can be sold for clone production.'), (307, 2, u'Construction Platform', u''), (340, 2, u'Secure Cargo Container', u''), (448, 2, u'Audit Log Secure Container', u''), (649, 2, u'Freight Container', u'Freight Containers are commonly used in Freighter-class ships to accomodate their massive cargobays.'), (711, 2, u'Harvestable Cloud', u''), (835, 2, u'Station Upgrade Platform', u''), (836, 2, u'Station Improvement Platform', u''), (1071, 2, u'Flashpoint', u'Points of conflict on a planet.'), (1165, 2, u'Satellite', u''), (1198, 2, u'Orbital Target', u'Orbital targets are locations on the ground lockable by ships.')]
        self.failUnlessEqual(groups,
                             self.eveDB.getGroupsList(categoryID = 2))


    def testGetCategoriesList(self):
        categories = [(2, u'Celestial', u''), (4, u'Material', u''), (5, u'Accessories', u''), (6, u'Ship', u''), (7, u'Module', u''), (8, u'Charge', u''), (9, u'Blueprint', u''), (16, u'Skill', u'Where all the skills go under.'), (17, u'Commodity', u''), (18, u'Drone', u'Player owned and controlled drones.'), (20, u'Implant', u'Implant'), (22, u'Deployable', u''), (23, u'Structure', u'Player owned structure related objects'), (24, u'Reaction', u''), (25, u'Asteroid', u''), (30, u'Apparel', u'1. clothing, especially outerwear; garments; attire; raiment.\n2. anything that decorates or covers.\n3. superficial appearance; aspect; guise. '), (32, u'Subsystem', u'Subsystems for tech 3 ships'), (34, u'Ancient Relics', u''), (35, u'Decryptors', u''), (39, u'Infrastructure Upgrades', u''), (40, u'Sovereignty Structures', u''), (41, u'Planetary Interaction', u'Stuff for planetary interaction'), (42, u'Planetary Resources', u'These are Items that can be extracted from a planet. '), (43, u'Planetary Commodities', u''), (46, u'Orbitals', u'Anchorable/Onlinable objects that operate similar to POS/SOV structures, but do not link to towers or sovereignty. Each class of orbital defines its own valid anchoring locations via Python code.'), (63, u'Special Edition Assets', u'Special Edition Assets')]
        self.failUnlessEqual(categories,
                             self.eveDB.getCategoriesList())


    def testGetItemsList(self):
        items = [(3293, 12, u'Medium Standard Container', u'A standard cargo container, used for common freight.', 100000.0, 325.0, 390.0, 1, None, 12000.0, 1, 1657, 0.0), (3296, 12, u'Large Standard Container', u'A standard cargo container, used for common freight.', 1000000.0, 650.0, 780.0, 1, None, 27000.0, 1, 1657, 0.0), (3297, 12, u'Small Standard Container', u'A standard cargo container, used for common freight.', 10000.0, 100.0, 120.0, 1, None, 4400.0, 1, 1657, 0.0)]
        self.failUnlessEqual(items,
                             self.eveDB.getItemsList(groupID = 12))


if __name__ == "__main__":
    unittest.main()

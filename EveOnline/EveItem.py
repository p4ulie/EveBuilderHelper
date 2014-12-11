'''
Created on Sep 15, 2014

@author: paulie
'''


#import math
from EveOnline.EveDB import EveDB
#from EveOnline.EveMathConstants import EVE_ACTIVITY_MANUFACTURING
#from EveOnline import EveMathIndustry


class EveItem(EveDB):
    '''
    Class for data and methods for Items in Eve Online
    '''

    def __init__(self, db_access_obj, type_id=None, type_name=None):
        '''
        Constructor
        '''

        # basic item attributes
        self.type_id = None
        self.group_id = None
        self.category_id = None
        self.type_name = ''
        self.description = ''
        self.mass = None
        self.volume = None
        self.capacity = None
        self.portion_size = None
        self.race_id = None
        self.base_price = None
        self.market_group_id = None

        self.graphic_id = None
        self.radius = None
        self.published = None
        self.chance_of_duplicating = None

        self.meta_group = None

        # manufacturing related attributes
        self.parent = None   # reference to parent object
        self.blueprint_type_id = None   # determines whether item is buildable
        self.blueprint_me_level = 10
        self.blueprint_te_level = 20

        self.manufacturing_quantity = 0

        self.build_queue_level = 0  # order in which materials have to be build

        self.asset_list = {}  # asset list to calculate in (need to buy less)

        self.assembly_line_type_id = None   # assembly line used, for bonuses

        self.material_list = []

        # initialize object and get basic data
        EveDB.__init__(self, db_access_obj)

        self.get_item(type_id=type_id, type_name=type_name)

    def get_item(self, type_id=None, type_name=None):
        '''
        Get item by ID or name
        '''

        item = self.get_inv_item(type_id=type_id, type_name=type_name)

        if item is not None:
            for attr_name, attr_value in item.iteritems():
                setattr(self, attr_name, attr_value)
            self.blueprint_type_id = self.get_blueprint_id_for_item(type_id=self.type_id)
            result = self.type_id
        else:
            self.type_id = None
            self.group_id = None
            self.type_name = ''
            self.description = ''
            self.mass = None
            self.volume = None
            self.capacity = None
            self.portion_size = None
            self.race_id = None
            self.base_price = None
            self.market_group_id = None

            self.graphic_id = None
            self.radius = None
            self.published = None
            self.chance_of_duplicating = None

            self.meta_group = None
            self.blueprint_type_id = None

            result = None

        return result


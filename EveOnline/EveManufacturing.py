'''
Created on Sep 15, 2014

@author: paulie
'''


import math

from EveOnline.EveItem import EveItem
from EveOnline.EveMathConstants import EVE_ACTIVITY_MANUFACTURING
from EveOnline import EveMathIndustry


class EveManufacturing(EveItem):
    '''
    Class for manufacturing in Eve Online
    '''

    build_list = {}
    buy_list = {}

    def __init__(self, db_access_obj, type_id=None, type_name=None):
        '''
        Constructor
        '''

        EveItem.__init__(self, db_access_obj)

        self.get_item(type_id=type_id, type_name=type_name)

    def calculate_build_buy_list(self,
                                 blueprint_type_id=None,
                                 activity_id=EVE_ACTIVITY_MANUFACTURING,
                                 facility_bonus=1,
                                 blueprint_me=0,
                                 runs=1):
        '''
        Method for calculating Build and Buy list with amounts of components
        and materials to build an item
        '''

        self.build_list = {}
        self.buy_list = {}

        if blueprint_type_id is not None:
            base_material_list = self.get_materials_for_blueprint(blueprint_type_id,
                                                                  activity_id=activity_id)
        elif self.blueprint_type_id is not None:
            base_material_list = self.get_materials_for_blueprint(self.blueprint_type_id,
                                                                  activity_id=activity_id)
        if base_material_list is not None:
            for base_material in base_material_list.itervalues():
                material_id = self.get_inv_item(type_id=base_material["material_type_id"])["type_id"]
                quantity = base_material["quantity"]

                #did we actually find an item?
                if material_id is not None:
                    material_blueprint_id = self.get_blueprint_id_for_item(type_id=material_id,
                                                                         activity_id=activity_id)

                    adjusted_quantity = math.ceil(quantity * \
                                                 EveMathIndustry.calculateMEMultiplier(blueprint_me,
                                                                                            facility_bonus)) * \
                                                                                            runs

                    # is it player buildable?
                    if material_blueprint_id is not None:
                        self.build_list[material_id] = adjusted_quantity
                    else:
                        self.buy_list[material_id] = adjusted_quantity

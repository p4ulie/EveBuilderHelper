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
                                 runs=1,
                                 asset_list=None):
        '''
        Method for calculating Build and Buy list with amounts of components
        and materials to build an item
        '''

        build_list = {}
        buy_list = {}

        if blueprint_type_id is not None:
            base_material_list = self.get_materials_for_blueprint(blueprint_type_id,
                                                                  activity_id=activity_id)
        elif self.blueprint_type_id is not None:
            base_material_list = self.get_materials_for_blueprint(self.blueprint_type_id,
                                                                  activity_id=activity_id)

        if base_material_list is not None:

            for base_material in base_material_list.itervalues():

                quantity = base_material["quantity"]
                material_id = self.get_inv_item(type_id=base_material["material_type_id"])["type_id"]

                #did we really find an item?
                if material_id is not None:
                    material_blueprint_id = self.get_blueprint_id_for_item(type_id=material_id,
                                                                           activity_id=activity_id)

                    adjusted_quantity = math.ceil(quantity * \
                                                  EveMathIndustry.calculate_me_multiplier(blueprint_me,
                                                                                            facility_bonus)) * \
                                                                                            runs

                    quantity_additional_to_get = adjusted_quantity

                    #do we already have some in assets?
                    if asset_list is not None:
                        if material_id in asset_list.iterkeys():
                            quantity_additional_to_get = adjusted_quantity - asset_list[material_id]
                            asset_list[material_id] = asset_list[material_id] - adjusted_quantity
                            if asset_list[material_id] <= 0:
                                del asset_list[material_id]

                    # is it player-buildable?
                    if material_blueprint_id is not None:
                        if quantity_additional_to_get > 0:
                            build_list[material_id] = quantity_additional_to_get
                    else:
                        if quantity_additional_to_get > 0:
                            buy_list[material_id] = quantity_additional_to_get

        return {"build_list": build_list, "buy_list": buy_list, "asset_list": asset_list}

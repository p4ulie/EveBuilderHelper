'''
Created on Sep 15, 2014

@author: paulie
'''


import math
from EveOnline.EveDB import EveDB
from EveOnline.EveMathConstants import EVE_ACTIVITY_MANUFACTURING
from EveOnline import EveMathIndustry


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
        self.blueprint_type_id = None   # determines whether item is buildable
        self.blueprint_me_level = 0
        self.blueprint_te_level = 0

        self.manufacturing_quantity = 0

        self.build_queue_level = 0  # order in which materials have to be build

        self.asset_list = None  # asset list to calculate in (need to buy less)

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

    def manufacturing_data_calculate(self):
        '''
        Calculate amounts of materials needed for manufacture,
        create build/buy lists for the materials
        '''

        self.material_list = []

        if (self.type_id is not None
        and self.blueprint_type_id is not None):
            base_material_list = self.get_materials_for_blueprint(self.blueprint_type_id,
                                                                  activity_id=EVE_ACTIVITY_MANUFACTURING)

            if base_material_list is not None:

                for base_material in base_material_list.itervalues():

                    quantity = base_material["quantity"]
                    material_id = self.get_inv_item(type_id=base_material["material_type_id"])["type_id"]

                    material = self.get_manufacturing_job(material_id)
                    if material is None:
                        # add material to list
                        material = EveItem(self.db_access_obj,
                                               type_id=material_id)
                        self.material_list.append(material)

                    if self.assembly_line_type_id is not None:
                        facility = self.get_assembly_line_type(assembly_line_type_id=self.assembly_line_type_id)
                        facility_multiplier = facility['base_material_multiplier']
                        if facility_multiplier is None:
                            facility_multiplier = 1
                    else:
                        facility_multiplier = 1

                    adjusted_quantity = math.ceil(quantity * \
                                                  EveMathIndustry.calculate_me_multiplier(self.blueprint_me_level,
                                                                                          facility_multiplier)) * \
                                                                                          self.manufacturing_quantity

                    material.manufacturing_quantity = adjusted_quantity
#                    material.asset_list = asset_list
                    material.build_queue_level = self.build_queue_level + 1
                    material.manufacturing_data_calculate()

    def get_material_list(self):
        '''
        Get list of objects representing materials
        '''

        material_list = {}

        # is the item buildable ?
        if self.blueprint_type_id is None:
            material_list[self.type_id] = self.manufacturing_quantity
        else:
            for job in self.material_list:
                mat_list = job.get_material_list()
                for mat_id, quant in mat_list.iteritems():
                    if mat_id in material_list.iterkeys():
                        material_list[mat_id] += quant
                    else:
                        material_list[mat_id] = quant

        return material_list

    def get_manufacturing_job(self, type_id):
        '''
        Return object reference to job form job list,
        according to specified parameters
        '''
        if type_id == self.type_id:
            return self

        for job in self.material_list:
            if job.get_manufacturing_job(type_id) is not None:
                return job

        return None

    def get_manufacturing_job_list(self):
        '''
        Get list of objects representing manufacturing jobs
        '''

        manufacturing_job_list = []

        # is the item buildable ?
        if self.blueprint_type_id is not None:
            manufacturing_job_list = [self]

            for job in self.material_list:
                manufacturing_job_list.extend(job.get_manufacturing_job_list())

        return manufacturing_job_list

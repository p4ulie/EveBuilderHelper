'''
Created on Sep 15, 2014

@author: paulie
'''


import math
from EveOnline.EveMathConstants import EVE_ACTIVITY_MANUFACTURING
from EveOnline import EveMathIndustry
from EveOnline.EveItem import EveItem


class EveItemManufacturing(EveItem):
    '''
    Class for data and methods for Items in Eve Online
    '''

    # manufacturing related attributes
    parent = None   # reference to parent object
    blueprint_type_id = None   # determines whether item is buildable
    blueprint_me_level = 0
    blueprint_te_level = 0

    manufacturing_quantity = 0

    build_queue_level = 0  # order in which materials have to be build

    assembly_line_type_id = None   # assembly line used, for bonuses

    material_list = []
    asset_list = {}  # asset list to calculate in (need to buy less)

    def __init__(self,
                 data_access,
                 type_id=None,
                 type_name=None,
                 blueprint_me_level=0,
                 blueprint_te_level=0,
                 manufacturing_quantity=1,
                 build_queue_level=0):
        '''
        Constructor
        '''

        # initialize object and get basic data
        EveItem.__init__(self,
                         data_access,
                         type_id=type_id,
                         type_name=type_name)

        self.get_item(type_id=type_id, type_name=type_name)
        self.blueprint_type_id = self.data_access.get_bp_id_for_item(self.type_id)

        self.blueprint_me_level = blueprint_me_level
        self.blueprint_te_level = blueprint_te_level
        self.manufacturing_quantity = manufacturing_quantity
        self.build_queue_level = build_queue_level

        self.material_list = []
        self.asset_list = {}

        self.manufacturing_data_calculate()

    def manufacturing_data_calculate(self):
        '''
        Calculate amounts of materials needed for manufacture,
        create build/buy lists for the materials
        '''

#        self.material_list = []

        if (self.type_id is not None) and (self.blueprint_type_id is not None):
            base_material_list = self.data_access.get_mat_for_bp(self.blueprint_type_id,
                                                                 activity_id=EVE_ACTIVITY_MANUFACTURING)

            if base_material_list is not None:

                for base_material in base_material_list:

                    material_id = self.data_access.get_inv_item(type_id=base_material["material_type_id"])["type_id"]
                    base_quantity = base_material["quantity"]

                    if self.assembly_line_type_id is not None:
                        facility = self.data_access.get_dtl_ram_asmb_line_types(assembly_line_type_id=self.assembly_line_type_id)
                        facility_multiplier = facility['base_material_multiplier']
                        if facility_multiplier is None:
                            facility_multiplier = 1
                    else:
                        facility_multiplier = 1

                    bonused_quantity = (math.ceil(base_quantity *
                                                  EveMathIndustry.calculate_me_multiplier(self.blueprint_me_level, facility_multiplier)) *
                                        self.manufacturing_quantity)

                    manufacturing_quantity = bonused_quantity

                    # do we already have some in assets?
                    if len(self.asset_list) > 0:
                        if material_id in self.asset_list.iterkeys():
                            manufacturing_quantity = bonused_quantity - self.asset_list[material_id]
                            self.asset_list[material_id] = self.asset_list[material_id] - bonused_quantity
                            if self.asset_list[material_id] <= 0:
                                del self.asset_list[material_id]

                    # do we already have this material in job list (if its buildable)
                    material = self.get_manufacturing_job_by_id(material_id)

                    # if we need to manufacture more than already in assets
                    if manufacturing_quantity > 0:
                        if material is None:
                            # add material to list
                            material = EveItemManufacturing(self.data_access,
                                                            type_id=material_id,
                                                            build_queue_level=(self.build_queue_level + 1))
                            material.parent = self
                            self.material_list.append(material)

                        material.manufacturing_quantity = manufacturing_quantity
                        material.asset_list = self.asset_list
                        material.manufacturing_data_calculate()
                    else:
                        # if new value calculated is 0, delete material from list
                        if material is not None:
                            self.material_list.remove(material)

    def get_manufacturing_job_by_id(self, type_id):
        '''
        Return object reference to job form job list,
        according to specified parameters
        '''
        if type_id == self.type_id:
            return self

        for job in self.material_list:
            if job.get_manufacturing_job_by_id(type_id) is not None:
                return job

        return None

    def get_manufacturing_job_by_name(self, type_name):
        '''
        Return object reference to job form job list,
        according to specified parameters
        '''
        if type_name == self.type_name:
            return self

        for job in self.material_list:
            if job.get_manufacturing_job_by_name(type_name) is not None:
                return job

        return None

    def get_manufacturing_list(self):
        '''
        Get list of objects
        '''

        manufacturing_job_list = [self]

        for job in self.material_list:
            manufacturing_job_list.extend(job.get_manufacturing_job_list())

        return manufacturing_job_list

    def get_manufacturing_job_list(self):
        '''
        Get list of objects representing buildable construction parts
        '''

        manufacturing_job_list = []

        # is the item buildable ?
        if self.blueprint_type_id is not None:
            manufacturing_job_list = [self]

            for job in self.material_list:
                manufacturing_job_list.extend(job.get_manufacturing_job_list())

        return manufacturing_job_list

    def get_manufacturing_material_list(self):
        '''
        Get list of objects representing materials
        '''

        material_list = {}

        # is the item buildable ?
        if self.blueprint_type_id is None:
            material_list[self.type_id] = self.manufacturing_quantity
        else:
            for job in self.material_list:
                mat_list = job.get_manufacturing_material_list()
                for mat_id, quant in mat_list.iteritems():
                    if mat_id in material_list.iterkeys():
                        material_list[mat_id] += quant
                    else:
                        material_list[mat_id] = quant

        return material_list
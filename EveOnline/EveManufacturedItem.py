'''
Created on Sep 15, 2014

@author: paulie
'''


import math
from EveOnline.EveItem import EveItem
from EveOnline.EveMathConstants import EVE_ACTIVITY_MANUFACTURING
from EveOnline import EveMathIndustry


class EveManufacturedItem(EveItem):
    '''
    Class for data and methods for Items in Eve Online
    '''

    def __init__(self, db_access_obj, type_id=None, type_name=None):
        '''
        Constructor
        '''

        # initialize object and get basic data
        EveItem.__init__(self, db_access_obj, type_id=type_id, type_name=type_name)

        self.get_item(type_id=type_id, type_name=type_name)

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

                for base_material in base_material_list:

                    material_id = self.get_inv_item(type_id=base_material["material_type_id"])["type_id"]
                    base_quantity = base_material["quantity"]

                    if self.assembly_line_type_id is not None:
                        facility = self.get_assembly_line_type(assembly_line_type_id=self.assembly_line_type_id)
                        facility_multiplier = facility['base_material_multiplier']
                        if facility_multiplier is None:
                            facility_multiplier = 1
                    else:
                        facility_multiplier = 1

                    bonused_quantity = math.ceil(base_quantity * \
                                                  EveMathIndustry.calculate_me_multiplier(self.blueprint_me_level,
                                                                                          facility_multiplier)) * \
                                                                                          self.manufacturing_quantity

                    manufacturing_quantity = bonused_quantity

                    #do we already have some in assets?
                    if len(self.asset_list) > 0:
                        if material_id in self.asset_list.iterkeys():
                            manufacturing_quantity = bonused_quantity - self.asset_list[material_id]
                            self.asset_list[material_id] = self.asset_list[material_id] - bonused_quantity
                            if self.asset_list[material_id] <= 0:
                                del self.asset_list[material_id]

                    #if we need to manufacture more than already in assets
                    if manufacturing_quantity > 0:
                        material = self.get_manufacturing_job_by_id(material_id)
                        if material is None:
                            # add material to list
                            material = EveManufacturedItem(self.db_access_obj,
                                                   type_id=material_id)
                            material.parent = self
                            self.material_list.append(material)

                        material.manufacturing_quantity = manufacturing_quantity
                        material.asset_list = self.asset_list
                        material.build_queue_level = self.build_queue_level + 1
                        material.manufacturing_data_calculate()

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

        manufacturing_list = []

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


'''
Created on Nov 13, 2014

@author: paulie
'''

import math
from EveOnline.EveItem import EveItem
from EveOnline.EveMathConstants import EVE_ACTIVITY_MANUFACTURING
from EveOnline import EveMathIndustry


class EveManufacturingJob(EveItem):
    '''
    Class managing manufacturing jobs
    '''

    def __init__(self,
                 db_access_obj,
                 type_id=None,
                 runs=1,
                 bp_me=0,
                 bp_te=0,
                 asset_list=None,
                 assembly_line_type_id=None,
                 buil_queue_level=0):
        '''
        Constructor
        '''

        EveItem.__init__(self, db_access_obj)

        self.get_item(type_id=type_id)

        if asset_list is not None:
            self.asset_list = asset_list
        else:
            self.asset_list = {}

        if assembly_line_type_id is not None:
            self.assembly_line_type_id = assembly_line_type_id
        else:
            self.assembly_line_type_id = None

        self.runs = runs
        self.bp_me = bp_me
        self.bp_te = bp_te

        self.buil_queue_level = buil_queue_level
        self.build_queue = []

        self.calculate_job()

    def calculate_subjobs(self):
        '''
        Calculate jobs of jobs from building list
        '''
        for job_item_id, job_quantity in self.build_list.iteritems():
            sub_job = EveManufacturingJob(self.db_access_obj,
                                      type_id=job_item_id,
                                      runs=job_quantity,
                                      buil_queue_level=(self.buil_queue_level + 1))

            self.build_queue.append(sub_job)

    def get_job_queue(self):
        '''
        Return list of all jobs, build queue levels flattened
        '''
        job_list = []

        job_list.append(self)

        for job in self.build_queue:
            job_subjobs = job.get_job_queue()
            job_list.extend(job_subjobs)

        return job_list

    def get_shopping_list_total(self):
        '''
        Return list of material to buy, total for all jobs
        '''
        buy_list = {}

        for job in self.get_job_queue():
            for buy_id, quantity in job.buy_list.iteritems():
                if buy_id in buy_list.iterkeys():
                    buy_list[buy_id] += quantity
                else:
                    buy_list[buy_id] = quantity

        return buy_list

    def calculate_job(self):
        '''
        Calculate material list for building,
        build and buy lists (adjusted by materials already in assets)
        '''
        self.base_material_list = {}
        self.material_list = {}
        self.build_list = {}
        self.buy_list = {}

        if self.blueprint_type_id is not None:
            self.base_material_list = self.get_materials_for_blueprint(self.blueprint_type_id,
                                                                  activity_id=EVE_ACTIVITY_MANUFACTURING)

        if self.assembly_line_type_id is not None:
            facility = self.get_assembly_line_type(assembly_line_type_id=self.assembly_line_type_id)
            facility_multiplier = facility['base_material_multiplier']
            if facility_multiplier is None:
                facility_multiplier = 1
        else:
            facility_multiplier = 1

        if self.base_material_list is not None:

            for base_material in self.base_material_list.itervalues():

                quantity = base_material["quantity"]
                material_id = self.get_inv_item(type_id=base_material["material_type_id"])["type_id"]

                #did we really find an item?
                if material_id is not None:
                    adjusted_quantity = math.ceil(quantity * \
                                                  EveMathIndustry.calculate_me_multiplier(self.bp_me,
                                                                                          facility_multiplier)) * \
                                                                                          self.runs

                    self.material_list[material_id] = adjusted_quantity
                    quantity_to_acquire = adjusted_quantity

                    #do we already have some in assets?
                    if len(self.asset_list) > 0:
                        if material_id in self.asset_list.iterkeys():
                            quantity_to_acquire = adjusted_quantity - self.asset_list[material_id]
                            self.asset_list[material_id] = self.asset_list[material_id] - adjusted_quantity
                            if self.asset_list[material_id] <= 0:
                                del self.asset_list[material_id]

                    # is it player-buildable?
                    material_blueprint_id = self.get_blueprint_id_for_item(type_id=material_id,
                                                                           activity_id=EVE_ACTIVITY_MANUFACTURING)
                    if material_blueprint_id is not None:
                        if quantity_to_acquire > 0:
                            self.build_list[material_id] = quantity_to_acquire
                    else:
                        if quantity_to_acquire > 0:
                            self.buy_list[material_id] = quantity_to_acquire

        self.calculate_subjobs()
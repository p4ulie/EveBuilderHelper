'''
Created on Oct 30, 2016

@author: paulie
'''


from EveOnline.EveOnlineInvType import EveOnlineInvType


class EveOnlineBlueprint(EveOnlineInvType):
    '''
    Class for data and methods for Blueprints in Eve Online
    '''

    # blueprint related attributes
    blueprint_type_id = None   # determines whether item is buildable (blueprint exists as EveOnlineInvType)
    blueprint_original = None  # True/False (Copy)
    blueprint_me_level = 0
    blueprint_te_level = 0
    blueprint_runs = 0

    def __init__(self,
                 data_access,
                 type_id=None,
                 type_name=None,
                 blueprint_original=None,
                 blueprint_me_level=0,
                 blueprint_te_level=0,
                 blueprint_runs=0):
        '''
        Constructor
        '''

        # initialize object and get basic data
        EveOnlineInvType.__init__(self,
                                  data_access,
                                  type_id=type_id,
                                  type_name=type_name)

        self.blueprint_type_id = self.data_access.get_bp_id_for_type_id(self.type_id)
        self.blueprint_produced_quantity = self.data_access.get_produced_quantity_per_run_for_bp_id(self.blueprint_type_id)

        self.blueprint_original = blueprint_original
        self.blueprint_me_level = blueprint_me_level
        self.blueprint_te_level = blueprint_te_level
        self.blueprint_runs = blueprint_runs


    def is_buildable(self):
        '''
        Test whether the inv_type actually has a blueprint
        '''

        if self.blueprint_type_id is not None:
            return True
        else:
            return False
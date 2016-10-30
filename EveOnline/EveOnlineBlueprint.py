'''
Created on Oct 30, 2016

@author: paulie
'''


from EveOnline.EveOnlineInvType import EveOnlineInvType


class EveBlueprint(EveOnlineInvType):
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
                                  type_id=type_id)

        self.blueprint_original = blueprint_original
        self.blueprint_me_level = blueprint_me_level
        self.blueprint_te_level = blueprint_te_level
        self.blueprint_runs = blueprint_runs

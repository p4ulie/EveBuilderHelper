'''
Created on Sep 15, 2014

@author: paulie
'''


class EveOnlineInvType(object):
    '''
    Class for data and methods for Items in Eve Online
    '''

    def __init__(self, data_access, type_id=None, type_name=None):
        '''
        Constructor
        '''

        # set data access object reference (to load data from DB, files, ...)
        self.data_access = data_access

        # basic invType attributes
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
        self.icon_id = None
        self.sound_id = None
        self.graphic_id = None

        if (type_id is not None) or (type_name is not None):
            self.get_inv_type(type_id=type_id, type_name=type_name)

    def get_inv_type(self, type_id=None, type_name=None):
        '''
        Get item by ID
        '''

        data = None

        if type_name is not None:
            data = self.data_access.get_inv_type(type_name=type_name)
        if type_id is not None:
            data = self.data_access.get_inv_type(type_id=type_id)

        if data is not None:
            for key, value in data.iteritems():
                setattr(self, key, value)

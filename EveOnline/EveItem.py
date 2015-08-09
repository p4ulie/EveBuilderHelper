'''
Created on Sep 15, 2014

@author: paulie
'''


class EveItem(object):
    '''
    Class for data and methods for Items in Eve Online
    '''

    def __init__(self, data_access_obj, type_id=None, type_name=None):
        '''
        Constructor
        '''

        # set data access object reference (to load data from DB, files, ...)
        self.data_access_obj = data_access_obj

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

        if type_id is not None:
            self.get_item(type_id=type_id)
        else:
            if type_name is not None:
                self.get_item(type_name=type_name)

    def get_item(self, type_id=None, type_name=None):
        '''
        Get item by ID or name
        '''

        data = self.data_access_obj.get_inv_item(type_id=type_id, type_name=type_name)

        for key, value in data.iteritems():
            setattr(self, key, value)

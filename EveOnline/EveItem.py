'''
Created on Sep 15, 2014

@author: paulie
'''


from EveOnline.EveDB import EveDB


class EveItem(EveDB):
    '''
    Class for data and methods for Items in Eve Online
    '''

    type_id = None
    group_id = None
    type_name = ''
    description = ''
    mass = None
    volume = None
    capacity = None
    portion_size = None
    race_id = None
    base_price = None
    market_group_id = None

    graphic_id = None
    radius = None
    published = None
    chance_of_duplicating = None

    meta_group = None
    blueprint_type_id = None

    def __init__(self, db_access_obj, type_id=None, type_name=None):
        '''
        Constructor
        '''

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

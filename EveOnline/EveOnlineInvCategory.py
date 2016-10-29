"""
Created on Oct 28, 2016

@author: paulie
"""


class EveOnlineInvCategory(object):
    """
    Class for data and methods for invCategories in Eve Online
    """

    def __init__(self, data_access, category_id=None, category_name=None):
        """
        Constructor
        """

        # set data access object reference (to load data from DB, files, ...)
        self.data_access = data_access

        # basic invCategory attributes
        self.category_id = None
        self.category_name = ''
        self.icon_id = None

        self.get_category(category_id=category_id, category_name=category_name)

    def get_category(self, category_id=None, category_name=None):
        '''
        Get item by ID
        '''

        if category_name is not None:
            data = self.data_access.get_inv_category(category_name=category_name)
        else:
            data = self.data_access.get_inv_category(category_id=category_id)

        if data is not None:
            for key, value in data.iteritems():
                setattr(self, key, value)

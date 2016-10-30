"""
Created on Oct 28, 2016

@author: paulie
"""


class EveOnlineInvGroup(object):
    """
    Class for data and methods for invGroups in Eve Online
    """

    def __init__(self, data_access, group_id=None, group_name=None):
        """
        Constructor
        """

        # set data access object reference (to load data from DB, files, ...)
        self.data_access = data_access

        # basic invGroup attributes
        self.group_id = None
        self.category_id = None
        self.group_name = ''
        self.icon_id = None
        self.use_base_price = None
        self.anchored = None
        self.anchorable = None
        self.fittable_non_singleton = None

        if (group_id is not None) or (group_name is not ''):
            self.get_inv_group(group_id=group_id, group_name=group_name)

    def get_inv_group(self, group_id=None, group_name=None):
        '''
        Get group by ID
        '''

        data = None

        data = self.data_access.get_inv_group(group_id=group_id)

        if data is not None:
            for key, value in data.iteritems():
                setattr(self, key, value)

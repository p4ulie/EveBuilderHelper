'''
Created on Oct 30, 2016

@author: paulie
'''


class EveOnlineRamAssemblyLineTypes(object):
    '''
    Class for data and methods for RamAssemblyLineTypes in Eve Online
    '''

    def __init__(self,
                 data_access, assembly_line_type_id=None,
                 assembly_line_type_name=None):
        '''
        Constructor
        '''

        # set data access object reference (to load data from DB, files, ...)
        self.data_access = data_access

        # basic invType attributes
        self.assembly_line_type_id = None
        self.assembly_line_type_name = ''
        self.description = ''
        self.base_time_multiplier = 1
        self.base_material_multiplier = 1
        self.base_cost_multiplier = 1
        self.volume = None
        self.activity_id = None
        self.min_cost_per_hour = None

        self.get_ram_assembly_line_type(assembly_line_type_id=assembly_line_type_id,
                                        assembly_line_type_name=assembly_line_type_name)

    def get_ram_assembly_line_type(self,
                                   assembly_line_type_id=None,
                                   assembly_line_type_name=None):
        '''
        Get item by ID
        '''

        if assembly_line_type_name is not None:
            data = self.data_access.get_ram_asmb_line_type(assembly_line_type_name=assembly_line_type_name)
        else:
            data = self.data_access.get_ram_asmb_line_type(assembly_line_type_id=assembly_line_type_id)

        if data is not None:
            for key, value in data.iteritems():
                setattr(self, key, value)

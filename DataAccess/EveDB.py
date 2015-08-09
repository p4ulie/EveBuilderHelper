'''
Created on 18.6.2014

@author: Pavol Antalik
'''

import math
from EveOnline.EveMathConstants import EVE_ACTIVITY_MANUFACTURING


class EveDB(object):
    '''
    Class for accessing EVE Online data dump data and methods
    in a database.
    db_access_obj can point to objects that access specific database types - SQLite, MySQL, ...
    '''

    def __init__(self,
                 db_access_obj):
        '''
        Constructor
        '''

        self.db_access_obj = db_access_obj

    def get_list_of_inv_categories(self):
        '''
        Get list of categories
        '''
        data = None

        query = """
                    SELECT c.categoryID,
                            c.categoryName,
                            c.description,
                            c.iconID
                    FROM invCategories AS c
                    WHERE c.published = 1
                """
        result = self.db_access_obj.fetch_data(query)

        if result is not None:
            data = []
            for row in result:
                data.append({'category_id': row[0],
                             'category_name': row[1],
                             'description': row[2],
                             'icon_id': row[3]})

        return data

    def get_list_of_inv_groups(self, category_id=None):
        '''
        Get list of groups
        '''
        data = None

        query = """
                    SELECT g.groupID,
                            g.categoryID,
                            g.groupName,
                            g.description,
                            g.iconID
                    FROM invGroups AS g
                    WHERE g.published = '1'
                """

        if category_id is not None:
            query += """
                        AND g.categoryID = ?
                    """
            result = self.db_access_obj.fetch_data(query, category_id)
        else:
            result = self.db_access_obj.fetch_data(query)

        if result is not None:
            data = []
            for row in result:
                data.append({'group_id': row[0],
                             'category_id': row[1],
                             'group_name': row[2],
                             'description': row[3],
                             'icon_id': row[4]})

        return data

    def get_inv_category(self, category_id=None):
        '''
        Get category data
        '''
        data = None

        if category_id is not None:
            query = """
                        SELECT c.categoryID,
                               c.categoryName,
                               c.description,
                               c.iconID
                        FROM invCategories AS c
                        WHERE c.published = '1'
                        AND c.categoryID = ?
                    """
            result = self.db_access_obj.fetch_data(query, category_id)

        if (result is not None) and (len(result) > 0):
            data = []
            for row in result:
                data.append({'`category_id': row[0],
                             'category_name': row[1],
                             'description': row[2],
                             'icon_id': row[3]})

        return data

    def get_inv_group(self, group_id=None):
        '''
        Get group data
        '''
        data = None

        if group_id is not None:
            query = """
                        SELECT g.groupID,
                               g.categoryID,
                               g.groupName,
                               g.description,
                               g.iconID,
                               g.useBasePrice,
                               g.allowManufacture,
                               g.allowRecycler,
                               g.anchored,
                               g.anchorable,
                               g.fittableNonSingleton
                        FROM invGroups AS g
                        WHERE g.published = '1'
                        AND g.groupID = ?
                    """
            result = self.db_access_obj.fetch_data(query, group_id)

        if (result is not None) and (len(result) > 0):
            data = []
            for row in result:
                data.append({'group_id': row[0],
                             'category_id': row[1],
                             'group_name': row[2],
                             'description': row[3],
                             'icon_id': row[4],
                             'use_base_price': row[5],
                             'allow_manufacture': row[6],
                             'allow_recycler': row[7],
                             'anchored': row[8],
                             'anchorable': row[9],
                             'fittable_non_singleton': row[10]})

        return data

    def get_list_of_inv_items(self, type_name=None, group_id=None):
        '''
        Get list of items by (part of) name or group_id
        '''
        result = None

        query = """
                    SELECT t.typeID,
                            t.groupID,
                            t.typeName,
                            t.description,
                            t.mass,
                            t.volume,
                            t.capacity,
                            t.portionSize,
                            t.raceID,
                            t.basePrice,
                            t.marketGroupID
                    FROM invtypes AS t
                    WHERE t.published = '1'
                """

        if type_name is not None:
            query += """
                        AND t.typeName like '%?%'
                    """
            result = self.db_access_obj.fetch_data(query, type_name)
        else:
            if group_id is not None:
                query += """
                            AND t.groupID = ?
                        """
                result = self.db_access_obj.fetch_data(query, group_id)

        if result is not None:
            data = []
            for row in result:
                data.append({'type_id': row[0],
                             'group_id': row[1],
                             'type_name': row[2],
                             'description': row[3],
                             'mass': row[4],
                             'volume': row[5],
                             'capacity': row[6],
                             'portion_size': row[7],
                             'race_id': row[8],
                             'base_price': row[9],
                             'market_group_id': row[0]})
        else:
            data = None

        return data

    def get_inv_item(self, type_id=None, type_name=None):
        '''
        Get item by ID or name
        '''
        result = None

        query = """
                    SELECT t.typeID,
                            t.groupID,
                            t.typeName,
                            t.description,
                            t.mass,
                            t.volume,
                            t.capacity,
                            t.portionSize,
                            t.raceID,
                            t.basePrice,
                            t.marketGroupID
                    FROM invtypes AS t
                    WHERE t.published = '1'
                """

        if type_id is not None:
            query += """
                        AND t.typeID = ?
                    """
            result = self.db_access_obj.fetch_data(query, type_id)
        else:
            if type_name is not None:
                query += """
                            AND t.typeName = ?
                        """
                result = self.db_access_obj.fetch_data(query, type_name)

        if (result is not None) and (len(result) != 0):
            # take only the first row
            row = result[0]
            data = {'type_id': row[0],
                    'group_id': row[1],
                    'type_name': row[2],
                    'description': row[3],
                    'mass': row[4],
                    'volume': row[5],
                    'capacity': row[6],
                    'portion_size': row[7],
                    'race_id': row[8],
                    'base_price': row[9],
                    'market_group_id': row[0]}
        else:
            data = None

        return data

    def get_bp_id_for_item(self,
                           type_id=None,
                           activity_id=EVE_ACTIVITY_MANUFACTURING):
        '''
        Get Blueprint typeID from Item typeID
        '''

        data = None

        if type_id is not None:
            query = """
                        SELECT typeID
                        FROM industryactivityproducts AS i
                        WHERE i.productTypeID = ?
                        and i.activityId = ?
                    """
            result = self.db_access_obj.fetch_data(query,
                                                   type_id,
                                                   activity_id)

            if (result is not None) and (len(result) > 0):
                data = result[0][0]

        return data

    def get_lst_mat_for_rfn(self, type_id=None):
        '''
        Get list of materials for refining
        '''
        data = None

        query = """
                    SELECT m.materialTypeID,
                            m.quantity
                    FROM invTypeMaterials AS m
                    WHERE m.typeID = ?
                """

        if type_id is not None:
            result = self.db_access_obj.fetch_data(query,
                                                   type_id)

            if result is not None:
                data = []
                for row in result:
                    data.append({'material_type_id': row[0],
                                 'quantity': row[1]})

        return data

    def get_lst_mat_for_rfn_adj(self,
                                type_id=None,
                                fclt_base_yield=0.54,
                                rprcs_skill_lvl=0,
                                rprcs_eff_skill_lvl=0,
                                mtrl_spcfc_prcs_skill_lvl=0,
                                implant_bonus=1):
        '''
        Get refining output materials adjusted by yield coeficient
        '''
        refining_type_id = None
        refining_list = []

        if type_id is not None:
            refining_type_id = type_id

        if refining_type_id is not None:
            refining_list = self.get_lst_mat_for_rfn(type_id=type_id)

            refining_yield_coeficienf = (fclt_base_yield *
                                         (1 + mtrl_spcfc_prcs_skill_lvl * 0.02) *
                                         (1 + rprcs_skill_lvl * 0.03) *
                                         (1 + rprcs_eff_skill_lvl * 0.02) *
                                         implant_bonus)

            for material in refining_list:
                material['quantity'] = int(math.floor((material['quantity'] * refining_yield_coeficienf)))

        return refining_list

    def get_mat_for_bp(self,
                       blueprint_type_id,
                       activity_id=EVE_ACTIVITY_MANUFACTURING):
        '''
        Get list of materials for specified blueprint typeID and activityId
        '''

        data = None

        query = """
                    SELECT i.materialTypeID,
                            i.quantity,
                            i.consume
                    FROM industryactivitymaterials AS i
                    WHERE i.typeID = ?
                    and i.activityId = ?
                """
        result = self.db_access_obj.fetch_data(query,
                                               blueprint_type_id,
                                               activity_id)

        if result is not None:
            data = []
            for row in result:
                data.append({'material_type_id': row[0],
                             'quantity': row[1],
                             'consume': row[2]})

        return data

    def get_time_for_blueprint(self,
                               blueprint_type_id,
                               activity_id=EVE_ACTIVITY_MANUFACTURING):
        '''
        Get time of industry action for specified blueprint typeID
        and activityId
        '''
        query = """
                    SELECT time
                    FROM industryactivity AS i
                    WHERE i.typeID = ?
                    and i.activityId = ?
                """
        result = self.db_access_obj.fetch_data(query,
                                               blueprint_type_id,
                                               activity_id)

        if result is not None:
            data = result[0][0]
        else:
            data = None

        return data

    def get_list_of_activities(self):
        '''
        Get list of ramActivities
        '''
        data = None

        query = """
                    SELECT r.activityId,
                            r.activityName,
                            r.iconNo,
                            r.description
                    FROM ramActivities AS r
                    WHERE r.published = '1'
                """
        result = self.db_access_obj.fetch_data(query)

        if result is not None:
            data = []
            for row in result:
                data.append({'activity_id': row[0],
                             'activity_name': row[1],
                             'icon_no': row[2],
                             'description': row[3]})

        return data

    def get_lst_ram_asmb_line_types(self,
                                    activity_id=EVE_ACTIVITY_MANUFACTURING,
                                    group_id=None,
                                    filter_outposts=False):
        '''
        Get list of ramassemblylinetypes
        '''

        data = None

        query = """
                    SELECT rlt.assemblyLineTypeID,
                           rlt.assemblyLineTypeName,
                           rlt.description,
                           rlt.baseTimeMultiplier,
                           rlt.baseMaterialMultiplier,
                           rlt.baseCostMultiplier,
                           rlt.volume,
                           rlt.activityID,
                           rlt.minCostPerHour
                    FROM
        """

        if group_id is None:
            query += """
                    ramAssemblyLineTypes as rlt
                    WHERE rlt.activityID = ?
            """
            result = self.db_access_obj.fetch_data(query, activity_id)
        else:
            query += """
                    ramAssemblyLineTypeDetailPerGroup as rg, ramAssemblyLineTypes as rlt
                    WHERE
                    rlt.assemblyLineTypeID = rg.assemblyLineTypeID
                    AND
                    rlt.activityID = ? and rg.groupID = ?
            """
            result = self.db_access_obj.fetch_data(query, activity_id, group_id)

        if result is not None:
            data = []
            for row in result:
                if (filter_outposts and ("Outpost" in row[1])) == False:
                    data.append({'assembly_line_type_id': row[0],
                                 'assembly_line_type_name': row[1],
                                 'description': row[2],
                                 'base_time_multiplier': row[3],
                                 'base_material_multiplier': row[4],
                                 'base_cost_multiplier': row[5],
                                 'volume': row[6],
                                 'activity_id': row[7],
                                 'min_cost_per_hour': row[8]})

        return data

    def get_dtl_ram_asmb_line_types(self,
                                    assembly_line_type_id=None,
                                    assembly_line_type_name=None,
                                    activity_id=EVE_ACTIVITY_MANUFACTURING):
        '''
        Get bonus multiplier for specified activity and assembly line type
        '''
        result = None

        query = """SELECT r.assemblyLineTypeID,
                            r.assemblyLineTypeName,
                            r.description,
                            r.baseTimeMultiplier,
                            r.baseMaterialMultiplier,
                            r.baseCostMultiplier,
                            r.volume,
                            r.activityId,
                            r.minCostPerHour
                    FROM ramAssemblyLineTypes AS r
                    WHERE r.activityId = ?
                """

        if assembly_line_type_id is not None:
            query += """
                            AND r.assemblyLineTypeId = ?
                    """
            result = self.db_access_obj.fetch_data(query,
                                                   activity_id,
                                                   assembly_line_type_id)
        else:
            if assembly_line_type_name is not None:
                query += """
                            AND r.assemblyLineTypeName = ?
                        """
                result = self.db_access_obj.fetch_data(query,
                                                       activity_id,
                                                       assembly_line_type_name)

        if (result is not None) and (len(result) != 0):
            row = result[0]
            data = {'assembly_line_type_id': row[0],
                    'assembly_line_type_name': row[1],
                    'description': row[2],
                    'base_time_multiplier': row[3],
                    'base_material_multiplier': row[4],
                    'base_cost_multiplier': row[5],
                    'volume': row[6],
                    'activity_id': row[7],
                    'min_cost_per_hour': row[8]}
        else:
            data = None

        return data

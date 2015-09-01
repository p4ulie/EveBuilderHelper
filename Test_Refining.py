'''
Created on Dec 1, 2014

@author: paulie
'''

from DataAccess.DBAccessSQLite import DBAccessSQLite
from DataAccess.EveDB import EveDB
from EveOnline.EveItemManufacturing import EveItemManufacturing
import cvxopt

DATA_FILE = 'data/eve.db'


def main():
    '''
    Main function
    '''

    ore = EveItemManufacturing(DATA_ACCESS_OBJECT)
    reproc_mat_list = ore.get_mineral_matrix_adjusted(sec_status_low_limit=0.0,
                                                      fclt_base_yield=0.54,
                                                      rprcs_skill_lvl=5,
                                                      rprcs_eff_skill_lvl=5,
                                                      mtrl_spcfc_prcs_skill_lvl=5,
                                                      implant_bonus=0)

    veld_and_plag_matrix = {1230: reproc_mat_list[1230],
                            18: reproc_mat_list[18],
                            1224: reproc_mat_list[1224],
                            1228: reproc_mat_list[1228]
                            }

    for k_ore,v_minerals in veld_and_plag_matrix.iteritems():
        ore_name = DATA_ACCESS_OBJECT.get_inv_item(type_id=k_ore)['type_name']

        output = ""
        names = ""

        min_group = DATA_ACCESS_OBJECT.get_inv_group(group_name='Mineral')['group_id']

        for mmm,quant in v_minerals.iteritems():
            min_item = DATA_ACCESS_OBJECT.get_inv_item(type_id=mmm)
            if min_item['group_id'] == min_group:
                output += "%s\t" % (quant)
                names += "%s\t" % (min_item['type_name'])

        print "Minerals:\t%s" % (names)
        print "%s:\t%s" % (ore_name, output)

    
if __name__ == '__main__':
    DB_ACCESS_OBJECT = DBAccessSQLite(DATA_FILE)
    DATA_ACCESS_OBJECT = EveDB(DB_ACCESS_OBJECT)

    main()

    DB_ACCESS_OBJECT.close()

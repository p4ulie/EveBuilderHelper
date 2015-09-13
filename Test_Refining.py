'''
Created on Dec 1, 2014

@author: paulie
'''

from DataAccess.DBAccessSQLite import DBAccessSQLite
from DataAccess.EveDB import EveDB
from EveOnline.EveItemManufacturing import EveItemManufacturing
from cvxopt import matrix, solvers

DATA_FILE = 'data/eve.db'


def main():
    '''
    Main function
    '''

    ore = EveItemManufacturing(DATA_ACCESS_OBJECT)
    reproc_mat_list = ore.get_mineral_matrix_adjusted(sec_status_low_limit=0.9,
                                                      fclt_base_yield=0.54,
                                                      rprcs_skill_lvl=5,
                                                      rprcs_eff_skill_lvl=5,
                                                      mtrl_spcfc_prcs_skill_lvl=5,
                                                      implant_bonus=0)

    # for simplyfication we filter ore list
    reproc_mat_list_filtered = {}
    reproc_mat_list_filtered[DATA_ACCESS_OBJECT.get_inv_item(type_name='Veldspar')['type_id']] = reproc_mat_list[DATA_ACCESS_OBJECT.get_inv_item(type_name='Veldspar')['type_id']]
    reproc_mat_list_filtered[DATA_ACCESS_OBJECT.get_inv_item(type_name='Plagioclase')['type_id']] = reproc_mat_list[DATA_ACCESS_OBJECT.get_inv_item(type_name='Plagioclase')['type_id']]
    reproc_mat_list_filtered[DATA_ACCESS_OBJECT.get_inv_item(type_name='Scordite')['type_id']] = reproc_mat_list[DATA_ACCESS_OBJECT.get_inv_item(type_name='Scordite')['type_id']]
    reproc_mat_list_filtered[DATA_ACCESS_OBJECT.get_inv_item(type_name='Pyroxeres')['type_id']] = reproc_mat_list[DATA_ACCESS_OBJECT.get_inv_item(type_name='Pyroxeres')['type_id']]
    reproc_mat_list = reproc_mat_list_filtered

    # define mineral amounts we want to get refining the ores
    mineral_amounts_desired={}
    mineral_amounts_desired[DATA_ACCESS_OBJECT.get_inv_item(type_name='Tritanium')['type_id']] = 200
    mineral_amounts_desired[DATA_ACCESS_OBJECT.get_inv_item(type_name='Nocxium')['type_id']] = 1
#    mineral_amounts_desired[DATA_ACCESS_OBJECT.get_inv_item(type_name='Pyerite')['type_id']] = 160
#    mineral_amounts_desired[DATA_ACCESS_OBJECT.get_inv_item(type_name='Mexallon')['type_id']] = 80

    # define variables for building matrices
    list_of_mineral_matrices = []
    mineral_amounts_desired_matrix = []
    ore_quantity_matrix = []

    # build matrices for linear programming
    for k_ore,v_minerals in reproc_mat_list.iteritems():
        min_quantity_list = [-float(quant) for quant in v_minerals.values()]
        list_of_mineral_matrices.append(min_quantity_list)
        ore_quantity_matrix.append(float(1.0))
        min_id_list = v_minerals.keys()

    for min_id in min_id_list:
        if (min_id not in mineral_amounts_desired.keys()):
            mineral_amounts_desired_matrix.append(float(0.0))
        else:
            mineral_amounts_desired_matrix.append(-float(mineral_amounts_desired[min_id]))
        
    A = matrix(list_of_mineral_matrices)
    b = matrix(mineral_amounts_desired_matrix)
    c = matrix(ore_quantity_matrix)

#    print A
#    print b
#    print c

    sol=solvers.lp(c,A,b)
    print(sol['x'])

if __name__ == '__main__':
    DB_ACCESS_OBJECT = DBAccessSQLite(DATA_FILE)
    DATA_ACCESS_OBJECT = EveDB(DB_ACCESS_OBJECT)

    main()

    DB_ACCESS_OBJECT.close()

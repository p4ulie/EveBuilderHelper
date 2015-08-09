'''
Created on Dec 1, 2014

@author: paulie
'''

from DataAccess.DBAccessSQLite import DBAccessSQLite
from DataAccess.EveDB import EveDB
from EveOnline.EveItemManufacturing import EveItemManufacturing

DATA_FILE = 'data/eve.db'


def main():
    '''
    Main function
    '''
    ore1 = EveItemManufacturing(DATA_ACCESS_OBJECT,
                                type_name='Plagioclase')

    print ore1.data_access.get_inv_group(group_id=12)

    print ore1.data_access.type_id

    print ore1.data_access.get_materials_for_refining()

    print ore1.data_access.get_mtrl_for_rfn_adj(fclt_base_yield=0.54,
                                                rprcs_skill_lvl=5,
                                                rprcs_eff_skill_lvl=5,
                                                mtrl_spcfc_prcs_skill_lvl=5,
                                                implant_bonus=1.02)

if __name__ == '__main__':
    DB_ACCESS_OBJECT = DBAccessSQLite(DATA_FILE)
    DATA_ACCESS_OBJECT = EveDB(DB_ACCESS_OBJECT)

    main()

    DB_ACCESS_OBJECT.close()

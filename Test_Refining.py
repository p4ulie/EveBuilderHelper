'''
Created on Dec 1, 2014

@author: paulie
'''

DB = 'data/eve.db'

from DBAccessSQLite import DBAccessSQLite
from EveOnline.EveManufacturedItem import EveItemManufacturing


def main():
    ore1 = EveItemManufacturing(db_access_object,
                   type_name='Plagioclase')

    print ore1.get_inv_group(group_id=12)

    print ore1.type_id

    print ore1.get_materials_for_refining()

    print ore1.get_mtrl_for_rfn_adj(fclt_base_yield=0.54,
                                                          rprcs_skill_lvl=5,
                                                          rprcs_eff_skill_lvl=5,
                                                          mtrl_spcfc_prcs_skill_lvl=5,
                                                          implant_bonus=1.02)

if __name__ == '__main__':
    db_access_object = DBAccessSQLite(DB)

    main()

    db_access_object.close()

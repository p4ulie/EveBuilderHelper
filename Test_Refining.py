'''
Created on Dec 1, 2014

@author: paulie
'''

DB = 'data/eve.db'

from DBAccessSQLite import DBAccessSQLite
from EveOnline.EveItem import EveItem


def main():
    ore1 = EveItem(db_access_object,
                   type_name='Plagioclase')

    print ore1.get_inv_group(group_id=12)

    print ore1.type_id

    print ore1.get_materials_for_refining()

    print ore1.get_materials_for_refining_adjusted(facility_base_yield=0.54,
                                                          reprocessing_skill_level=5,
                                                          reprocessing_efficiency_skill_level=5,
                                                          material_specific_processing_skill_level=5,
                                                          implant_bonus=1.02)

if __name__ == '__main__':
    db_access_object = DBAccessSQLite(DB)

    main()

    db_access_object.close()

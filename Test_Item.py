'''
Created on 8.8.2015

@author: Pavol Antalik
'''

from DataAccess.DBAccessSQLite import DBAccessSQLite
from DataAccess.EveDB import EveDB
from EveOnline.EveOnlineInvType import EveOnlineInvType
from EveOnline.EveOnlineInvGroup import EveOnlineInvGroup
from EveOnline.EveOnlineInvCategory import EveOnlineInvCategory

DATA_FILE = 'data/eve.db'


def main():
    '''
    Main function for testing the classes
    '''

    DATA_ACCESS_OBJECT = EveDB(DBAccessSQLite(DATA_FILE))

    eve_inv_category = EveOnlineInvCategory(DATA_ACCESS_OBJECT,
                                            category_name="Asteroid")

    eve_inv_group = EveOnlineInvGroup(DATA_ACCESS_OBJECT,
                                      group_name="Veldspar")

    eve_inv_type = EveOnlineInvType(DATA_ACCESS_OBJECT,
                                    type_name="Veldspar")

    print eve_inv_category.category_name
    print eve_inv_group.group_name
    print eve_inv_type.type_name

    DATA_ACCESS_OBJECT.db_access_obj.close()

if __name__ == '__main__':
    main()

'''
Created on 8.8.2015

@author: Pavol Antalik
'''

from DataAccess.DBAccessSQLite import DBAccessSQLite
from DataAccess.EveDB import EveDB
from EveOnline.EveItem import EveItem

DATA_FILE = 'data/eve.db'


def main():
    '''
    Main function for testing the classes
    '''

    db_access_object = DBAccessSQLite(DATA_FILE)
    DATA_ACCESS_OBJECT = EveDB(db_access_object)

    eve_item = EveItem(DATA_ACCESS_OBJECT,
                       type_name="Archon")

    print eve_item.type_name

    db_access_object.close()

if __name__ == '__main__':
    main()

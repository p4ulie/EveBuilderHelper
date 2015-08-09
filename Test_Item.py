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
    data_access_object = EveDB(db_access_object)

    eve_item = EveItem(data_access_object,
                       type_name="Providence")

    print eve_item.type_name

    db_access_object.close()

if __name__ == '__main__':
    main()

'''
Created on 17.6.2014

@author: Pavol Antalik
'''

#import math

from DBAccessSQLite import DBAccessSQLite

from EveMath.EveMathConstants import EVE_ACTIVITY_MANUFACTURING

#from EveModules import EveDB, EveItem
#from EveMath import EveMathIndustry
from EveManufacturing import EveManufacturing

DB = 'data/eve.db'

BUILD_PRODUCT_NAME = 'Kronos'
BUILD_PRODUCT_COUNT = 1
BUILD_PRODUCT_ME = 9
BUILD_PRODUCT_PE = 18


def main():
    '''
    Main function for testing the classes
    '''

    blueprint_me = BUILD_PRODUCT_ME
#    blueprintPE = BUILD_PRODUCT_PE

    e_manuf = EveManufacturing.EveManufacturing(db_access_object, type_name=BUILD_PRODUCT_NAME)

    facility_bonus_ship = e_manuf.get_bonus_for_assembly_line_type(assembly_line_type_name="Advanced Medium Ship Assembly Array",
                                                                             activity_id=EVE_ACTIVITY_MANUFACTURING)['base_material_multiplier']

    e_manuf.calculate_build_buy_list(activity_id=EVE_ACTIVITY_MANUFACTURING,
                    blueprint_me=blueprint_me,
                    facility_bonus=facility_bonus_ship,
                    runs=BUILD_PRODUCT_COUNT)

    print "Building: %s" % e_manuf.type_name

    for build_type_id, build_quantity in e_manuf.build_list.iteritems():
        build_name = e_manuf.get_inv_item(type_id=build_type_id)
        if build_name is not None:
            print "Build %s\t%d" % (build_name["type_name"], build_quantity)

    print

    for buy_type_id, buy_quantity in e_manuf.buy_list.iteritems():
        buy_name = e_manuf.get_inv_item(type_id=buy_type_id)
        if buy_name is not None:
            print "Buy %s\t%d" % (buy_name["type_name"], buy_quantity)


if __name__ == '__main__':
    db_access_object = DBAccessSQLite(DB)

    main()

    db_access_object.close()

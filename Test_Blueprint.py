'''
Created on 17.6.2014

@author: Pavol Antalik
'''

#import math
import re

from DBAccessSQLite import DBAccessSQLite

from EveOnline.EveMathConstants import EVE_ACTIVITY_MANUFACTURING

from EveOnline import EveManufacturing

DB = 'data/eve.db'

BUILD_PRODUCT_NAME = 'Kronos'
BUILD_PRODUCT_COUNT = 1
BUILD_PRODUCT_ME = 10
BUILD_PRODUCT_PE = 18

ASSETS_LIST = '''Morphite\t13,010\tMineral\t
Tritanium\t6,818,891\tMineral\t
Magnetometric Sensor Cluster\t3,817\tConstruction Components\t
Pulse Shield Emitter\t3385\tConstruction Components\t
Fusion Reactor Unit\t193\tConstruction Components\t
'''


def build(type_id=None,
            type_name=None,
            blueprint_me=0,
            runs=1,
            asset_list=None):
    '''
    Calculate build/buy list
    '''
    eve_manufacturing = EveManufacturing.EveManufacturing(db_access_object, type_id=type_id, type_name=type_name)

    facility_bonus_product = eve_manufacturing.get_bonuses_for_assembly_line_type(assembly_line_type_name="Component Assembly Array")['base_material_multiplier']

    industrial_plan = eve_manufacturing.calculate_build(blueprint_me=blueprint_me,
                                                       facility_bonus=facility_bonus_product,
                                                       runs=runs,
                                                       asset_list=asset_list)

    for build_type_id, build_quantity in industrial_plan['build_list'].iteritems():
        build(type_id=build_type_id,
              blueprint_me=10,
              runs=build_quantity,
              asset_list=asset_list)

    return industrial_plan


def create_asset_list(line_list):
    '''
    Generate asset list from text lines
    '''
    asset_dict = {}

    e_asset = EveManufacturing.EveManufacturing(db_access_object)

    for line in line_list.splitlines():
        match = re.match(r"^(\D+)\t([\d\,]*)\t(\D+)\t.*", line)
        if match is not None:
            type_name = match.group(1).strip()
            quantity_string = match.group(2).replace(',','').strip()
            if quantity_string == '':
                quantity = 0
            else:
                quantity = int(quantity_string)
            group_name = match.group(3).strip()

            item = e_asset.get_inv_item(type_name=type_name)
            if item is not None:
                type_id = item["type_id"]
                if type_id in asset_dict.iterkeys():
                    asset_dict[type_id] += quantity
                else:
                    asset_dict[type_id] = quantity

    return asset_dict


def main():
    '''
    Main function for testing the classes
    '''

    blueprint_me = BUILD_PRODUCT_ME
#    blueprintPE = BUILD_PRODUCT_PE

    e_manuf = EveManufacturing.EveManufacturing(db_access_object, type_name=BUILD_PRODUCT_NAME)

    asset_dict = create_asset_list(ASSETS_LIST)
    asset_list = asset_dict.copy()
    asset_list2 = asset_dict.copy()

    build(type_name=BUILD_PRODUCT_NAME,
          blueprint_me=BUILD_PRODUCT_ME,
          runs=BUILD_PRODUCT_COUNT,
          asset_list=asset_list2)

    industrial_plan = e_manuf.calculate_build(activity_id=EVE_ACTIVITY_MANUFACTURING,
                                                       blueprint_me=blueprint_me,
                                                       runs=BUILD_PRODUCT_COUNT,
                                                       asset_list=asset_list)

    print "Building: %s\n" % e_manuf.type_name

    for material_type_id, material_quantity in industrial_plan['material_list'].iteritems():
        material_name = e_manuf.get_inv_item(type_id=material_type_id)
        if material_name is not None:

            if material_type_id in asset_dict.iterkeys():
                asset_quantity = asset_dict[material_type_id]
            else:
                asset_quantity = 0

            print "Material %s\t%d (in assets %d)" % (material_name["type_name"], material_quantity, asset_quantity)

    print

    for build_type_id, build_quantity in industrial_plan['build_list'].iteritems():
        build_name = e_manuf.get_inv_item(type_id=build_type_id)
        if build_name is not None:
            print "Build %s\t%d" % (build_name["type_name"], build_quantity)

    print

    for buy_type_id, buy_quantity in industrial_plan['buy_list'].iteritems():
        buy_name = e_manuf.get_inv_item(type_id=buy_type_id)
        if buy_name is not None:
            print "Buy %s\t%d" % (buy_name["type_name"], buy_quantity)

    db_access_object.close()

if __name__ == '__main__':
    db_access_object = DBAccessSQLite(DB)

    main()

    db_access_object.close()

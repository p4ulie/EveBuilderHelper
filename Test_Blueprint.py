'''
Created on 17.6.2014

@author: Pavol Antalik
'''

#import math
import re

from DBAccessSQLite import DBAccessSQLite

from EveOnline.EveMathConstants import EVE_ACTIVITY_MANUFACTURING

from EveOnline import EveItem

from EveOnline import EveManufacturingJob

DB = 'data/eve.db'

BUILD_PRODUCT_NAME = 'Guardian'
BUILD_PRODUCT_RUNS = 1
BUILD_PRODUCT_ME = 2
BUILD_PRODUCT_TE = 4

ASSETS_LIST = '''Morphite\t85\tMineral\t
Tritanium\t6,818,891\tMineral\t
Magnetometric Sensor Cluster\t3,817\tConstruction Components\t
Pulse Shield Emitter\t3385\tConstruction Components\t
Fusion Reactor Unit\t193\tConstruction Components\t
Augoror\t20\tShips\t
R.A.M.- Starship Tech\t20\tSomething\t

'''

#ASSETS_LIST = ''

def create_asset_list(line_list):
    '''
    Generate asset list from text lines
    '''
    asset_dict = {}

    e_asset = EveItem.EveItem(db_access_object)

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

def write_material_list(material_list,
                        asset_list,
                        format_string):

    for material_type_id, material_quantity in material_list.iteritems():
        material_item = EveItem.EveItem(db_access_object,
                                 type_id=material_type_id)
        material_name = material_item.get_inv_item(type_id=material_type_id)
        if material_name is not None:
            if material_type_id in asset_list.iterkeys():
                asset_quantity = asset_list[material_type_id]
            else:
                asset_quantity = 0

            print format_string % (material_name["type_name"], material_quantity, asset_quantity)


def main():
    '''
    Main function for testing the classes
    '''

    asset_dict = create_asset_list(ASSETS_LIST)

    e_built_item = EveItem.EveItem(db_access_object,
                             type_name=BUILD_PRODUCT_NAME)

    facility_id = e_built_item.get_assembly_line_type(assembly_line_type_name="Component Assembly Array")['assemblyLineTypeID']

    e_manuf_job = EveManufacturingJob.EveManufacturingJob(db_access_object,
                                                          type_id=e_built_item.type_id,
                                                          runs=BUILD_PRODUCT_RUNS,
                                                          bp_me=BUILD_PRODUCT_ME,
                                                          bp_te=BUILD_PRODUCT_TE,
                                                          asset_list=asset_dict,
                                                          assembly_line_type_id=facility_id)

    print "Building: %s\n" % e_manuf_job.type_name

    for job in e_manuf_job.get_job_queue():
        print "%s: %d (job level %d)" % (job.type_name,
                                   job.runs,
                                   job.buil_queue_level)

    print "\n"

    write_material_list(e_manuf_job.get_shopping_list_total(),
                        asset_dict,
                        "Buy %s\t%d (in assets %d)")


if __name__ == '__main__':
    db_access_object = DBAccessSQLite(DB)

    main()

    db_access_object.close()

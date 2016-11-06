'''
Created on 17.6.2014

@author: Pavol Antalik
'''

import re

from DataAccess.DBAccessSQLite import DBAccessSQLite
from DataAccess.EveDB import EveDB
# from EveOnline.EveMathConstants import EVE_ACTIVITY_MANUFACTURING
from EveOnline.EveOnlineInvType import EveOnlineInvType
from EveOnline.EveOnlineBlueprint import EveOnlineBlueprint
from EveOnline.EveOnlineManufacturingJob import EveOnlineManufacturingJob
from EveOnline.EveOnlineRamAssemblyLineTypes import EveOnlineRamAssemblyLineTypes

from DataAccess.MarketAccessEveCentral import MarketAccessEveCentral
from DataAccess.EveMarket import EveMarket

DATA_FILE = 'data/eve.db'

BUILD_PRODUCT_NAME = 'Nitrogen Fuel Block'
#BUILD_FACILITY = 'Large Ship Assembly Array'
#BUILD_PRODUCT_NAME = 'Capital Cargo Bay'
BUILD_FACILITY = 'STATION manufacturing'
BUILD_PRODUCT_RUNS = 650
BUILD_PRODUCT_ME = 10
BUILD_PRODUCT_TE = 20

# ASSETS_LIST = '''Capital Jump Drive\t29\tCapital Construction Components\t
# '''

ASSETS_LIST = '''Tritanium\t2929173\tMineral\t\t\t4,546.37 m3
Pyerite\t97720\tMineral\t\t\t245,869.82 m3
Mexallon\t161164\tMineral\t\t\t1,410.84 m3
Isogen\t6082\tMineral\t\t\t623.82 m3
Nocxium\t23663\tMineral\t\t\t3,259.77 m3
Zydrine\t6194\tMineral\t
Megacyte\t39402\tMineral\t\t\t1,402.09 m3
'''

ASSETS_LIST = ''


def create_asset_list(line_list):
    '''
    Generate asset list from text lines
    '''
    asset_dict = {}

    for line in line_list.splitlines():
        match = re.match(r"^(\D+)\t([\d\,]*)\t(\D+)\t.*", line)
        if match is not None:
            type_name = match.group(1).strip()
            quantity_string = match.group(2).replace(',', '').strip()
            if quantity_string == '':
                quantity = 0
            else:
                quantity = int(quantity_string)
            # group_name = match.group(3).strip()

            item = DATA_ACCESS_OBJECT.get_inv_type(type_name=type_name)
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
    '''
    Outputs a formated material list
    '''

    for material_type_id, material_quantity in material_list.iteritems():
        material_item = EveOnlineManufacturingJob(DATA_ACCESS_OBJECT,
                                                  type_id=material_type_id)
        material_name = material_item.data_access.get_inv_type(type_id=material_type_id)
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

    building_job_chain = EveOnlineManufacturingJob(DATA_ACCESS_OBJECT,
                                                   type_name=BUILD_PRODUCT_NAME,
                                                   blueprint_me_level=BUILD_PRODUCT_ME,
                                                   manufacturing_runs=BUILD_PRODUCT_RUNS,
                                                   assembly_line_type_name=BUILD_FACILITY)

    if building_job_chain.is_buildable() == False:
        print ("Can not build this item.")
        exit()

    # generate manufacturing job tree
    building_job_chain.manufacturing_data_calculate()

    # set facility for all jobs
    manufacturing_job_list = building_job_chain.get_manufacturing_job_list()

    for job in manufacturing_job_list:
        if job.type_name[0:7] == 'Capital':
            job.blueprint_me_level = 10
            job.assembly_line = EveOnlineRamAssemblyLineTypes(DATA_ACCESS_OBJECT,
                                                              assembly_line_type_name='Thukker Component Assembly Array')

    # Recalculate after setting facility
    asset_dict = create_asset_list(ASSETS_LIST)
    building_job_chain.asset_list = asset_dict
    building_job_chain.manufacturing_data_calculate()

    manufacturing_job_list = building_job_chain.get_manufacturing_job_list()

    for job in manufacturing_job_list:
        print ("level: %d, runs %d (produced %d), %s (ME: %d, Facility: %s)" % (job.build_queue_level,
                                                                                job.manufacturing_runs,
                                                                                job.blueprint_produced_quantity,
                                                                                job.type_name,
                                                                                job.blueprint_me_level,
                                                                                job.assembly_line.assembly_line_type_name
                                                                                ))

    print

    for mat_id, quant in building_job_chain.get_manufacturing_material_list().iteritems():
        e_material_item = EveOnlineManufacturingJob(DATA_ACCESS_OBJECT,
                                                    type_id=mat_id)

        print "%s\t%d" % (e_material_item.type_name, quant)


    print

    refining_type = EveOnlineInvType(DATA_ACCESS_OBJECT,
                                     type_name="White Glaze")

    refining_list = DATA_ACCESS_OBJECT.get_lst_mat_for_rfn(type_id=refining_type.type_id)
    print ("Refining list for %s:" % (refining_type.type_name))

    for mat in refining_list:
        print ("material: %s, quantity: %d" % (DATA_ACCESS_OBJECT.get_inv_type(mat['material_type_id'])['type_name'],
                                               mat['quantity']))

    market = EveMarket(MarketAccessEveCentral())

    print market.market_access_obj.get_marketstats(type_id=34,use_system=30000142)[0]['buy']['max']
    print market.get_price(type_id=34,
                           solar_system_id=30000142,
                           price_type='buy',
                           price_param='max')

if __name__ == '__main__':
    DB_ACCESS_OBJECT = DBAccessSQLite(DATA_FILE)
    DATA_ACCESS_OBJECT = EveDB(DB_ACCESS_OBJECT)

    main()

    DB_ACCESS_OBJECT.close()

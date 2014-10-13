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
BUILD_PRODUCT_ME = 9
BUILD_PRODUCT_PE = 18

ASSETS_LIST = '''Carbon\t1\tGeneral\t\t\t2 m3
Construction Blocks\t13,430\tRefined Commodities\t\t\t20,145 m3
Construction Components Capital\t\tFreight Container\t\t\t250,000 m3
Crystalline Carbonide Armor Plate\t17,676\tConstruction Components\t\t\t17,676 m3
Eifyr and Co. 'Alchemist' Neurotoxin Control NC-903\t1\tCyber Biology\t\t9\t 1 m3
Enormous Freight Container\t8\tFreight Container\t\t\t20,000 m3
Fermionic Condensates\t549\tComposite\t\t\t713.70 m3
Ferrogel\t640\tComposite\t\t\t640 m3
Fullerene Intercalated Sheets\t36\tHybrid Tech Components\t\t\t180 m3
Fullerides\t49,695\tComposite\t\t\t7,454.25 m3
Fusion Reactor Unit\t336\tConstruction Components\t\t\t336 m3
Giant Freight Container\t10\tFreight Container\t\t\t12,000 m3
Guidance Systems\t1,196\tSpecialized Commodities\t\t\t7,176 m3
Hypersynaptic Fibers\t624\tComposite\t\t\t374.40 m3
Ion Thruster\t561\tConstruction Components\t\t\t561 m3
Isogen\t95,023\tMineral\t\t\t950.23 m3
Magnetometric Sensor Cluster\t4,587\tConstruction Components\t\t\t4,587 m3
Maller\t1\tCruiser\t\t\t10,000 m3
Mechanical Parts\t65\tRefined Commodities\t\t\t97.50 m3
Megacyte\t2,035\tMineral\t\t\t20.35 m3
Metallofullerene Plating\t72\tHybrid Tech Components\t\t\t360 m3
Mexallon\t3,329,832\tMineral\t\t\t33,298.32 m3
Morphite\t13,880\tMineral\t\t\t138.80 m3
Nanotransistors\t1,792\tComposite\t\t\t448 m3
Nanowire Composites\t81\tHybrid Tech Components\t\t\t405 m3
Nocxium\t24,525\tMineral\t\t\t245.25 m3
Ore\t\tFreight Container\t\t\t250,000 m3
Oscillator Capacitor Unit\t4,491\tConstruction Components\t\t\t4,491 m3
Phenolic Composites\t3,470\tComposite\t\t\t694 m3
Photon Microprocessor\t11,895\tConstruction Components\t\t\t11,895 m3
Pulse Shield Emitter\t3,775\tConstruction Components\t\t\t3,775 m3
Pyerite\t1,364,724\tMineral\t\t\t13,647.24 m3
R.A.M.- Ammunition Tech\t6,300\tTool\t\t\t252 m3
R.A.M.- Armor/Hull Tech\t200\tTool\t\t\t8 m3
R.A.M.- Electronics\t5,300\tTool\t\t\t212 m3
R.A.M.- Energy Tech\t200\tTool\t\t\t8 m3
R.A.M.- Robotics\t96,900\tTool\t\t\t3,876 m3
R.A.M.- Shield Tech\t200\tTool\t\t\t8 m3
R.A.M.- Starship Tech\t65,880\tTool\t\t\t2,635.20 m3
R.A.M.- Weapon Tech\t5,000\tTool\t\t\t200 m3
Rifter\t6\tFrigate\t\t\t15,000 m3
Robotics\t1,676\tSpecialized Commodities\t\t\t10,056 m3
Sylramic Fibers\t133,256\tComposite\t\t\t6,662.80 m3
Synth Blue Pill Booster Reaction\t1\tSimple Biochemical Reactions\t\t\t1 m3
Terahertz Metamaterials\t1,976\tComposite\t\t\t1,976 m3
Tristan\t4\tFrigate\t\t\t10,000 m3
Tritanium\t6,818,891\tMineral\t\t\t68,188.91 m3
Tungsten Carbide\t511,908\tComposite\t\t\t5,119.08 m3
Venture\t11\tFrigate\t\t\t27,500 m3
Zydrine\t7,431\tMineral\t\t\t74.31 m3
'''

def main():
    '''
    Main function for testing the classes
    '''

    blueprint_me = BUILD_PRODUCT_ME
#    blueprintPE = BUILD_PRODUCT_PE

    e_manuf = EveManufacturing.EveManufacturing(db_access_object, type_name=BUILD_PRODUCT_NAME)

    facility_bonus_ship = e_manuf.get_bonus_for_assembly_line_type(assembly_line_type_name="Advanced Large Ship Assembly Array",
                                                                             activity_id=EVE_ACTIVITY_MANUFACTURING)['base_material_multiplier']

    facility_bonus_component = e_manuf.get_bonus_for_assembly_line_type(assembly_line_type_name="Components Assembly Array",
                                                                        activity_id=EVE_ACTIVITY_MANUFACTURING)['base_material_multiplier']

    asset_dict = {}

    for line in ASSETS_LIST.splitlines():
        match = re.match(r"^(\D+)\t([\d\,]*)\t(\D+)\t.*", line)
        if match is not None:
            type_name = match.group(1).strip()
            quantity_string = match.group(2).replace(',','').strip()
            if quantity_string == '':
                quantity = 0
            else:
                quantity = int(quantity_string)
            group_name = match.group(3).strip()

            item = e_manuf.get_inv_item(type_name=type_name)
            if item is not None:
                type_id = item["type_id"]
                asset_dict[type_id] = quantity
                #--------------- print "In assets %s\t%d" % (type_name,quantity)

    print

    industrial_plan = e_manuf.calculate_build_buy_list(activity_id=EVE_ACTIVITY_MANUFACTURING,
                                                       blueprint_me=blueprint_me,
                                                       facility_bonus=facility_bonus_ship,
                                                       runs=BUILD_PRODUCT_COUNT,
                                                       asset_list=asset_dict)

    print "Building: %s\n" % e_manuf.type_name

    for build_type_id, build_quantity in industrial_plan['build_list'].iteritems():
        build_name = e_manuf.get_inv_item(type_id=build_type_id)
        if build_name is not None:
            print "Build %s\t%d" % (build_name["type_name"], build_quantity)

    print

    for buy_type_id, buy_quantity in industrial_plan['buy_list'].iteritems():
        buy_name = e_manuf.get_inv_item(type_id=buy_type_id)
        if buy_name is not None:
            print "Buy %s\t%d" % (buy_name["type_name"], buy_quantity)

#===============================================================================
#     print
# 
#     for type_id, quantity in industrial_plan['asset_list'].iteritems():
#         name = e_manuf.get_inv_item(type_id=type_id)
#         if name is not None:
#             print "Assets left %s\t%d" % (name["type_name"], quantity)
#===============================================================================

if __name__ == '__main__':
    db_access_object = DBAccessSQLite(DB)

    main()

    db_access_object.close()

'''
Created on 17.6.2014

@author: Pavol Antalik
'''

#import math
import re

from DBAccessSQLite import DBAccessSQLite

from EveOnline.EveMathConstants import EVE_ACTIVITY_MANUFACTURING

from EveOnline.EveManufacturedItem import EveManufacturedItem

DB = 'data/eve.db'

BUILD_PRODUCT_NAME = 'Ark'
BUILD_PRODUCT_RUNS = 1
BUILD_PRODUCT_ME = 5
BUILD_PRODUCT_TE = 0

ASSETS_LIST = '''
Antimatter Reactor Unit\t123\tConstruction Components\t\t\t123 m3
Crystalline Carbonide Armor Plate\t17,676\tConstruction Components\t\t\t17,676 m3
Deflection Shield Emitter\t23\tConstruction Components\t\t\t23 m3
Electrolytic Capacitor Unit\t99\tConstruction Components\t\t\t99 m3
Fernite Carbide Composite Armor Plate\t664\tConstruction Components\t\t\t664 m3
Fusion Reactor Unit\t135\tConstruction Components\t\t\t135 m3
Fusion Thruster\t417\tConstruction Components\t\t\t417 m3
Gravimetric Sensor Cluster\t8\tConstruction Components\t\t\t8 m3
Graviton Reactor Unit\t1,132\tConstruction Components\t\t\t1,132 m3
Ion Thruster\t561\tConstruction Components\t\t\t561 m3
Ladar Sensor Cluster\t52\tConstruction Components\t\t\t52 m3
Linear Shield Emitter\t838\tConstruction Components\t\t\t838 m3
Magnetometric Sensor Cluster\t3,817\tConstruction Components\t\t\t3,817 m3
Magpulse Thruster\t685\tConstruction Components\t\t\t685 m3
Nanoelectrical Microprocessor\t10,191\tConstruction Components\t\t\t10,191 m3
Nanomechanical Microprocessor\t213\tConstruction Components\t\t\t213 m3
Nuclear Reactor Unit\t14\tConstruction Components\t\t\t14 m3
Oscillator Capacitor Unit\t1,815\tConstruction Components\t\t\t1,815 m3
Photon Microprocessor\t6,544\tConstruction Components\t\t\t6,544 m3
Plasma Thruster\t29\tConstruction Components\t\t\t29 m3
Pulse Shield Emitter\t390\tConstruction Components\t\t\t390 m3
Quantum Microprocessor\t815\tConstruction Components\t\t\t815 m3
Radar Sensor Cluster\t1,482\tConstruction Components\t\t\t1,482 m3
Scalar Capacitor Unit\t1,021\tConstruction Components\t\t\t1,021 m3
Sustained Shield Emitter\t454\tConstruction Components\t\t\t454 m3
Tesseract Capacitor Unit\t4,240\tConstruction Components\t\t\t4,240 m3
Titanium Diborite Armor Plate\t7,200\tConstruction Components\t\t\t7,200 m3
Tungsten Carbide Armor Plate\t12,742\tConstruction Components\t\t\t12,742 m3
Condor\t54\tFrigate\t\t\t135,000 m3
Kestrel\t11\tFrigate\t\t\t27,500 m3
Merlin\t105\tFrigate\t\t\t262,500 m3
Morphite\t14,966\tMineral\t\t\t149.66 m3
Construction Blocks\t6,408\tRefined Commodities\t\t\t9,612 m3
R.A.M.- Starship Tech\t81,161\tTool\t\t\t3,246.44 m3
Zydrine\t228\tMineral\t\t\t2.28 m3
Tritanium\t454,637\tMineral\t\t\t4,546.37 m3
Pyerite\t24,586,982\tMineral\t\t\t245,869.82 m3
Nocxium\t325,977\tMineral\t\t\t3,259.77 m3
Mexallon\t141,084\tMineral\t\t\t1,410.84 m3
Megacyte\t140,209\tMineral\t\t\t1,402.09 m3
Isogen\t62,382\tMineral\t\t\t623.82 m3
Tungsten Carbide\t198,034\tComposite\t\t\t1,980.34 m3
Terahertz Metamaterials\t206\tComposite\t\t\t206 m3
Phenolic Composites\t3,959\tComposite\t\t\t791.80 m3
Nanotransistors\t185\tComposite\t\t\t46.25 m3
Hypersynaptic Fibers\t62\tComposite\t\t\t37.20 m3
Fullerides\t5,221\tComposite\t\t\t783.15 m3
Ferrogel\t952\tComposite\t\t\t952 m3
Fermionic Condensates\t304\tComposite\t\t\t395.20 m3
Mexallon\t10,400,000\tMineral\t\t\t104,000 m3
Tritanium\t66,298,756\tMineral\t\t\t662,987.56 m3\t
Capital Antimatter Reactor Unit\t7\tAdvanced Capital Construction Components\t\t\t70 m3
Capital Fusion Thruster\t6\tAdvanced Capital Construction Components\t\t\t60 m3
Capital Linear Shield Emitter\t7\tAdvanced Capital Construction Components\t\t\t70 m3
Capital Nanoelectrical Microprocessor\t10\tAdvanced Capital Construction Components\t\t\t100 m3
Capital Radar Sensor Cluster\t6\tAdvanced Capital Construction Components\t\t\t60 m3
Capital Tesseract Capacitor Unit\t10\tAdvanced Capital Construction Components\t\t\t100 m3
Capital Tungsten Carbide Armor Plate\t15\tAdvanced Capital Construction Components\t\t\t150 m3
Capital Armor Plates\t1\tCapital Construction Components\t\t\t10,000 m3
Capital Cargo Bay\t1\tCapital Construction Components\t\t\t10,000 m3
Capital Construction Parts\t27\tCapital Construction Components\t\t\t270,000 m3
Capital Corporate Hangar Bay\t1\tCapital Construction Components\t\t\t10,000 m3
Capital Jump Drive\t1\tCapital Construction Components\t\t\t10,000 m3
Capital Sensor Cluster\t1\tCapital Construction Components\t\t\t10,000 m3
Capital Shield Emitter\t1\tCapital Construction Components\t\t\t10,000 m3
Crystalline Carbonide\t9,831,635\tComposite\t\t\t98,316.35 m3
Fernite Carbide\t360,959\tComposite\t\t\t3,609.59 m3
Fullerides\t28,767\tComposite\t\t\t4,315.05 m3
Hypersynaptic Fibers\t516\tComposite\t\t\t309.60 m3
Nanotransistors\t61,882\tComposite\t\t\t15,470.50 m3
Nonlinear Metamaterials\t95\tComposite\t\t\t95 m3
Phenolic Composites\t135,464\tComposite\t\t\t27,092.80 m3
Photonic Metamaterials\t2,473\tComposite\t\t\t2,473 m3
Plasmonic Metamaterials\t5,567\tComposite\t\t\t5,567 m3
Terahertz Metamaterials\t1,172\tComposite\t\t\t1,172 m3
Titanium Carbide\t5,298,301\tComposite\t\t\t52,983.01 m3
Providence\t1\tFreighter\t\t\t1000000 m3
R.A.M.- Starship Tech\t10000\tTool\t\t\t1000000 m3
Sylramic Fibers\t18,126\tComposite\t\t\t906.30 m3
Sylramic Fibers\t1,119,257\tComposite\t\t\t55,962.85 m3
'''

#ASSETS_LIST = '''Zydrine\t51732\tMineral\t
#Providence\t1\tShip\t
#'''

#ASSETS_LIST = '''Capital Jump Drive\t29\tCapital Construction Components\t
#'''

#ASSETS_LIST = ''


def create_asset_list(line_list):
    '''
    Generate asset list from text lines
    '''
    asset_dict = {}

    e_asset = EveManufacturedItem(db_access_object)

    for line in line_list.splitlines():
        match = re.match(r"^(\D+)\t([\d\,]*)\t(\D+)\t.*", line)
        if match is not None:
            type_name = match.group(1).strip()
            quantity_string = match.group(2).replace(',', '').strip()
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
        material_item = EveManufacturedItem(db_access_object,
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

    e_built_item = EveManufacturedItem(db_access_object,
                                   type_name=BUILD_PRODUCT_NAME)

    e_built_item.manufacturing_quantity = BUILD_PRODUCT_RUNS
    e_built_item.blueprint_me_level = BUILD_PRODUCT_ME
    e_built_item.assembly_line_type_id = e_built_item.get_assembly_line_type(assembly_line_type_name="Advanced Large Ship Assembly Array")['assemblyLineTypeID']

    #generate manufacturing job tree
    e_built_item.manufacturing_data_calculate()

#    print [job.type_name for job in e_built_item.get_manufacturing_job_list()]

    print "Building: %s\n" % e_built_item.type_name

    #set facility for all jobs
    manufacturing_job_list = e_built_item.get_manufacturing_job_list()

    for job in manufacturing_job_list:
        if job.type_name[0:7] == 'Capital':
            job.assembly_line_type_id = job.get_assembly_line_type(assembly_line_type_name="Thukker Component Assembly Array")['assemblyLineTypeID']

    # Recalculate after setting facility
    asset_dict = create_asset_list(ASSETS_LIST)
    e_built_item.asset_list = asset_dict
    e_built_item.manufacturing_data_calculate()

    manufacturing_job_list = e_built_item.get_manufacturing_job_list()

    for job in manufacturing_job_list:
        print "%s (id %s): runs %d (ME: %d, level %d)" % (job.type_name,
                                                  job.type_id,
                                                  job.manufacturing_quantity,
                                                  job.blueprint_me_level,
                                                  job.build_queue_level)

    print

    print "Building: %s\n" % e_built_item.type_name

    for mat_id, quant in e_built_item.get_manufacturing_material_list().iteritems():
        e_material_item = EveManufacturedItem(db_access_object,
                                          type_id=mat_id)

        print "%s\t%d" % (e_material_item.type_name, quant)


if __name__ == '__main__':
    db_access_object = DBAccessSQLite(DB)

    main()

    db_access_object.close()

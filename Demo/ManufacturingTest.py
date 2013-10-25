'''
Created on 22.10.2013

@author: ridb10157
'''

from EveModules.EveInvType import EveInvType
from EveModules.EveBlueprint import EveInvBlueprintType
from EveManufacturing.EveManufacturingProject import EveManufacturingProject

from Config import *

def main():
    
    proj = EveManufacturingProject(name='Ishtar Project')

    invType = EveInvType(DB, name='Mjolnir Fury Light Missile')
    
    bp = EveInvBlueprintType(DB, productID = invType.getTypeID(), ResearchLevelME = -4, ResearchLevelPE = -4)
    task = proj.addTask(name=invType.getTypeName(), blueprint=bp)

    matList = [(mat.getTypeID(), mat.getTypeName(), mat.getQuantity()) for mat in proj.getMaterialList()]
    for mt in matList:
        print "(%s) %s: %d" % (mt[0], mt[1], mt[2])
    
    print
        
    print "Number of task in project: %d" % proj.getTaskCount()
    print "List of tasks in project: " + format(proj.getTaskNamesList())
#    print "Material list for project: " + format(proj.getProjectMaterialList())
    
if __name__ == '__main__':
    main()
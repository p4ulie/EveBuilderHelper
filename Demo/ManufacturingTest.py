'''
Created on 22.10.2013

@author: ridb10157
'''

from EveModules.EveInvType import EveInvType
from EveModules.EveBlueprintType import EveInvBlueprintType
from EveManufacturing.EveManufacturingProject import EveManufacturingProject

from Config import *

def main():
    
    proj = EveManufacturingProject(name='Ishtar Project')

    invType = EveInvType(DB, name='Mjolnir Fury Light Missile')
    bp = EveInvBlueprintType(DB, productID = invType.getTypeID(), ResearchLevelME = -4, ResearchLevelPE = -4)

    task = proj.addTask(blueprint=bp)
    task.setQuantity(2)

    task = proj.addTask(blueprint=bp)

    print "Number of task in project: %d" % proj.getTaskCount()

    print "List of tasks in project: "
    for task in proj.getTaskList():
        matList = [(mat.getTypeID(), mat.getTypeName(), mat.getQuantity()) for mat in task.getMaterialList()]
        print "%s:" % task.getName()
        for mt in matList:
            print "(%s) %s: %d" % (mt[0], mt[1], mt[2])
        print

#    print "Material list for project: "
#    matList = [(mat.getTypeID(), mat.getTypeName(), mat.getQuantity()) for mat in proj.getMaterialList()]
#     for mt in matList:
#         print "(%s) %s: %d" % (mt[0], mt[1], mt[2])
    
if __name__ == '__main__':
    main()
'''
Created on 22.10.2013

@author: ridb10157
'''

from EveModules.EveInvType import EveInvType
from EveModules.EveBlueprintType import EveInvBlueprintType
from EveManufacturing.EveManufacturingProject import EveManufacturingProject

from Config import *

def main():
    
    proj = EveManufacturingProject(name='Ishtar  Project')

    invType = EveInvType(name='Ishtar')
    bp = EveInvBlueprintType(productID = invType.typeID, ResearchLevelME = -4, ResearchLevelPE = -4)

    task = proj.addTask(blueprint=bp)
    task.manufacturingQuantity = 10

#    task = proj.addTask(blueprint=bp)

    print "Number of task in project: %d\n" % proj.getTaskCount()
    print "List of tasks in project:\n"
    for task in proj.getTaskList():
        print "%s\n" % task.name

#     print "List of tasks in project:\n"
#     for task in proj.getTaskList():
#         taskMatList = [(taskMaterial.typeID, taskMaterial.typeName, taskMaterial.quantity) for taskMaterial in task.getMaterialList()]
#         print "%s:" % task.name
#         for tskMt in taskMatList:
#             print "(%s) %s: %d" % (tskMt[0], tskMt[1], tskMt[2])
# 
#         print

    print "Material list for project: "
    projMatList = [(projMaterial.typeID, projMaterial.typeName, projMaterial.quantity) for projMaterial in proj.getMaterialList()]
    for prjMt in projMatList:
         print "(%s) %s: %d" % (prjMt[0], prjMt[1], prjMt[2])
    
if __name__ == '__main__':
    main()
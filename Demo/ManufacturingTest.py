'''
Created on 22.10.2013

@author: ridb10157
'''

from EveModules.EveInvType import EveInvType
from EveModules.EveInvBlueprintType import EveInvBlueprintType
from EveManufacturing.EveManufacturingProject import EveManufacturingProject

from Config import *

def main():
    # start new project
    proj = EveManufacturingProject(name='Ishtar')

    # add task to project, based on blueprint
    invType = EveInvType(name='Ishtar')
    bp = EveInvBlueprintType(productID = invType.typeID, ResearchLevelME = -4, ResearchLevelPE = -4)
    task = proj.addTask(name=invType.typeName, blueprint=bp, quantity = 1, recursive=True)

    # add task to project, based on blueprint
    invType = EveInvType(name='Myrmidon')
    bp = EveInvBlueprintType(productID = invType.typeID, ResearchLevelME = 0, ResearchLevelPE = 0)
    task = proj.addTask(name=invType.typeName, blueprint=bp, quantity = 1, recursive=True)

    print "Number of task in project: %d\n" % proj.getTaskCount()
    print "List of tasks in project:\n"
    for task in proj.getTaskList():
        print "Manufacturing %s: %d (priority: %d)" % (task.name, task.manufacturingQuantity, task.taskPriority)

#     print
#     
#     print "Material list for project: "
#     projMatList = [(projMaterial.typeID, projMaterial.typeName, projMaterial.quantity) for projMaterial in proj.getMaterialList()]
#     for prjMt in projMatList:
#         print "(%s) %s: %d" % (prjMt[0], prjMt[1], prjMt[2])

if __name__ == '__main__':
    main()
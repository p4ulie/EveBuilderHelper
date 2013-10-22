'''
Created on 22.10.2013

@author: ridb10157
'''

from EveManufacturing.EveManufacturingProject import EveManufacturingProject

def main():
    proj = EveManufacturingProject(name='Ishtar Project')
    proj.addTask()

    print "Number of task in project: %d" % proj.getTaskCount()
    print "List of tasks in project: " + format(proj.getTaskList())
    print "Material list for project: " + format(proj.getProjectMaterialList())
    
if __name__ == '__main__':
    main()
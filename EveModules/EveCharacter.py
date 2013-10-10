'''
Created on 9.10.2013

@author: Pavol Antalik
'''

class EveCharacter(object):
    '''
    Eve Online character data
    '''

    charID = None
    name = ''
    skills = {}

    def addSkill(self, skillName, skillLevel):
        '''
        Add skill to the list
        '''
        self.skills[skillName] = skillLevel
    
    def getSkillLevel(self, skillName):
        '''
        Return level of skill
        '''
        skillLevel = None

        if skillName in self.skills.keys():
            skillLevel = self.skills[skillName]

        return skillLevel
    
    def __init__(self, name = ''):
        '''
        Constructor
        '''
        if name is not None:
            self.name = name
        
'''
Created on 19.6.2014

@author: Pavol Antalik

Various functions to handle Eve Online industry related math (material calculations, ...)
'''

def calculateMEMultiplier(blueprintMELevel = 0, facilityBonus = 0):
    '''
    Calculate material multiplier for specified ME Blueprint Research level
    and facility bonus
    '''
    multiplier = ( ( 100 - float(blueprintMELevel) ) / 100 ) * facilityBonus
    
    return multiplier

def calculateTEMultiplier(blueprintTELevel = 0, facilityBonus = 0):
    '''
    Calculate material multiplier for specified TE Blueprint Research level
    and character skills
    '''


if __name__ == '__main__':
    pass
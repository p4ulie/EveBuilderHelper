'''
Created on 19.6.2014

@author: Pavol Antalik

Various functions to handle Eve Online industry related math (material calculations, ...)
'''


def calculate_me_multiplier(blueprint_me_level=0, facility_multiplier=None):
    '''
    Calculate material multiplier for specified ME Blueprint Research level
    and facility bonus
    '''
    multiplier = ((100 - float(blueprint_me_level)) / 100)

    if facility_multiplier is not None:
        multiplier = multiplier * facility_multiplier

    return multiplier


def calculate_te_multiplier(blueprint_te_level=0, facility_bonus=None):
    '''
    Calculate material multiplier for specified TE Blueprint Research level
    and character skills
    '''

    multiplier = ((100 - float(blueprint_te_level)) / 100)

    if facility_bonus is not None:
        multiplier = multiplier * facility_bonus

    return multiplier

if __name__ == '__main__':
    pass

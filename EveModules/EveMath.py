'''
Created on 19.6.2014

@author: Pavol Antalik

Various functions to handle Eve related math (material calculations, ...)
'''

def calculateWasteFromBlueprintMELevel(materialAmount,
                                       wasteFactor,
                                       blueprintMELevel = 0):
    '''
    Calculate waste for specific ME Blueprint Research level
    '''
    if blueprintMELevel >= 0:
        waste = round(float(materialAmount) * (float(wasteFactor) / 100) * (1 / (float(blueprintMELevel) + 1)))
    else:
        waste = round(float(materialAmount) * (float(wasteFactor) / 100) * (1 - float(blueprintMELevel)))

    return int(waste)

def calculateWasteFromCharacterTEskillLevel(materialAmount,
                                            characterTEskillLevel = 0):
    '''
    Calculate waste for trained Production Efficiency skill level
    '''
    waste = round(((25 - (5 * float(characterTEskillLevel))) * float(materialAmount)) / 100)

    return int(waste)

if __name__ == '__main__':
    pass
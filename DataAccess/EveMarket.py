'''
Created on 06.11.2016

@author: Pavol Antalik
'''

import json
import re
from EveOnline.EveMathConstants import EVE_ACTIVITY_MANUFACTURING


class EveMarket(object):
    '''
    Class for accessing EVE Online market price
    market_access_obj can point to objects that access specific data sources - DB, Eve-Central, Crest, ...
    '''

    def __init__(self,
                 market_access_obj):
        '''
        Constructor
        '''

        self.market_access_obj = market_access_obj

    def get_price(self,
                  type_id=None,
                  solar_system_id=None,
                  price_type=None,
                  price_param=None):
        '''
        :param type_id:
        :param solar_system_id:
        :return:
        '''

        price_data = self.market_access_obj.get_marketstats(type_id=type_id,
                                                            use_system=solar_system_id)

        if price_type is not None:
            if price_param is not None:
                return price_data[0][price_type][price_param]
        else:
            return price_data
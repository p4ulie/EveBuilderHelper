'''
Created on 18.6.2014

@author: Pavol Antalik
'''

import types
import datetime
import requests
import requests_cache

class MarketAccessEveCentral(object):
    '''
    Class for accessing Eve-Central database
    '''

    BASE_URL = 'https://api.eve-central.com/api'
    CACHE_EXPIRE_AFTER = 3600 # expire after specified number of seconds

    def __init__(self,
                 base_url=None,
                 use_cache=True):
        '''
        Constructor
        '''

        if base_url is not None:
            self.BASE_URL = base_url

        if use_cache:
            expire_after = datetime.timedelta(seconds=self.CACHE_EXPIRE_AFTER)
            requests_cache.install_cache(expire_after=expire_after)
            requests_cache.core.remove_expired_responses()

    def get_marketstats(self,
                        type_id=None,
                        use_system=None,
                        region_limit=None,
                        min_quantity=None,
                        hours=None):
        '''
        :param type_id_list: ID or list of IDs
        :return: dictionary with market data
        '''

        api_method = '/marketstat/json'

        url = self.BASE_URL + api_method

        payload = []

        if type_id is not None:
            if isinstance(type_id, types.ListType):
                type_id_list = [('type_id', id) for id in type_id]
            else:
                type_id_list = [('typeid', type_id)]

            payload.extend(type_id_list)

            if use_system is not None:
                payload.append(('usesystem', use_system))

            r = requests.get(url, params=payload)

            return r.json()

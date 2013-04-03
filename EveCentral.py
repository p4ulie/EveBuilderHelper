'''
Classes for accessing Eve-Central

Created on 2.8.2012

@author: PA
'''

from urllib2 import urlopen
from urllib import urlencode
from xml.dom import minidom
#import EveDB

'''
Eve Central API documentation: http://dev.eve-central.com/evec-api/start
'''


class EveCentral(object):
    '''
    Basic class for interacting with EveDB
    '''

    EVE_CENTRAL_BASE_URI = 'http://api.eve-central.com/api/'

    def __fetchData(self, url, args):
        '''
        Main method for accessing the Eve-Central API
        '''
        result = None

        result = urlopen(url, args).read()

        return result

    #===========================================================================
    # def getItemDataByTypeID(self, items):
    #    '''
    #    Get item data from Eve-Central by TypeID,
    #    multiple typeID can be specified in a list
    #    '''
    #    args = []
    #    for item in items:
    #        args.append(('typeid', item))
    #    encargs = urlencode(args)
    #    xmlresult = self.__fetchData("marketstat", encargs)
    #    return xmlresult
    #===========================================================================

    def marketstatParse(self, tradeData, typeID, orderType, attributeName):
        '''
        Parse XML data returned by marketstatGet() call,
        return the attribute specified by orderType and attributeName
        '''
        result = None
        xmldoc = minidom.parseString(tradeData)
        for node in xmldoc.getElementsByTagName('type'):
            if node.getAttribute('id') == str(typeID):
                for data in node.getElementsByTagName(orderType)[0].getElementsByTagName(attributeName):
                    result = data.firstChild.data
        return float(result)

    def marketstatGet(self, typeID, setHours, regionLimit, useSystem, setMinQ):
        '''
        Endpoint: http://api.eve-central.com/api/marketstat
        Purpose: Retrieve aggregate statistics for the items specified.
        Parameters: hours     Statistics from the last X specified hours. Defaults to 24.
                    typeid     The type ID of the item you are requesting. I.e., 34 for Tritanium. Can be specified more than once
                    minQ     The minimum quantity in an order to consider it for the statistics
                    regionlimit     Restrict statistics to a region. Can be specified more than once.
                    usesystem     Restrict statistics to a system.
        '''
        args = []

        url = self.EVE_CENTRAL_BASE_URI + 'marketstat'

        xmlresult = ''

        if typeID:
            args.append(('typeid', typeID))

            if setHours:
                args.append(('setHours', setHours))

            if regionLimit:
                for region in regionLimit:
                    args.append(('regionlimit', region))

            if useSystem:
                args.append(('useSystem', useSystem))

            if setMinQ:
                args.append(('setMinQ', setMinQ))

            encargs = urlencode(args)
#            print encargs
            xmlresult = self.__fetchData(url, encargs)
        return xmlresult

    def quicklookParse(self, tradeData, orderType):
        '''
        Parse XML data returned by quicklookGet() call,
        return the attribute specified by orderType and attributeName
        '''
        result = []
        xmldoc = minidom.parseString(tradeData)
        for node in xmldoc.getElementsByTagName(orderType):
            for order in node.getElementsByTagName('order'):
                row = []
                row.append(order.getElementsByTagName('region')[0].firstChild.data)
                row.append(order.getElementsByTagName('station')[0].firstChild.data)
                row.append(order.getElementsByTagName('station_name')[0].firstChild.data)
                row.append(order.getElementsByTagName('security')[0].firstChild.data)
                row.append(order.getElementsByTagName('range')[0].firstChild.data)
                row.append(order.getElementsByTagName('price')[0].firstChild.data)
                row.append(order.getElementsByTagName('vol_remain')[0].firstChild.data)
                row.append(order.getElementsByTagName('min_volume')[0].firstChild.data)
                row.append(order.getElementsByTagName('expires')[0].firstChild.data)
                row.append(order.getElementsByTagName('reported_time')[0].firstChild.data)
                result.append(row)
        return result

    def quicklookGet(self, typeID, setHours, regionLimit, useSystem, setMinQ):
        '''
        Endpoint: http://api.eve-central.com/api/quicklook
        Purpose: Retrieve all of the available market orders, including prices, stations, order IDs, volumes, etc.
        Parameters: typeid     The type ID to be queried
                    sethours     Get orders which have been posted within the last X hours. Defaults to 360
                    regionlimit     Restrict the view to only show from within the specified region IDs. Can be specified multiple times.
                    usesystem     Restrict the view to the following system only
                    setminQ     Restrict the view to show only orders above the specified quantity
        '''
        args = []

        url = self.EVE_CENTRAL_BASE_URI + 'quicklook'

        xmlresult = ''

        if typeID:
            args.append(('typeid', typeID))

            if setHours:
                args.append(('setHours', setHours))

            if regionLimit:
                for region in regionLimit:
                    args.append(('regionlimit', region))

            if useSystem:
                args.append(('useSystem', useSystem))

            if setMinQ:
                args.append(('setMinQ', setMinQ))

            encargs = urlencode(args)
            xmlresult = self.__fetchData(url, encargs)
        return xmlresult

    def quicklookGetList(self, typeID, setHours, regionLimit, useSystem, setMinQ, orderType):
        xmlresult = self.quicklookGet(typeID, setHours, regionLimit, useSystem, setMinQ)
        result = self.quicklookParse(xmlresult, orderType)

    def __init__(self):
        '''
        Constructor
        '''

if __name__ == '__main__':
    pass

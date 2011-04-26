#!/usr/bin/env python

from BeautifulSoup import BeautifulStoneSoup
from vars import ConnectionParameters
import urllib2


class AddOnsAPI(object):
               
    def __init__(self, search_extension = 'firebug'):
        self.api_base_url = ConnectionParameters.baseurl + '/en-us/firefox/api/1.5/search/'
        self.search_url = self.api_base_url + search_extension      
        self.parsed_xml = BeautifulStoneSoup(urllib2.urlopen(self.search_url) )
        
    def get_name_of_first_addon(self):
        name_of_first_addon_listed = self.parsed_xml.searchresults.addon.nameTag.contents[0]
        return name_of_first_addon_listed
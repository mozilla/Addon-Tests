#!/usr/bin/env python

from BeautifulSoup import BeautifulStoneSoup
from vars import ConnectionParameters
import urllib2


class AddOnsAPI(object):
               
    def __init__(self, search_extension = 'firebug'):
        self.api_base_url = ConnectionParameters.baseurl + '/en-us/firefox/api/1.5/search/'
        self.search_url = self.api_base_url + search_extension      
        self.parsed_xml = BeautifulStoneSoup(urllib2.urlopen(self.search_url) )
    
    def get_addon_id(self, addon_name):
        numeric_id =  self.parsed_xml.find(text=addon_name).findParent().findParent().attrs[0] #"get id for addon name"
        return numeric_id[1]
        
    def get_name_of_first_addon(self):
        name_of_first_addon_listed = self.parsed_xml.searchresults.addon.nameTag.contents[0]
        return name_of_first_addon_listed

    def get_addon_type_name(self):
        addon_type_name = self.parsed_xml.addon.type.string
        return addon_type_name
        
    def get_addon_type_id(self):
        addon_type_id = self.parsed_xml.addon.type["id"]
        return addon_type_id
        
    def get_addon_version_number(self):
        addon_version_number = self.parsed_xml.addon.version.string
        return addon_version_number
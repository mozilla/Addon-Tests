#!/usr/bin/env python

from BeautifulSoup import BeautifulStoneSoup
from selenium import selenium
from vars import ConnectionParameters
import unittest2 as unittest
import urllib2
#import sys
#from nose.plugins.multiprocess import MultiProcess
#import pytest
#xfail = pytest.mark.xfail

#https://addons.allizom.org/en-us/firefox/api/1.5/search/firebug

class AddOnsAPI(object):
               
    def __init__(self, search_extension = 'firebug'):
        self.api_base_url = ConnectionParameters.baseurl + '/en-us/firefox/api/1.5/search/'
        self.search_url = self.api_base_url + search_extension      
        self.parsed_xml = BeautifulStoneSoup(urllib2.urlopen(self.search_url) )
        
    def get_name_of_first_addon(self):
        name_of_first_addon_listed = self.parsed_xml.searchresults.addon.nameTag.contents[0]
        return name_of_first_addon_listed
            
class APITests(unittest.TestCase):
    
    def setUp(self):
        self.selenium = selenium(ConnectionParameters.server, 
                                    ConnectionParameters.port,
                                    ConnectionParameters.browser, 
                                    ConnectionParameters.baseurl)
        #self.selenium.start()
        #self.selenium.set_timeout(ConnectionParameters.page_load_timeout)

    def tearDown(self):
       #self.selenium.stop() 
       pass

    def test_check_that_firebug_is_listed_first_in_addons_search_for_fire(self):  
        """ TestCase for Litmus 15314 """       
        addons_xml = AddOnsAPI('fire')
        self.assertEquals("Firebug", addons_xml.get_name_of_first_addon())

    def test_check_that_firebug_is_listed_first_in_addons_search_for_firebug(self):  
        """ TestCase for Litmus 15316 """
        addons_xml = AddOnsAPI()
        self.assertEquals("Firebug", addons_xml.get_name_of_first_addon())
                    
if __name__ == "__main__":
    unittest.main()

            
        
        
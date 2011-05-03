#!/usr/bin/env python

from addons_api import AddOnsAPI
import unittest2 as unittest
#import pytest
#xfail = pytest.mark.xfail

#These tests should only call the api.  There should be no tests requiring selenium in this class.
class APIOnlyTests(unittest.TestCase):
    
    def setUp(self):
        self.addons_xml = AddOnsAPI()
        
    def test_get_addon_type_name(self):
        self.assertEquals("Extension", self.addons_xml.get_addon_type_name("Firebug"))#("Firefox 3 theme for Firefox 4"))
        
    def test_get_version_number(self):
        self.assertEquals("1.1.6", self.addons_xml.get_addon_version_number("Illuminations for Developers for Firebug"))
                
    def test_addon_is_not_in_search_results(self):
        self.assertRaises(AttributeError, self.addons_xml.get_xml_for_single_addon("Firepug"))
    
    def test_first_addon_fails_when_addon_is_not_in_results(self):
        bad_xml = AddOnsAPI("Firepug")
        self.assertRaises(AttributeError, bad_xml.get_name_of_first_addon())
    
    def test_addon_type_fails_when_addon_is_not_in_results(self):
        self.assertRaises(AttributeError, self.addons_xml.get_addon_type_id("Firepug"))
        self.assertRaises(AttributeError, self.addons_xml.get_addon_type_name("Firepug"))
    
    def test_addon_version_number_fails_when_addon_is_not_in_results(self):
        self.assertRaises(AttributeError, self.addons_xml.get_addon_version_number("Firepug"))
             
if __name__ == "__main__":
    unittest.main()
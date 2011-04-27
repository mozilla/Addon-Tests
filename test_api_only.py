#!/usr/bin/env python

from addons_api import AddOnsAPI
import unittest2 as unittest
#import pytest
#xfail = pytest.mark.xfail

#These tests should only call the api.  There should be no tests requiring selenium in this class.
class APIOnlyTests(unittest.TestCase):

    def test_that_firebug_is_listed_first_in_addons_search_for_fire(self):  
        """ TestCase for Litmus 15314 """       
        addons_xml = AddOnsAPI('fire')
        self.assertEquals("Firebug", addons_xml.get_name_of_first_addon())

    def test_that_firebug_is_listed_first_in_addons_search_for_firebug(self):  
        """ TestCase for Litmus 15316 """
        addons_xml = AddOnsAPI()
        self.assertEquals("Firebug", addons_xml.get_name_of_first_addon())

	def test_that_firebug_addon_type_name_is_extension(self):
		"Testcase for Litmus 15316"
		addons_xml = AddOnsAPI()
		self.assertEquals("Extension", addons_xml.get_addon_type_name())
	
	def test_that_firebug_addon_type_id_is_1(self):
		"Testcase for Litmus 15316"
		addon_xml = AddonsAPI()
		self.assertEquals("1", addons_xml.get_addon_type_id())
	
	def test_firebug_version_number(self):
		"Testcase for Litmus 15317"
		addon_xml = AddonsAPI()
		print addon_xml.get_addon_version_number()
		self.assertEquals("1.7.0", addons_xml.get_addon_version_number())
                    
if __name__ == "__main__":
    unittest.main()
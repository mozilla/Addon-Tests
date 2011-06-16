#!/usr/bin/env python

from addons_api import AddOnsAPI
from unittestzero import Assert
import pytest

#These tests should only call the api.
#There should be no tests requiring selenium in this class.

class TestAPIOnlyTests:
    def test_that_firebug_is_listed_first_in_addons_search_for_fire(self, testsetup):
        """TestCase for Litmus 15314"""
        testsetup.skip_selenium = True
        addons_xml = AddOnsAPI(testsetup, 'fire')
        Assert.equal("Firebug", addons_xml.get_name_of_first_addon())

    def test_that_firebug_is_listed_first_in_addons_search_for_firebug(self, testsetup):  
        """TestCase for Litmus 15316"""
        addons_xml = AddOnsAPI(testsetup)
        Assert.equal("Firebug", addons_xml.get_name_of_first_addon())

    def test_that_firebug_addon_type_name_is_extension(self, testsetup):
        """Testcase for Litmus 15316"""
        addons_xml = AddOnsAPI(testsetup)
        Assert.equal("Extension", addons_xml.get_addon_type_name("Firebug"))
    
    def test_that_firebug_addon_type_id_is_1(self, testsetup):
        """Testcase for Litmus 15316"""
        addon_xml = AddOnsAPI(testsetup)
        Assert.equal("1", addon_xml.get_addon_type_id("Firebug"))
    
    def test_firebug_version_number(self, testsetup):
        """Testcase for Litmus 15317"""
        addon_xml = AddOnsAPI(testsetup)
        Assert.equal("1.7.0", addon_xml.get_addon_version_number("Firebug"))
                    
if __name__ == "__main__":
    unittest.main()
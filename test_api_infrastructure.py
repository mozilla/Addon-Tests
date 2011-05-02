#!/usr/bin/env python

from addons_api import AddOnsAPI
import unittest2 as unittest
#import pytest
#xfail = pytest.mark.xfail

#These tests should only call the api.  There should be no tests requiring selenium in this class.
class APIOnlyTests(unittest.TestCase):

    def test_get_firebug_addon_id(self):
        addons_xml = AddOnsAPI('fire')
        self.assertEquals("1843", addons_xml.get_addon_id("Firebug"))
        
    def test_get_firegestures_addon_id(self):
        addons_xml = AddOnsAPI()
        self.assertEquals("11905", addons_xml.get_addon_id("Firefinder for Firebug"))
                    
if __name__ == "__main__":
    unittest.main()
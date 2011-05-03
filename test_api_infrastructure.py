#!/usr/bin/env python

from addons_api import AddOnsAPI
import unittest2 as unittest
#import pytest
#xfail = pytest.mark.xfail

#These tests should only call the api.  There should be no tests requiring selenium in this class.
class APIOnlyTests(unittest.TestCase):
        
    def test_get_addon_type_name(self):
        addons_xml = AddOnsAPI()
        self.assertEquals("Extension", addons_xml.get_addon_type_name("Firebug"))#("Firefox 3 theme for Firefox 4"))
        
    def test_get_firefinder_version_number(self):
        addons_xml = AddOnsAPI()
        self.assertEquals("1.1.6", addons_xml.get_addon_version_number("Illuminations for Developers for Firebug"))
                    
if __name__ == "__main__":
    unittest.main()
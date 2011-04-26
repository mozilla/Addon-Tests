#!/usr/bin/env python

from addons_api import AddOnsAPI
import unittest2 as unittest
#import pytest
#xfail = pytest.mark.xfail

#These tests should only call the api.  There should be no tests requiring selenium in this class.
class APIOnlyTests(unittest.TestCase):

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
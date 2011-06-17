#!/usr/bin/env python

from addons_api import AddOnsAPI
from unittestzero import Assert
import pytest

#These tests should only call the api.  There should be no tests requiring selenium in this class.
class TestAPIOnlyTests():
            
    @pytest.mark.skip_selenium  
    def test_get_addon_type_name(self, testsetup):
        addons_xml = AddOnsAPI(testsetup)
        Assert.equal("Extension", addons_xml.get_addon_type_name("Firebug"))#("Firefox 3 theme for Firefox 4"))
        
    @pytest.mark.skip_selenium
    def test_get_version_number(self, testsetup):
        addons_xml = AddOnsAPI(testsetup)
        Assert.equal("1.1.6", addons_xml.get_addon_version_number("Illuminations for Developers for Firebug"))
                
    @pytest.mark.skip_selenium
    def test_addon_is_not_in_search_results(self, testsetup):
        addons_xml = AddOnsAPI(testsetup)
        Assert.raises(AttributeError, addons_xml.get_xml_for_single_addon("Firepug"))
    
    @pytest.mark.skip_selenium
    def test_first_addon_fails_when_addon_is_not_in_results(self, testsetup):
        addons_xml = AddOnsAPI(testsetup)
        bad_xml = AddOnsAPI("Firepug")
        #try:
        Assert.raises (AttributeError, addons_xml )#self.bad_xml.get_name_of_first_addon())
        #except AssertionError:
        #pass

    @pytest.mark.skip_selenium       
    def test_that_assert_raises_catches_exceptions(self):
        Assert.raises(ZeroDivisionError, self._divide_by_zero)

    @pytest.mark.skip_selenium
    def test_that_we_raise_when_error_not_thrown(self):
        try:
            Assert.raises(Exception, self._add_num, 5,4)
        except AssertionError:
            pass

    def _divide_by_zero(self):
        return 1/0

    def _add_num(self, first, second):
        return first + second            
            
            
    
    @pytest.mark.skip_selenium
    def test_addon_type_fails_when_addon_is_not_in_results(self, testsetup):
        addons_xml = AddOnsAPI(testsetup)
        try:
            Assert.raises(AttributeError, addons_xml.get_addon_type_id("Firepug") )
        except AssertionError:
            pass
        #Assert.raises(AttributeError, addons_xml.get_addon_type_name("Firepug"))
    
    @pytest.mark.skip_selenium
    def test_addon_version_number_fails_when_addon_is_not_in_results(self, testsetup):
        addons_xml = AddOnsAPI(testsetup)
        Assert.raises(AttributeError, addons_xml.get_addon_version_number("Firepug"))
             
if __name__ == "__main__":
    unittest.main()
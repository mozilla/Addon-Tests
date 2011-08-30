#!/usr/bin/env python

from addons_api import AddOnsAPI
from unittestzero import Assert
import pytest

#These tests should only call the api.
#There should be no tests requiring selenium in this class.


@pytest.mark.skip_selenium
class TestAPIOnlyTests:

    def test_that_firebug_is_listed_first_in_addons_search_for_fire(self, mozwebqa):
        """TestCase for Litmus 15314"""
        addons_xml = AddOnsAPI(mozwebqa, 'fire')
        Assert.equal("Firebug", addons_xml.get_name_of_first_addon())

    def test_that_firebug_is_listed_first_in_addons_search_for_firebug(self, mozwebqa):
        """TestCase for Litmus 15316"""
        addons_xml = AddOnsAPI(mozwebqa)
        Assert.equal("Firebug", addons_xml.get_name_of_first_addon())

    def test_that_firebug_addon_type_name_is_extension(self, mozwebqa):
        """Testcase for Litmus 15316"""
        addons_xml = AddOnsAPI(mozwebqa)
        Assert.equal("Extension", addons_xml.get_addon_type_name("Firebug"))

    def test_that_firebug_addon_type_id_is_1(self, mozwebqa):
        """Testcase for Litmus 15316"""
        addon_xml = AddOnsAPI(mozwebqa)
        Assert.equal("1", addon_xml.get_addon_type_id("Firebug"))

    def test_firebug_version_number(self, mozwebqa):
        """Testcase for Litmus 15317"""
        addon_xml = AddOnsAPI(mozwebqa)
        Assert.equal("1.8.1", addon_xml.get_addon_version_number("Firebug"))

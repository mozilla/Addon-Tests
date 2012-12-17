#!/usr/bin/env python
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from unittestzero import Assert

from pages.desktop.addons_api import AddOnsAPI

#These tests should only call the api.
#There should be no tests requiring selenium in this class.


@pytest.mark.skip_selenium
class TestAPIOnlyTests:

    @pytest.mark.nondestructive
    def test_that_firebug_is_listed_in_top_five_search_results_for_fire(self, mozwebqa):
        """Test for Litmus 15314."""
        addons_xml = AddOnsAPI(mozwebqa, 'fire')
        assert any("Firebug" in name for name in
                   addons_xml.get_name_of_top_addons(count=5)
                   ), "Firebug was not found in the top 5 search results for 'fire'."

    @pytest.mark.nondestructive
    def test_that_firebug_is_listed_first_in_addons_search_for_firebug(self, mozwebqa):
        """Test for Litmus 15316."""
        addons_xml = AddOnsAPI(mozwebqa)
        Assert.equal("Firebug", addons_xml.get_name_of_first_addon())

    @pytest.mark.nondestructive
    def test_that_firebug_addon_type_name_is_extension(self, mozwebqa):
        """Test for Litmus 15316."""
        addons_xml = AddOnsAPI(mozwebqa)
        Assert.equal("Extension", addons_xml.get_addon_type_name("Firebug"))

    @pytest.mark.nondestructive
    def test_that_firebug_addon_type_id_is_1(self, mozwebqa):
        """Test for Litmus 15316."""
        addon_xml = AddOnsAPI(mozwebqa)
        Assert.equal("1", addon_xml.get_addon_type_id("Firebug"))

    @pytest.mark.nondestructive
    def test_firebug_version_number(self, mozwebqa):
        """Test for Litmus 15317."""
        addon_xml = AddOnsAPI(mozwebqa)
        Assert.equal("1.10.6", addon_xml.get_addon_version_number("Firebug"))

    @pytest.mark.nondestructive
    def test_that_firebug_status_id_is_4_and_fully_reviewed(self, mozwebqa):
        """Test for Litmus 15318."""
        addon_xml = AddOnsAPI(mozwebqa)
        Assert.equal("4", addon_xml.get_addon_status("Firebug")[0])
        Assert.equal("Fully Reviewed", addon_xml.get_addon_status("Firebug")[1])

    @pytest.mark.nondestructive
    def test_that_firebug_has_install_link(self, mozwebqa):
        """Test for Litmus 15327."""
        addon_xml = AddOnsAPI(mozwebqa)
        Assert.contains("fx.xpi?src=api", addon_xml.get_install_link("Firebug"))

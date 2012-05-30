#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import re
import pytest

from unittestzero import Assert

from pages.desktop.discovery import DiscoveryPane
from pages.desktop.home import Home


class TestDiscoveryPane:
    """This only works with Firefox 4."""

    #Need to get this info before run
    basepath = '/en-US/firefox/discovery/pane/4.0/Darwin'

    @pytest.mark.nondestructive
    def test_that_users_with_less_than_3_addons_get_what_are_addons(self, mozwebqa):
        """
        Test for Litmus 15063.
        Since Selenium starts with a clean profile all the time this will always have
        less than 3 addons.
        """
        discovery_pane = DiscoveryPane(mozwebqa, self.basepath)
        what_are_addons_expected = "Add-ons are applications that let you personalize "
        what_are_addons_expected += "Firefox with extra functionality or style. Try a time-saving"
        what_are_addons_expected += " sidebar, a weather notifier, or a themed look to make "
        what_are_addons_expected += "Firefox your own.\nLearn More"

        Assert.equal(what_are_addons_expected, discovery_pane.what_are_addons_text)

    @pytest.mark.nondestructive
    def test_that_mission_statement_is_on_addons_home_page(self, mozwebqa):
        """Test for Litmus 15065."""
        discovery_pane = DiscoveryPane(mozwebqa, self.basepath)
        expected_text = "Thanks for using Firefox and supporting Mozilla's mission!"

        mission_text = discovery_pane.mission_section
        Assert.true(expected_text in mission_text)
        Assert.true(discovery_pane.mozilla_org_link_visible())
        download_count_regex = "Add-ons downloaded: (.+)"
        Assert.true(re.search(download_count_regex, discovery_pane.download_count) != None)

    @pytest.mark.nondestructive
    def test_that_featured_personas_is_present_and_has_5_item(self, mozwebqa):
        """Test for Litmus 15079, 15080."""
        discovery_pane = DiscoveryPane(mozwebqa, self.basepath)
        Assert.true(discovery_pane.is_personas_section_visible)
        Assert.equal(5, discovery_pane.personas_count)
        Assert.true(discovery_pane.is_personas_see_all_link_visible)

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_featured_personas_go_to_their_landing_page_when_clicked(self, mozwebqa):
        """Test for Litmus 15081."""
        discovery_pane = DiscoveryPane(mozwebqa, self.basepath)
        first_persona = discovery_pane.first_persona
        persona = discovery_pane.click_on_first_persona()
        Assert.equal(first_persona, persona.persona_title)

    @pytest.mark.nondestructive
    def test_that_more_ways_to_customize_section_is_available(self, mozwebqa):
        """Test for Litmus 15082."""
        discovery_pane = DiscoveryPane(mozwebqa, self.basepath)
        Assert.true(discovery_pane.more_ways_section_visible)
        Assert.equal("Browse all add-ons", discovery_pane.browse_all_addons)
        Assert.equal("See all themes", discovery_pane.see_all_themes)

    @pytest.mark.nondestructive
    def test_that_up_and_coming_is_present_and_had_5_items(self, mozwebqa):
        """Test for Litmus 15074."""
        discovery_pane = DiscoveryPane(mozwebqa, self.basepath)
        Assert.equal(5, discovery_pane.up_and_coming_item_count)

    @pytest.mark.nondestructive
    @pytest.mark.login
    def test_the_logout_link_for_logged_in_users(self, mozwebqa):
        """
        Test for Litmus 15110.
        https://litmus.mozilla.org/show_test.cgi?id=15110
        """
        home_page = Home(mozwebqa)
        home_page.login("browserID")
        Assert.true(home_page.is_the_current_page)
        Assert.true(home_page.header.is_user_logged_in)

        discovery_pane = DiscoveryPane(mozwebqa, self.basepath)
        home_page = discovery_pane.click_logout()
        Assert.true(home_page.is_the_current_page)
        Assert.false(home_page.header.is_user_logged_in)

    @pytest.mark.smoke
    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_carousel_works(self, mozwebqa):
        """
        Test for Litmus 15071.
        https://litmus.mozilla.org/show_test.cgi?id=15071
        """
        discovery_pane = DiscoveryPane(mozwebqa, self.basepath)
        slider2 = ''

        #checking > button works and slides change
        for i in range(0, len(discovery_pane.sliders)):
            slider1 = discovery_pane.sliders[i].header_name
            Assert.not_equal(slider1, slider2)
            Assert.greater(discovery_pane.sliders[i].opacity_value_for_next, 0.3)
            discovery_pane.sliders[i].click_next()
            slider2 = slider1

        #checking < button works and slides change
        for i in range(0, len(discovery_pane.sliders)):
            slider1 = discovery_pane.sliders[i].header_name
            Assert.not_equal(slider1, slider2)
            Assert.greater(discovery_pane.sliders[i].opacity_value_for_previous, 0.3)
            discovery_pane.sliders[i].click_previous()
            slider2 = slider1

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_extension_is_underlined_while_hover_and_text_not(self, mozwebqa):
        """
        Test for Litmus 15118.
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=15118
        """
        discovery_pane = DiscoveryPane(mozwebqa, self.basepath)

        Assert.equal(discovery_pane.hover_over_extension_and_get_css_property_for_title, "underline")
        Assert.equal(discovery_pane.hover_over_extension_and_get_css_property_for_text, "none")

#!/usr/bin/env python

# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is Mozilla WebQA Selenium Tests.
#
# The Initial Developer of the Original Code is
# Mozilla.
# Portions created by the Initial Developer are Copyright (C) 2011
# the Initial Developer. All Rights Reserved.
#
# Contributor(s): David Burns
#                 Dave Hunt <dhunt@mozilla.com>
#                 Marlena Compton <mcompton@mozilla.com
#                 Alin Trif <alin.trif@softvision.ro>
#                 Teodosia Pop <teodosia.pop@softvision.ro>
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
#
# ***** END LICENSE BLOCK *****


import re
import pytest

from unittestzero import Assert

from pages.discovery import DiscoveryPane
from pages.home import Home

nondestructive = pytest.mark.nondestructive


class TestDiscoveryPane:
    """ This only works with Firefox 4 """

    #Need to get this info before run
    basepath = '/en-US/firefox/discovery/pane/4.0/Darwin'

    @nondestructive
    def test_that_users_with_less_than_3_addons_get_what_are_addons(self, mozwebqa):
        """ Test case for litmus 15063 -
        Since Selenium starts with a clean profile all the time this will always have
        less than 3 addons
        """
        discovery_pane = DiscoveryPane(mozwebqa, self.basepath)
        what_are_addons_expected = "Add-ons are applications that let you personalize "
        what_are_addons_expected += "Firefox with extra functionality or style. Try a time-saving"
        what_are_addons_expected += " sidebar, a weather notifier, or a themed look to make "
        what_are_addons_expected += "Firefox your own.\nLearn More"

        Assert.equal(what_are_addons_expected, discovery_pane.what_are_addons_text)

    @nondestructive
    def test_that_mission_statement_is_on_addons_home_page(self, mozwebqa):
        """ TestCase for Litmus 15065 """
        discovery_pane = DiscoveryPane(mozwebqa, self.basepath)
        expected_text = "Thanks for using Firefox and supporting Mozilla's mission!"

        mission_text = discovery_pane.mission_section
        Assert.true(expected_text in mission_text)
        Assert.true(discovery_pane.mozilla_org_link_visible())
        download_count_regex = "Add-ons downloaded: (.+)"
        Assert.true(re.search(download_count_regex, discovery_pane.download_count) != None)

    @nondestructive
    def test_that_featured_personas_is_present_and_has_5_item(self, mozwebqa):
        """ TestCase for Litmus 15079, 15080 """
        discovery_pane = DiscoveryPane(mozwebqa, self.basepath)
        Assert.true(discovery_pane.is_personas_section_visible)
        Assert.equal(5, discovery_pane.personas_count)
        Assert.true(discovery_pane.is_personas_see_all_link_visible)

    @nondestructive
    def test_that_featured_personas_go_to_their_landing_page_when_clicked(self, mozwebqa):
        """ TestCase for Litmus 15081 """
        discovery_pane = DiscoveryPane(mozwebqa, self.basepath)
        first_persona = discovery_pane.first_persona
        persona = discovery_pane.click_on_first_persona()
        Assert.equal(first_persona, persona.persona_title)

    @nondestructive
    def test_that_More_Ways_To_Customize_section_is_available(self, mozwebqa):
        " TestCase for Litmus 15082 """
        discovery_pane = DiscoveryPane(mozwebqa, self.basepath)
        Assert.true(discovery_pane.more_ways_section_visible)
        Assert.equal("Browse all add-ons", discovery_pane.more_ways_addons)
        Assert.equal("See all themes and Personas", discovery_pane.more_ways_personas)

    @nondestructive
    def test_that_up_and_coming_is_present_and_had_5_items(self, mozwebqa):
        """ TestCase for Litmus 15074 """
        discovery_pane = DiscoveryPane(mozwebqa, self.basepath)
        Assert.equal(5, discovery_pane.up_and_coming_item_count)

    @nondestructive
    def test_the_logout_link_for_logged_in_users(self, mozwebqa):
        """
        Litmus 15110
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

    def test_that_carousel_works(self, mozwebqa):
        """
        Litmus 15071
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

    def test_that_extension_is_underlined_while_hover_and_text_not(self, mozwebqa):
        """
        Litmus 15118
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=15118
        """
        discovery_pane = DiscoveryPane(mozwebqa, self.basepath)

        Assert.equal(discovery_pane.hover_over_extension_and_get_css_property_for_title, "underline")
        Assert.equal(discovery_pane.hover_over_extension_and_get_css_property_for_text, "none")

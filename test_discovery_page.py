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
xfail = pytest.mark.xfail

from unittestzero import Assert

from discovery_page import DiscoveryPane
#from homepage import HomePage


class TestDiscoveryPane:
    """ This only works with Firefox 4 """

    #Need to get this info before run
    basepath = '/en-US/firefox/discovery/pane/4.0/Darwin'

    def test_that_users_with_less_than_3_addons_get_what_are_addons(self, mozwebqa):
        """ Test case for litmus 15063 -
        Since Selenium starts with a clean profile all the time this will always have
        less than 3 addons
        """
        discovery_pane = DiscoveryPane(mozwebqa, self.basepath)
        what_are_addons_expected = "Add-ons are applications that let you personalize "
        what_are_addons_expected += "Firefox with extra functionality or style. Try a time-saving"
        what_are_addons_expected += " sidebar, a weather notifier, or a themed look to make "
        what_are_addons_expected += "Firefox your own. Learn More"

        Assert.equal(what_are_addons_expected, discovery_pane.what_are_addons_text)

    def test_that_mission_statement_is_on_addons_home_page(self, mozwebqa):
        """ TestCase for Litmus 15065 """
        discovery_pane = DiscoveryPane(mozwebqa, self.basepath)
        discovery_pane.wait_for_mission_visible
        Assert.true(discovery_pane.is_mission_section_visible)
        expected_text = "Thanks for using Firefox and supporting Mozilla's mission!"

        mission_text = discovery_pane.mission_section
        Assert.true(expected_text in mission_text)
        Assert.true(discovery_pane.mozilla_org_link_visible())
        download_count_regex = "Add-ons downloaded: (.+)"
        Assert.true(re.search(download_count_regex, discovery_pane.download_count) != None)

    def test_that_featured_personas_is_present_and_has_5_item(self, mozwebqa):
        """ TestCase for Litmus 15079, 15080 """
        discovery_pane = DiscoveryPane(mozwebqa, self.basepath)
        Assert.true(discovery_pane.is_personas_section_visible)
        Assert.equal(5, discovery_pane.personas_count)
        Assert.true(discovery_pane.is_personas_see_all_link_visible)

    @xfail(reason="Disabled until bug 674374 is fixed.")
    def test_that_featured_personas_go_to_their_landing_page_when_clicked(self, mozwebqa):
        """ TestCase for Litmus 15081 """
        discovery_pane = DiscoveryPane(mozwebqa, self.basepath)
        first_persona = discovery_pane.first_persona
        first_persona_url = first_persona.lower().replace(" ", "-")
        persona = discovery_pane.click_on_first_persona()
        Assert.true(first_persona_url in discovery_pane.get_url_current_page())
        Assert.equal(first_persona, persona.persona_title)

    def test_that_More_Ways_To_Customize_section_is_available(self, mozwebqa):
        " TestCase for Litmus 15082 """
        discovery_pane = DiscoveryPane(mozwebqa, self.basepath)
        Assert.true(discovery_pane.more_ways_section_visible)
        Assert.equal("Browse all add-ons", discovery_pane.more_ways_addons)
        Assert.equal("See all themes and Personas", discovery_pane.more_ways_personas)

    def test_that_up_and_coming_is_present_and_had_5_items(self, mozwebqa):
        """ TestCase for Litmus 15074 """
        discovery_pane = DiscoveryPane(mozwebqa, self.basepath)
        Assert.true(discovery_pane.up_and_coming_visible)
        Assert.equal(5, discovery_pane.up_and_coming_item_count)

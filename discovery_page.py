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
#                 Marc George
#                 Dave Hunt <dhunt@mozilla.com>
#                 Alex Rodionov <p0deje@gmail.com>
#                 Joel Andersson <janderssn@gmail.com>
#                 Bebe <florin.strugariu@softvision.ro>
#                 Marlena Compton <mcompton@mozilla.com>
#                 Teodosia Pop <teodosia.pop@softvision.ro>
#                 Alex Lakatos <alex@greensqr.com>
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

from page import Page
from base_page import BasePage


class DiscoveryPane(BasePage):

    _what_are_addons_section_locator = 'id=intro'
    _what_are_addons_text_locator = 'css=#intro p'
    _mission_section_locator = 'id=mission'
    _mission_section_text_locator = 'css=#mission > p'
    _learn_more_locator = 'id=learn-more'
    _mozilla_org_link_locator = "css=#mission a"
    _download_count_text_locator = "id=download-count"
    _personas_section_locator = "id=featured-personas"
    _personas_see_all_link = "css=.all[href='/en-US/firefox/personas/']"
    _personas_locator = "//span[@class='addon-title']/b"
    _more_ways_section_locator = "id=more-ways"
    _more_ways_addons_locator = "id=more-addons"
    _more_ways_personas_locator = "id=more-personas"
    _up_and_coming_section = "id=up-and-coming"
    _up_and_coming_item = "//section[@id='up-and-coming']/ul/li/a[@class='addon-title']"

    def __init__(self, testsetup, path):
        BasePage.__init__(self, testsetup)
        self.selenium.open("%s/%s" % (self.site_version, path))
        #resizing this page for elements that disappear when the window is < 1000
        self.selenium.get_eval("window.resizeTo(10000,10000); window.moveTo(0,0)")

    @property
    def what_are_addons_text(self):
        return self.selenium.get_text(self._what_are_addons_text_locator)

    def click_learn_more(self):
        self.selenium.click(self._learn_more_locator)
        self.selenium.wait_for_page_to_load(self.timeout)

    @property
    def is_mission_section_visible(self):
        return self.selenium.is_visible(self._mission_section_locator)

    def wait_for_mission_visible(self):
            self.wait_for_element_visible(self._mission_section_locator)

    @property
    def mission_section(self):
        return self.selenium.get_text(self._mission_section_text_locator)

    def mozilla_org_link_visible(self):
        return self.selenium.is_visible(self._mozilla_org_link_locator)

    @property
    def download_count(self):
        self.wait_for_element_visible(self._download_count_text_locator)
        return self.selenium.get_text(self._download_count_text_locator)

    @property
    def is_personas_section_visible(self):
        return self.selenium.is_visible(self._personas_section_locator)

    @property
    def personas_count(self):
        return int(self.selenium.get_xpath_count(self._personas_locator))

    @property
    def is_personas_see_all_link_visible(self):
        return self.selenium.is_visible(self._personas_see_all_link)

    @property
    def first_persona(self):
        return self.selenium.get_text(self._personas_locator)

    def click_on_first_persona(self):
        self.selenium.click(self._personas_locator)
        self.selenium.wait_for_page_to_load(self.timeout)
        return DiscoveryPersonasDetailPage(self.testsetup)

    @property
    def more_ways_section_visible(self):
        return self.selenium.is_visible(self._more_ways_section_locator)

    @property
    def more_ways_addons(self):
        return self.selenium.get_text(self._more_ways_addons_locator)

    @property
    def more_ways_personas(self):
        return self.selenium.get_text(self._more_ways_personas_locator)

    @property
    def up_and_coming_visible(self):
        return self.selenium.is_visible(self._up_and_coming_section)

    @property
    def up_and_coming_item_count(self):
        return int(self.selenium.get_xpath_count(self._up_and_coming_item))


class DiscoveryPersonasDetailPage(BasePage):

    _persona_title = 'css=h1.addon'

    @property
    def persona_title(self):
        return self.selenium.get_text(self._persona_title)

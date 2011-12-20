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

from selenium.webdriver.common.by import By

from pages.base import Base


class DiscoveryPane(Base):

    _what_are_addons_text_locator = (By.CSS_SELECTOR, '#intro p')
    _mission_section_text_locator = (By.CSS_SELECTOR, '#mission > p')
    _learn_more_locator = (By.ID, 'learn-more')
    _mozilla_org_link_locator = (By.CSS_SELECTOR, "#mission a")
    _download_count_text_locator = (By.ID, "download-count")
    _personas_section_locator = (By.ID, "featured-personas")
    _personas_see_all_link = (By.CSS_SELECTOR, ".all[href='/en-US/firefox/personas/']")
    _personas_locator = (By.XPATH, "//span[@class='addon-title']/b")
    _more_ways_section_locator = (By.ID, "more-ways")
    _more_ways_addons_locator = (By.ID, "more-addons")
    _more_ways_personas_locator = (By.ID, "more-personas")
    _up_and_coming_item = (By.XPATH, "//section[@id='up-and-coming']/ul/li/a[@class='addon-title']")
    _logout_link_locator = (By.CSS_SELECTOR, "#logout > a")

    def __init__(self, testsetup, path):
        Base.__init__(self, testsetup)
        self.selenium.get("%s/%s" % (self.api_base_url, path))
        #resizing this page for elements that disappear when the window is < 1000
        #self.selenium.set_window_size(1000, 1000) Commented because this selenium call is still in beta

    @property
    def what_are_addons_text(self):
        return self.selenium.find_element(*self._what_are_addons_text_locator).text

    def click_learn_more(self):
        self.selenium.find_element(*self._learn_more_locator).click()

    @property
    def mission_section(self):
        return self.selenium.find_element(*self._mission_section_text_locator).text

    def mozilla_org_link_visible(self):
        return self.is_element_visible(*self._mozilla_org_link_locator)

    @property
    def download_count(self):
        return self.selenium.find_element(*self._download_count_text_locator).text

    @property
    def is_personas_section_visible(self):
        return self.is_element_visible(*self._personas_section_locator)

    @property
    def personas_count(self):
        return len(self.selenium.find_elements(*self._personas_locator))

    @property
    def is_personas_see_all_link_visible(self):
        return self.is_element_visible(*self._personas_see_all_link)

    @property
    def first_persona(self):
        return self.selenium.find_elements(*self._personas_locator)[0].text

    def click_on_first_persona(self):
        self.selenium.find_elements(*self._personas_locator)[0].click()
        return DiscoveryPersonasDetail(self.testsetup)

    @property
    def more_ways_section_visible(self):
        return self.is_element_visible(*self._more_ways_section_locator)

    @property
    def more_ways_addons(self):
        return self.selenium.find_element(*self._more_ways_addons_locator).text

    @property
    def more_ways_personas(self):
        return self.selenium.find_element(*self._more_ways_personas_locator).text

    @property
    def up_and_coming_item_count(self):
        return len(self.selenium.find_elements(*self._up_and_coming_item))

    def click_logout(self):
        self.selenium.find_element(*self._logout_link_locator).click()
        from pages.home import Home
        return Home(self.testsetup, open_url=False)


class DiscoveryPersonasDetail(Base):

    _persona_title = (By.CSS_SELECTOR, 'h1.addon')

    @property
    def persona_title(self):
        return self.selenium.find_element(*self._persona_title).text

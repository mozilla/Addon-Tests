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
# Contributor(s): Bebe <florin.strugariu@softvision.ro>
#                 David Burns
#                 Marc George
#                 Dave Hunt <dhunt@mozilla.com>
#                 Alex Rodionov <p0deje@gmail.com>
#                 Joel Andersson <janderssn@gmail.com>
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

import re
from unittestzero import Assert

from selenium.webdriver.common.by import By

from pages.base import Base


class Personas(Base):

    _page_title = "Personas :: Add-ons for Firefox"
    _personas_locator = (By.CSS_SELECTOR, 'div.persona.persona-small a')
    _start_exploring_locator = (By.CSS_SELECTOR, "#featured-addons.personas-home a.more-info")
    _featured_addons_locator = (By.CSS_SELECTOR, "#featured-addons.personas-home")

    _featured_personas_locator = (By.CSS_SELECTOR, ".personas-featured .persona.persona-small")
    _recently_added_locator = (By.XPATH, "//div[@class='addons-column'][1]//div[@class='persona persona-small']")
    _most_popular_locator = (By.XPATH, "//div[@class='addons-column'][2]//div[@class='persona persona-small']")
    _top_rated_locator = (By.XPATH, "//div[@class='addons-column'][3]//div[@class='persona persona-small']")

    _persona_header_locator = (By.CSS_SELECTOR, ".featured-inner > h2")

    @property
    def persona_count(self):
        """ Returns the total number of persona links in the page. """
        return len(self.selenium.find_elements(*self._personas_locator))

    def click_persona(self, index):
        """ Clicks on the persona with the given index in the page. """
        self.selenium.find_elements(*self._personas_locator)[index].click()
        return PersonasDetail(self.testsetup)

    def open_persona_detail_page(self, persona_key):
        self.selenium.get(self.base_url + "/addon/%s" % persona_key)
        return PersonasDetail(self.testsetup)

    def click_start_exploring(self):
        self.selenium.find_element(*self._start_exploring_locator).click()
        return PersonasBrowse(self.testsetup)

    @property
    def is_featured_addons_present(self):
        return len(self.selenium.find_elements(*self._featured_addons_locator)) > 0

    @property
    def featured_personas_count(self):
        return len(self.selenium.find_elements(*self._featured_personas_locator))

    @property
    def recently_added_count(self):
        return len(self.selenium.find_elements(*self._recently_added_locator))

    @property
    def recently_added_dates(self):
        iso_dates = self._extract_iso_dates("Added %B %d, %Y", *self._recently_added_locator)
        return iso_dates

    @property
    def most_popular_count(self):
        return len(self.selenium.find_elements(*self._most_popular_locator))

    @property
    def most_popular_downloads(self):
        pattern = "(\d+(?:[,]\d+)*)\s+users"
        return self._extract_integers(pattern, *self._most_popular_locator)

    @property
    def top_rated_count(self):
        return len(self.selenium.find_elements(*self._top_rated_locator))

    @property
    def top_rated_ratings(self):
        pattern = "Rated\s+(\d)\s+.*"
        return self._extract_integers(pattern, *self._top_rated_locator)

    @property
    def persona_header(self):
        return self.selenium.find_element(*self._persona_header_locator).text


class PersonasDetail(Base):

    _page_title_regex = '.+ :: Add-ons for Firefox'

    _personas_title_locator = (By.CSS_SELECTOR, 'h2.addon')

    @property
    def is_the_current_page(self):
        # This overrides the method in the Page super class.
        Assert.not_none(re.match(self._page_title_regex, self.selenium.title), 'Expected the current page to be the personas detail page.')
        return True

    @property
    def title(self):
        return self.selenium.find_element(*self._personas_title_locator).text


class PersonasBrowse(Base):

    _selected_sort_by_locator = (By.CSS_SELECTOR, '#addon-list-options li.selected a')
    _personas_grid_locator = (By.CSS_SELECTOR, '.featured.listing ul.personas-grid')

    @property
    def is_the_current_page(self):
        # This overrides the method in the Page super class.
        Assert.true(self.is_element_present(*self._personas_grid_locator),
            'Expected the current page to be the personas browse page.')
        return True

    @property
    def sort_key(self):
        """ Returns the current value of the sort request parameter. """
        url = self.selenium.current_url
        return re.search("[/][?]sort=(.+)[&]?", url).group(1)

    @property
    def sort_by(self):
        """ Returns the label of the currently selected sort option. """
        return self.selenium.find_element(*self._selected_sort_by_locator).text

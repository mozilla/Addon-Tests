#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re
from unittestzero import Assert

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.desktop.base import Base


class Personas(Base):

    _page_title = "Personas :: Add-ons for Firefox"
    _personas_locator = (By.CSS_SELECTOR, 'div.persona.persona-small a')
    _start_exploring_locator = (By.CSS_SELECTOR, "#featured-addons.personas-home a.more-info")
    _featured_addons_locator = (By.CSS_SELECTOR, "#featured-addons.personas-home")

    _featured_personas_locator = (By.CSS_SELECTOR, ".personas-featured .persona.persona-small")
    _recently_added_locator = (By.CSS_SELECTOR, "#personas-created .persona-small")
    _most_popular_locator = (By.CSS_SELECTOR, "#personas-popular .persona-small")
    _top_rated_locator = (By.CSS_SELECTOR, "#personas-rating .persona-small")

    _persona_header_locator = (By.CSS_SELECTOR, ".featured-inner > h2")

    @property
    def persona_count(self):
        """Returns the total number of persona links in the page."""
        return len(self.selenium.find_elements(*self._personas_locator))

    def click_persona(self, index):
        """Clicks on the persona with the given index in the page."""
        self.selenium.find_elements(*self._personas_locator)[index].click()
        persona_detail = PersonasDetail(self.testsetup)
        WebDriverWait(self.selenium, 10).until(lambda s: persona_detail.is_title_visible)
        return persona_detail

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
        actual_page_title = self.selenium.title
        Assert.not_none(re.match(self._page_title_regex, actual_page_title), 'Expected the current page to be the personas detail page.\n Actual title: %s' % actual_page_title)
        return True

    @property
    def is_title_visible(self):
        return self.is_element_visible(*self._personas_title_locator)

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
        """Returns the current value of the sort request parameter."""
        url = self.selenium.current_url
        return re.search("[/][?]sort=(.+)[&]?", url).group(1)

    @property
    def sort_by(self):
        """Returns the label of the currently selected sort option."""
        return self.selenium.find_element(*self._selected_sort_by_locator).text

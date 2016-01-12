# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re

from selenium.webdriver.common.by import By

from pages.page import PageRegion
from pages.desktop.base import Base
from pages.desktop.search import SearchResultList


class Themes(Base):

    _url = '{base_url}/{locale}/firefox/themes/'

    _page_title = "Themes :: Add-ons for Firefox"
    _start_exploring_locator = (By.CSS_SELECTOR, "#featured-addons.personas-home a.more-info")
    _featured_addons_locator = (By.CSS_SELECTOR, "#featured-addons.personas-home")

    _featured_themes_locator = (By.CSS_SELECTOR, '.personas-featured .persona-preview')
    _recently_added_locator = (By.CSS_SELECTOR, "#personas-created .persona-small")
    _most_popular_locator = (By.CSS_SELECTOR, "#personas-popular .persona-small")
    _top_rated_locator = (By.CSS_SELECTOR, "#personas-rating .persona-small")

    _theme_header_locator = (By.CSS_SELECTOR, ".featured-inner > h2")

    @property
    def featured_themes(self):
        return [self.ThemePreview(self.base_url, self.selenium, root=el) for
                el in self.selenium.find_elements(*self._featured_themes_locator)]

    def open_theme_detail_page(self, theme_key):
        self.selenium.get(self.base_url + "/addon/%s" % theme_key)
        return ThemesDetail(self.base_url, self.selenium)

    def click_start_exploring(self):
        self.selenium.find_element(*self._start_exploring_locator).click()
        return ThemesBrowse(self.base_url, self.selenium)

    @property
    def is_featured_addons_present(self):
        return len(self.selenium.find_elements(*self._featured_addons_locator)) > 0

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
    def theme_header(self):
        return self.selenium.find_element(*self._theme_header_locator).text

    class ThemePreview(PageRegion):

        _link_locator = (By.TAG_NAME, 'a')

        def click(self):
            self.root.find_element(*self._link_locator).click()
            return ThemesDetail(self.base_url, self.selenium)


class ThemesDetail(Base):

    _page_title_regex = '.+ :: Add-ons for Firefox'

    _themes_title_locator = (By.CSS_SELECTOR, 'h2.addon > span')
    _breadcrumb_locator = (By.ID, "breadcrumbs")

    @property
    def is_the_current_page(self):
        # This overrides the method in the Page super class.
        actual_page_title = self.page_title
        assert re.match(self._page_title_regex, actual_page_title) is not None, 'Expected the current page to be the themes detail page.\n Actual title: %s' % actual_page_title
        return True

    @property
    def is_title_visible(self):
        return self.is_element_visible(*self._themes_title_locator)

    @property
    def title(self):
        return self.selenium.find_element(*self._themes_title_locator).text

    @property
    def breadcrumb(self):
        return self.selenium.find_element(*self._breadcrumb_locator).text


class ThemesBrowse(Base):

    _selected_sort_by_locator = (By.CSS_SELECTOR, '#addon-list-options li.selected a')
    _themes_grid_locator = (By.CSS_SELECTOR, '.featured.listing ul.personas-grid')

    @property
    def is_the_current_page(self):
        # This overrides the method in the Page super class.
        assert self.is_element_present(*self._themes_grid_locator), 'Expected the current page to be the themes browse page.'
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


class ThemesSearchResultList(SearchResultList):
    _results_locator = (By.CSS_SELECTOR, 'ul.personas-grid div.persona-small')

    class ThemesSearchResultItem(SearchResultList.SearchResultItem):
        _name_locator = (By.CSS_SELECTOR, 'h6 > a')

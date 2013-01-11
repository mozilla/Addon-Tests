#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from pages.desktop.regions.sorter import Sorter
from pages.desktop.base import Base
from pages.page import Page
from pages.desktop.search import SearchResultList


class FullThemes(Base):

    _addons_root_locator = (By.CSS_SELECTOR, '.listing-grid > li')
    _addon_name_locator = (By.CSS_SELECTOR, 'h3')
    _addons_metadata_locator = (By.CSS_SELECTOR, '.vital .updated')
    _addons_download_locator = (By.CSS_SELECTOR, '.downloads.adu')
    _addons_rating_locator = (By.CSS_SELECTOR, 'span span')
    _category_locator = (By.CSS_SELECTOR, '#c-30 > a')
    _categories_locator = (By.CSS_SELECTOR, '#side-categories li')
    _category_link_locator = (By.CSS_SELECTOR, _categories_locator[1] + ':nth-of-type(%s) a')
    _next_link_locator = (By.CSS_SELECTOR, '.paginator .rel > a:nth-child(3)')
    _previous_link_locator = (By.CSS_SELECTOR, '.paginator .rel > a:nth-child(2)')
    _last_page_link_locator = (By.CSS_SELECTOR, '.rel > a:nth-child(4)')
    _explore_filter_links_locators = (By.CSS_SELECTOR, '#side-explore a')

    @property
    def _addons_root_element(self):
        return self.selenium.find_element(*self._addons_root_locator)

    def click_sort_by(self, type):
        Sorter(self.testsetup).sort_by(type)

    @property
    def sorted_by(self):
        return Sorter(self.testsetup).sorted_by

    @property
    def selected_explore_filter(self):
        for link in self.selenium.find_elements(*self._explore_filter_links_locators):
            selected = link.value_of_css_property('font-weight')
            if selected == 'bold' or int(selected) > 400:
                return link.text

    def click_on_first_addon(self):
        self._addons_root_element.find_element(*self._addon_name_locator).click()
        return FullTheme(self.testsetup)

    def click_on_first_category(self):
        self.selenium.find_element(*self._category_locator).click()
        return FullThemesCategory(self.testsetup)

    def get_category(self, lookup):
        return self.selenium.find_element(self._category_link_locator[0],
                                          self._category_link_locator[1] % lookup).text

    @property
    def full_themes_category(self):
        return self.selenium.find_element(*self._category_locator).text

    @property
    def categories_count(self):
        return len(self.selenium.find_elements(*self._categories_locator))

    @property
    def get_all_categories(self):
        return [element.text for element in self.selenium.find_elements(*self._categories_locator)]

    @property
    def addon_names(self):
        addon_name = []
        for addon in self._addons_root_element.find_elements(*self._addon_name_locator):
            ActionChains(self.selenium).move_to_element(addon).perform()
            addon_name.append(addon.text)
        return addon_name

    def addon_name(self, lookup):
        return self.selenium.find_element(By.CSS_SELECTOR,
                                          "%s:nth-of-type(%s) h3" % (self._addons_root_locator[1], lookup)).text

    @property
    def addon_count(self):
        return len(self._addons_root_element.find_elements(*self._addon_name_locator))

    @property
    def addon_updated_dates(self):
        return self._extract_iso_dates("Updated %B %d, %Y", *self._addons_metadata_locator)

    @property
    def addon_created_dates(self):
        return self._extract_iso_dates("Added %B %d, %Y", *self._addons_metadata_locator)

    @property
    def addon_download_number(self):
        pattern = "(\d+(?:[,]\d+)*) weekly downloads"
        downloads = self._extract_integers(pattern, *self._addons_download_locator)
        return downloads

    @property
    def addon_rating(self):
        pattern = "(\d)"
        ratings = self._extract_integers(pattern, *self._addons_rating_locator)
        return ratings

    @property
    def full_themes(self):
        return [self.FullTheme(self.testsetup, fulltheme)for fulltheme in self.selenium.find_elements(*self._addons_root_locator)]

    @property
    def paginator(self):
        from pages.desktop.regions.paginator import Paginator
        return Paginator(self.testsetup)

    class FullTheme(Page):

        _is_incompatible_locator = (By.CSS_SELECTOR, "div.hovercard > span.notavail")
        _not_available_locator = (By.CSS_SELECTOR, "div.hovercard.incompatible > div.more > div.install-shell > div.extra > span.notavail")
        _hovercard_locator = (By.CSS_SELECTOR, "div.hovercard")
        _more_flyout_locator = (By.CSS_SELECTOR, 'div.more')

        def __init__(self, testsetup, element):
            Page.__init__(self, testsetup)
            self._root_element = element

        def _move_to_full_theme_flyout(self):
            # Due to the grid like movement of the mouse and overlapping of hover cards
            # sometimes the wrong hovercard can stick open. First we move the mouse to
            # a location below the hover then move up to ensure we hover on the correct one
            ActionChains(self.selenium).\
                move_to_element_with_offset(self._root_element, 200, 10).\
                move_to_element(self._root_element).\
                perform()

        @property
        def is_flyout_visible(self):
            return self._root_element.find_element(*self._more_flyout_locator).is_displayed()

        @property
        def is_incompatible(self):
            return 'incompatible' in self._root_element.find_element(*self._hovercard_locator).get_attribute('class')

        @property
        def not_available_flag_text(self):
            # This refers to the red 'not available for Firefox x' text inside the flyout
            # We need to move the mouse to expose the flyout so we can see the text
            self._move_to_full_theme_flyout()
            if not self.is_flyout_visible:
                raise Exception('Flyout did not expand, possible mouse focus/ActionChain issue')
            return self._root_element.find_element(*self._not_available_locator).text

        @property
        def is_incompatible_flag_visible(self):
            # This refers to the grey 'This full theme is incompatible' text on the panel

            from selenium.common.exceptions import NoSuchElementException
            self.selenium.implicitly_wait(0)
            try:
                return self._root_element.find_element(*self._is_incompatible_locator).is_displayed()
            except NoSuchElementException:
                return False
            finally:
                # set back to where you once belonged
                self.selenium.implicitly_wait(self.testsetup.default_implicit_wait)


class FullTheme(Base):

    _addon_title = (By.CSS_SELECTOR, "h1.addon")
    _install_button = (By.CSS_SELECTOR, "p.install-button > a")
    _breadcrumb_locator = (By.ID, "breadcrumbs")

    @property
    def addon_title(self):
        return self.selenium.find_element(*self._addon_title).text

    @property
    def install_button_exists(self):
        return self.is_element_visible(*self._install_button)

    @property
    def breadcrumb(self):
        return self.selenium.find_element(*self._breadcrumb_locator).text


class FullThemesCategory(Base):

    _title_locator = (By.CSS_SELECTOR, "section.primary > h1")
    _breadcrumb_locator = (By.CSS_SELECTOR, "#breadcrumbs > ol")

    @property
    def title(self):
        return self.selenium.find_element(*self._title_locator).text


class FullThemesSearchResultList(SearchResultList):
    _results_locator = (By.CSS_SELECTOR, '.items .item')

    class FullThemesSearchResultItem(SearchResultList.SearchResultItem):
        _name_locator = (By.CSS_SELECTOR, 'h3 > a')

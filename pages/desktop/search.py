#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from time import strptime, mktime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

from pages.page import Page
from pages.desktop.base import Base
from pages.desktop.regions.search_filter import FilterBase


class SearchHome(Base):

    _number_of_results_found = (By.CSS_SELECTOR, "#search-facets > p")

    _no_results_locator = (By.CSS_SELECTOR, "p.no-results")
    _search_results_title_locator = (By.CSS_SELECTOR, "section.primary>h1")
    _results_locator = (By.CSS_SELECTOR, "div.items div.item.addon")

    _sort_by_relevance_locator = (By.LINK_TEXT, 'Relevance')
    _sort_by_most_users_locator = (By.LINK_TEXT, 'Most Users')
    _sort_by_top_rated_locator = (By.LINK_TEXT, 'Top Rated')
    _sort_by_newest_locator = (By.LINK_TEXT, 'Newest')

    _sort_by_name_locator = (By.XPATH, "//div[@id='sorter']//li/a[normalize-space(text())='Name']")
    _sort_by_weekly_downloads_locator = (By.XPATH, "//div[@id='sorter']//li/a[normalize-space(text())='Weekly Downloads']")
    _sort_by_recently_updated_locator = (By.XPATH, "//div[@id='sorter']//li/a[normalize-space(text())='Recently Updated']")
    _sort_by_up_and_coming_locator = (By.XPATH, "//div[@id='sorter']//li/a[normalize-space(text())='Up & Coming']")

    _hover_more_locator = (By.CSS_SELECTOR, "li.extras > a")

    _updating_locator = (By.CSS_SELECTOR, "div.updating")

    def wait_for_results_refresh(self):
        WebDriverWait(self.selenium, 10).until(lambda s: not self.is_element_present(*self._updating_locator))

    @property
    def is_no_results_present(self):
        return self.is_element_present(*self._no_results_locator)

    @property
    def no_results_text(self):
        return self.selenium.find_element(*self._no_results_locator).text

    @property
    def number_of_results_text(self):
        return self.selenium.find_element(*self._number_of_results_found).text

    @property
    def search_results_title(self):
        return self.selenium.find_element(*self._search_results_title_locator).text

    @property
    def filter(self):
        return FilterBase(self.testsetup)

    @property
    def result_count(self):
        return len(self.selenium.find_elements(*self._results_locator))

    def sort_by(self, type):
        hover_element = self.selenium.find_element(*self._hover_more_locator)
        click_element = self.selenium.find_element(*getattr(self, '_sort_by_%s_locator' % type.replace(' ', '_').lower()))
        ActionChains(self.selenium).move_to_element(hover_element).\
            move_to_element(click_element).\
            click().perform()
        self.wait_for_results_refresh()
        return SearchHome(self.testsetup)

    def result(self, lookup):
        elements = self.selenium.find_elements(*self._results_locator)
        return self.SearchResult(self.testsetup, elements[lookup])

    @property
    def results(self):
        return [self.SearchResult(self.testsetup, web_element)
                for web_element in self.selenium.find_elements(*self._results_locator)]

    class SearchResult(Page):
        _name_locator = (By.CSS_SELECTOR, 'div.info > h3 > a')
        _created_date = (By.CSS_SELECTOR, 'div.info > div.vitals > div.updated')
        _sort_criteria = (By.CSS_SELECTOR, 'div.info > div.vitals > div.adu')

        def __init__(self, testsetup, element):
            Page.__init__(self, testsetup)
            self._root_element = element

        @property
        def name(self):
            return self._root_element.find_element(*self._name_locator).text

        @property
        def text(self):
            return self._root_element.text

        @property
        def downloads(self):
            number = self._root_element.find_element(*self._sort_criteria).text
            return int(number.split()[0].replace(',', ''))

        @property
        def users(self):
            number = self._root_element.find_element(*self._sort_criteria).text
            return int(number.split()[0].replace(',', ''))

        @property
        def created_date(self):
            """Returns created date of result in POSIX format."""
            date = self._root_element.find_element(*self._created_date).text.strip().replace('Added ', '')
            # convert to POSIX format
            date = strptime(date, '%B %d, %Y')
            return mktime(date)

        @property
        def updated_date(self):
            """Returns updated date of result in POSIX format."""
            date = self._root_element.find_element(*self._created_date).text.replace('Updated ', '')
            # convert to POSIX format
            date = strptime(date, '%B %d, %Y')
            return mktime(date)

        def click_result(self):
            self._root_element.find_element(*self._name_locator).click()
            from pages.desktop.details import Details
            return Details(self.testsetup)

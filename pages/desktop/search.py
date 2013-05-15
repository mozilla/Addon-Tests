#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from time import strptime, mktime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.page import Page
from pages.desktop.base import Base


class SearchResultList(Base):

    _number_of_results_found = (By.CSS_SELECTOR, "#search-facets > p")

    _no_results_locator = (By.CSS_SELECTOR, "p.no-results")
    _search_results_title_locator = (By.CSS_SELECTOR, "section.primary > h1")
    _results_locator = (By.CSS_SELECTOR, "div.items div.item.addon")

    def __init__(self, testsetup):
        Base.__init__(self, testsetup)
        try:  # the result could legitimately be zero, but give it time to make sure
            WebDriverWait(self.selenium, self.timeout).until(
                lambda s: len(s.find_elements(*self._results_locator)) > 0
            )
        except Exception:
            pass

    @property
    def is_no_results_present(self):
        return self.is_element_present(*self._no_results_locator)

    @property
    def number_of_results_text(self):
        return self.selenium.find_element(*self._number_of_results_found).text

    @property
    def search_results_title(self):
        return self.selenium.find_element(*self._search_results_title_locator).text

    @property
    def filter(self):
        from pages.desktop.regions.search_filter import FilterBase
        return FilterBase(self.testsetup)

    @property
    def result_count(self):
        return len(self.selenium.find_elements(*self._results_locator))

    def click_sort_by(self, type):
        from pages.desktop.regions.sorter import Sorter
        Sorter(self.testsetup).sort_by(type)

    def result(self, lookup):
        elements = self.selenium.find_elements(*self._results_locator)
        from pages.desktop.collections import Collections, CollectionSearchResultList
        from pages.desktop.themes import ThemesSearchResultList, Themes
        from pages.desktop.complete_themes import CompleteThemes, CompleteThemesSearchResultList
        if isinstance(self, (Collections, CollectionSearchResultList)):
            return self.CollectionsSearchResultItem(self.testsetup, elements[lookup])
        elif isinstance(self, (Themes, ThemesSearchResultList)):
            return self.ThemesSearchResultItem(self.testsetup, elements[lookup])
        elif isinstance(self, (CompleteThemes, CompleteThemesSearchResultList)):
            return self.CompleteThemesSearchResultItem(self.testsetup, elements[lookup])
        else:
            return self.SearchResultItem(self.testsetup, elements[lookup])

    @property
    def results(self):
        elements = self.selenium.find_elements(*self._results_locator)
        return [self.SearchResultItem(self.testsetup, web_element)
                for web_element in elements
                ]

    @property
    def paginator(self):
        from pages.desktop.regions.paginator import Paginator
        return Paginator(self.testsetup)

    class SearchResultItem(Page):
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
            from pages.desktop.collections import Collection, CollectionSearchResultList
            from pages.desktop.themes import ThemesDetail, ThemesSearchResultList
            from pages.desktop.complete_themes import CompleteTheme, CompleteThemesSearchResultList
            from pages.desktop.details import Details
            if isinstance(self, CollectionSearchResultList.CollectionsSearchResultItem):
                return Collection(self.testsetup)
            elif isinstance(self, ThemesSearchResultList.ThemesSearchResultItem):
                return ThemesDetail(self.testsetup)
            elif isinstance(self, CompleteThemesSearchResultList.CompleteThemesSearchResultItem):
                return CompleteTheme(self.testsetup)
            else:
                return Details(self.testsetup)

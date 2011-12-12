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
#                 Alex Rodionov <p0deje@gmail.com>
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


from time import strptime, mktime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

from pages.page import Page
from pages.base import Base
from pages.regions.search_filter import FilterBase


class SearchHome(Base):

    _number_of_results_found = (By.CSS_SELECTOR, "#search-facets > p")

    _no_results_locator = (By.CSS_SELECTOR, "p.no-results")
    _search_results_title_locator = (By.CSS_SELECTOR, "section.primary>h1")
    _results_locator = (By.CSS_SELECTOR, "div.items div.item.addon")

    _sort_by_relevance_locator = (By.CSS_SELECTOR, "div#sorter > ul > li:nth-child(1) > a")
    _sort_by_most_users_locator = (By.CSS_SELECTOR, "div#sorter > ul > li:nth-child(2) > a")
    _sort_by_top_rated_locator = (By.CSS_SELECTOR, "div#sorter > ul > li:nth-child(3) > a")
    _sort_by_newest_locator = (By.CSS_SELECTOR, "div#sorter > ul > li:nth-child(4) > a")

    _sort_by_name_locator = (By.CSS_SELECTOR, "li.extras > ul > li:nth-child(1) > a")
    _sort_by_weekly_downloads_locator = (By.CSS_SELECTOR, "li.extras > ul > li:nth-child(2) > a")
    _sort_by_recently_updated_locator = (By.CSS_SELECTOR, "li.extras > ul > li:nth-child(4) > a")
    _sort_by_up_and_coming_locator = (By.CSS_SELECTOR, "li.extras > ul > li:nth-child(5) > a")

    _hover_more_locator = (By.CSS_SELECTOR, "li.extras > a")

    _next_link_locator = (By.CSS_SELECTOR, ".paginator .rel > a:nth-child(3)")
    _previous_link_locator = (By.CSS_SELECTOR, ".paginator .rel > a:nth-child(2)")
    _updating_locator = (By.CSS_SELECTOR, "div.updating")
    _results_displayed_text_locator = (By.CSS_SELECTOR, ".paginator .pos")

    def _wait_for_results_refresh(self):
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
        self._wait_for_results_refresh()
        return SearchHome(self.testsetup)

    def result(self, lookup):
        elements = self.selenium.find_elements(*self._results_locator)
        return self.SearchResult(self.testsetup, elements[lookup])

    def results(self):
        return [self.SearchResult(self.testsetup, element)
                for element in self.selenium.find_elements(*self._results_locator)]

    def page_forward(self):
        self.selenium.find_element(*self._next_link_locator).click()
        self._wait_for_results_refresh()

    def page_back(self):
        self.selenium.find_element(*self._previous_link_locator).click()
        self._wait_for_results_refresh()

    @property
    def is_next_link_enabled(self):
        button = self.selenium.find_element(*self._next_link_locator).get_attribute('class')
        return not("disabled" in button)

    @property
    def results_displayed(self):
        return self.selenium.find_element(*self._results_displayed_text_locator).text

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
            """ Returns created date of result in POSIX format """
            date = self._root_element.find_element(*self._created_date).text.strip().replace('Added ', '')
            # convert to POSIX format
            date = strptime(date, '%B %d, %Y')
            return mktime(date)

        @property
        def updated_date(self):
            """ Returns updated date of result in POSIX format """
            date = self._root_element.find_element(*self._created_date).text.replace('Updated ', '')
            # convert to POSIX format
            date = strptime(date, '%B %d, %Y')
            return mktime(date)

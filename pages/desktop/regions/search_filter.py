#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.page import Page


class FilterBase(Page):

    _results_count_tag = (By.CSS_SELECTOR, 'p.cnt b')

    def tag(self, lookup):
        return self.Tag(self.testsetup, lookup)

    @property
    def results_count(self):
        return self.selenium.find_element(*self._results_count_tag).text

    class FilterResults(Page):

        _item_link = (By.CSS_SELECTOR, ' a')
        _all_tags_locator = (By.CSS_SELECTOR, 'li#tag-facets h3')

        def __init__(self, testsetup, lookup):
            Page.__init__(self, testsetup)
            # expand the thing here to represent the proper user action
            is_expanded = self.selenium.find_element(*self._all_tags_locator).get_attribute('class')
            if ('active' not in is_expanded):
                self.selenium.find_element(*self._all_tags_locator).click()
            self._root_element = self.selenium.find_element(self._base_locator[0],
                                    "%s[a[contains(@data-params, '%s')]]" % (self._base_locator[1], lookup))

        @property
        def name(self):
            return self._root_element.text

        @property
        def is_selected(self):
            return "selected" in self._root_element.get_attribute('class')

        def click_tag(self):
            self._root_element.find_element(*self._item_link).click()

    class Tag(FilterResults):
        _base_locator = (By.XPATH, ".//*[@id='tag-facets']/ul/li")

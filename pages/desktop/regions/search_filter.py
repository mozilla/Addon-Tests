# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.page import Page


class FilterBase(Page):

    _results_count_tag = (By.CSS_SELECTOR, 'p.cnt b')

    @property
    def category(self):
        return self.Category(self.base_url, self.selenium)

    @property
    def works_with(self):
        return self.WorksWith(self.base_url, self.selenium)

    def tag(self, lookup):
        return self.Tag(self.base_url, self.selenium, lookup)

    @property
    def results_count(self):
        return self.selenium.find_element(*self._results_count_tag).text

    class Category(Page):
        '''
            Filter results by Addon category
        '''

        _category_section_locator = (By.ID, 'category-facets')
        _expand_category_section_locator = (By.CSS_SELECTOR, '#category-facets h3')
        _selected_filter_locator = (By.CSS_SELECTOR, '#category-facets .selected a')
        _complete_themes_filter_locator = (By.CSS_SELECTOR, "#category-facets > ul > li:nth-child(3) > a")

        def expand_filter_options(self):
            self.selenium.find_element(*self._expand_category_section_locator).click()
            self.wait(lambda s: 'active' in s.find_element(*self._category_section_locator).get_attribute('class'))

        def click_filter_complete_themes(self):
            self.selenium.find_element(*self._complete_themes_filter_locator).click()
            self.wait.until(lambda s: s.find_element(*self._complete_themes_filter_locator) == s.find_element(*self._selected_filters_locator))

    class WorksWith(Page):
        '''
            Filter results by version of Firefox and Operating System
        '''

        _works_with_section_locator = (By.ID, 'compat-facets')
        _expand_works_with_section_locator = (By.CSS_SELECTOR, '#compat-facets h3')
        _selected_filters_locator = (By.CSS_SELECTOR, '#compat-facets .selected a')
        _any_firefox_filter_locator = (By.CSS_SELECTOR, '#compat-facets a[data-params*=any]')
        _all_systems_filter_locator = (By.CSS_SELECTOR, '#compat-facets a[data-params*=all]')

        def expand_filter_options(self):
            self.selenium.find_element(*self._expand_works_with_section_locator).click()
            self.wait.until(lambda s: 'active' in s.find_element(*self._works_with_section_locator).get_attribute('class'))

        def click_filter_all_versions_of_firefox(self):
            self.selenium.find_element(*self._any_firefox_filter_locator).click()
            self.wait.until(lambda s: s.find_element(*self._any_firefox_filter_locator) in s.find_elements(*self._selected_filters_locator))

        def click_filter_all_systems(self):
            self.selenium.find_element(*self._all_systems_filter_locator).click()
            self.wait.until(lambda s: s.find_element(*self._all_systems_filter_locator) in s.find_elements(*self._selected_filters_locator))

    class Tag(Page):

        _base_locator = (By.XPATH, ".//*[@id='tag-facets']/ul/li")
        _item_link = (By.CSS_SELECTOR, ' a')
        _all_tags_locator = (By.CSS_SELECTOR, 'li#tag-facets h3')

        def __init__(self, base_url, selenium, lookup):
            Page.__init__(self, base_url, selenium)
            # expand the thing here to represent the proper user action
            is_expanded = self.selenium.find_element(*self._all_tags_locator).get_attribute('class')
            if ('active' not in is_expanded):
                self.selenium.find_element(*self._all_tags_locator).click()
            self._root_element = self.selenium.find_element(self._base_locator[0],
                                                            "%s[a[contains(@data-params, '%s')]]"
                                                            % (self._base_locator[1], lookup))

        @property
        def name(self):
            return self._root_element.text

        @property
        def is_selected(self):
            return "selected" in self._root_element.get_attribute('class')

        def click_tag(self):
            self._root_element.find_element(*self._item_link).click()

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from pages.page import Page


class Sorter(Page):

    _menu_locator = (By.CSS_SELECTOR, '#sort-menu ul')
    _menu_option_locator = (By.CSS_SELECTOR, 'li')

    @property
    def is_extensions_dropdown_visible(self):
        return self.is_element_visible(*self._menu_locator)

    @property
    def options(self):
        return [self.SortOption(self.base_url, self.selenium, element)
                for element in self.selenium.find_element(*self._menu_locator).find_elements(*self._menu_option_locator)]

    class SortOption(Page):

        _name_locator = (By.CSS_SELECTOR, 'a')

        def __init__(self, base_url, selenium, element):
            Page.__init__(self, base_url, selenium)
            self._root_element = element

        @property
        def name(self):
            return self._root_element.find_element(*self._name_locator).text

        @property
        def is_option_visible(self):
            return self._root_element.find_element(*self._name_locator).is_displayed()

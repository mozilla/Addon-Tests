#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from pages.page import Page

class SortExtensions(Page):

    _sort_by_locator = (By.CSS_SELECTOR, '.label > span')
    _dropdown_menu_locator = (By.CSS_SELECTOR, '#sort-menu ul')

    def click_sort_by(self):
        self.selenium.find_element(*self._sort_by_locator).click

    @property
    def is_extensions_dropdown_visible(self):
        return self.selenium.is_visible(*self._dropdown_menu_locator)

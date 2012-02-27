#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.page import Page


class DropdownMenu(Page):

    _name_items_locator = (By.CSS_SELECTOR, 'a')

    def __init__(self, testsetup, element):
        Page.__init__(self, testsetup)
        self._root_element = element

    @property
    def name(self):
        return self._root_element.find_element(*self._name_items_locator).text


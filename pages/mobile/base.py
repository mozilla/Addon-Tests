#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from pages.page import Page


class Base(Page):

    @property
    def footer(self):
        return Base.Footer(self.testsetup)

    @property
    def header(self):
        return Base.HeaderRegion(self.testsetup)

    class Footer(Page):
        _desktop_version_locator = (By.CSS_SELECTOR, 'a.desktop-link')
        _other_language_locator = (By.CSS_SELECTOR, '#language')
        _other_language_text_locator = (By.CSS_SELECTOR, '#lang_form > label')
        _privacy_locator = (By.CSS_SELECTOR, '#footer-links > a:nth-child(1)')
        _legal_locator = (By.CSS_SELECTOR, '#footer-links > a:nth-child(2)')

        def click_desktop_version(self):
            self.selenium.find_element(*self._desktop_version_locator).click()
            from pages.desktop.home import Home
            return Home(self.testsetup)

        @property
        def desktop_version_text(self):
            return self.selenium.find_element(*self._desktop_version_locator).text

        @property
        def other_language_text(self):
            return self.selenium.find_element(*self._other_language_text_locator).text

        @property
        def is_other_language_dropdown_visible(self):
            return self.is_element_visible(*self._other_language_locator)

        @property
        def privacy_text(self):
            return self.selenium.find_element(*self._privacy_locator).text

        @property
        def legal_text(self):
            return self.selenium.find_element(*self._legal_locator).text

    class HeaderRegion(Page):

        _menu_items_locator = (By.CSS_SELECTOR, '.menu-items li')
        _menu_button_locator = (By.CSS_SELECTOR, '.tab > a')

        @property
        def dropdown_menu_items(self):
            from pages.mobile.regions.menu_region import DropdownMenu
            return [DropdownMenu(self.testsetup, element) for element in self.selenium.find_elements(*self._menu_items_locator)]

        def click(self):
            self.selenium.find_element(*self._menu_button_locator).click()

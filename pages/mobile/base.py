# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from pages.page import Page


class Base(Page):

    def scroll_to_element(self, *locator):
        """Scroll to element"""
        el = self.selenium.find_element(*locator)
        self.selenium.execute_script("window.scrollTo(0, %s)" % (el.location['y'] - el.size['height']))

    @property
    def footer(self):
        return Base.Footer(self.base_url, self.selenium)

    @property
    def header(self):
        return Base.HeaderRegion(self.base_url, self.selenium)

    class Footer(Page):
        _desktop_version_locator = (By.CSS_SELECTOR, 'a.desktop-link')
        _other_language_locator = (By.CSS_SELECTOR, '#language')
        _other_language_text_locator = (By.CSS_SELECTOR, '#lang_form > label')
        _privacy_locator = (By.CSS_SELECTOR, '#footer-links > a:nth-child(1)')
        _legal_locator = (By.CSS_SELECTOR, '#footer-links > a:nth-child(2)')

        def click_desktop_version(self):
            self.selenium.find_element(*self._desktop_version_locator).click()
            from pages.desktop.home import Home
            return Home(self.base_url, self.selenium)

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

        _dropdown_menu_locator = (By.CLASS_NAME, 'menu-items')
        _menu_items_locator = (By.CSS_SELECTOR, '.menu-items li')
        _menu_button_locator = (By.CSS_SELECTOR, '.tab > a')

        def click_header_menu(self):
            self.selenium.find_element(*self._menu_button_locator).click()

        @property
        def is_dropdown_menu_visible(self):
            return self.is_element_visible(*self._dropdown_menu_locator)

        @property
        def dropdown_menu_items(self):
            # returns a list containing all the menu items
            return [self.MenuItem(self.base_url, self.selenium, web_element) for web_element in self.selenium.find_elements(*self._menu_items_locator)]

        class MenuItem(Page):

            _name_items_locator = (By.CSS_SELECTOR, 'a')

            def __init__(self, base_url, selenium, element):
                Page.__init__(self, base_url, selenium)
                self._root_element = element

            @property
            def name(self):
                return self._root_element.find_element(*self._name_items_locator).text

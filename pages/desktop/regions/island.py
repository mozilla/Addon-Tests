# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from pages.page import Page


class Island(Page):
    _pager_locator = (By.CSS_SELECTOR, 'nav.pager')
    _title_locator = (By.CSS_SELECTOR, 'h2')
    _see_all_locator = (By.CSS_SELECTOR, 'h2 > a.seeall')
    _sections_locator = (By.CSS_SELECTOR, 'ul > section')
    _item_locator = (By.CSS_SELECTOR, 'li > div')

    def __init__(self, base_url, selenium, element):
        Page.__init__(self, base_url, selenium)
        self._root = element

    @property
    def pager(self):
        try:
            return self.Pager(self.base_url, self.selenium, self._root.find_element(*self._pager_locator))
        except NoSuchElementException:
            raise AssertionError('Paginator is not available')

    @property
    def see_all_text(self):
        return self._root.find_element(*self._see_all_locator).text

    @property
    def see_all_link(self):
        return self._root.find_element(*self._see_all_locator).get_attribute('href')

    def click_see_all(self):
        see_all_url = self.see_all_link
        self._root.find_element(*self._see_all_locator).click()

        if 'extensions' in see_all_url:
            from pages.desktop.extensions import ExtensionsHome
            return ExtensionsHome(self.base_url, self.selenium)
        elif 'personas' in see_all_url:
            from pages.desktop.personas import Personas
            return Personas(self.base_url, self.selenium)
        elif 'collections' in see_all_url:
            from pages.desktop.collections import Collections
            return Collections(self.base_url, self.selenium)

    @property
    def title(self):
        text = self._root.find_element(*self._title_locator).text
        return text.replace(self.see_all_text, '').strip()

    @property
    def visible_section(self):
        for idx, section in enumerate(self._root.find_elements(*self._sections_locator)):
            if section.is_displayed():
                return idx

    @property
    def addons(self):
        return [self.Addon(self.base_url, self.selenium, element)
                for element in self._root.find_elements(*self._sections_locator)[self.pager.selected_dot].find_elements(*self._item_locator)]

    class Addon(Page):
        def __init__(self, base_url, selenium, element):
            Page.__init__(self, base_url, selenium)
            self._root = element

    class Pager(Page):
        _next_locator = (By.CSS_SELECTOR, 'a.next')
        _prev_locator = (By.CSS_SELECTOR, 'a.prev')
        _dot_locator = (By.CSS_SELECTOR, 'a.dot')
        _footer_locator = (By.ID, 'footer')

        def __init__(self, base_url, selenium, elment):
            Page.__init__(self, base_url, selenium)
            self._root = elment

        def click_footer(self):
            self.selenium.find_element(*self._footer_locator).click()

        def next(self):
            self.click_footer()
            self._root.find_element(*self._next_locator).click()

        def prev(self):
            self.click_footer()
            self._root.find_element(*self._prev_locator).click()

        @property
        def dot_count(self):
            return len(self._root.find_elements(*self._dot_locator))

        @property
        def selected_dot(self):
            for idx, dot in enumerate(self._root.find_elements(*self._dot_locator)):
                if 'selected' in dot.get_attribute('class'):
                    return idx

        def click_dot(self, idx):
            self._root.find_elements(*self._dot_locator)[idx].click()

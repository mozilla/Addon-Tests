# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.page import Page


class Paginator(Page):

    # Numbering
    _page_number_locator = (By.CSS_SELECTOR, 'nav.paginator .num > a:nth-child(1)')
    _total_page_number_locator = (By.CSS_SELECTOR, 'nav.paginator .num > a:nth-child(2)')

    # Navigation
    _first_page_locator = (By.CSS_SELECTOR, 'nav.paginator .rel a:nth-child(1)')
    _prev_locator = (By.CSS_SELECTOR, 'nav.paginator .rel a.prev')
    _next_locator = (By.CSS_SELECTOR, 'nav.paginator .rel a.next')
    _last_page_locator = (By.CSS_SELECTOR, 'nav.paginator .rel a:nth-child(4)')

    # Position
    _start_item_number_locator = (By.CSS_SELECTOR, 'nav.paginator .pos b:nth-child(1)')
    _end_item_number_locator = (By.CSS_SELECTOR, 'nav.paginator .pos b:nth-child(2)')
    _total_item_number = (By.CSS_SELECTOR, 'nav.paginator .pos b:nth-child(3)')

    _updating_locator = (By.CSS_SELECTOR, "div.updating")

    @property
    def page_number(self):
        return int(self.selenium.find_element(*self._page_number_locator).text)

    @property
    def total_page_number(self):
        return int(self.selenium.find_element(*self._total_page_number_locator).text)

    def click_first_page(self):
        self._navigate(self._first_page_locator)

    def click_prev_page(self):
        self._navigate(self._prev_locator)

    @property
    def is_prev_page_disabled(self):
        return 'disabled' in self.selenium.find_element(*self._prev_locator).get_attribute('class')

    @property
    def is_first_page_disabled(self):
        return 'disabled' in self.selenium.find_element(*self._first_page_locator).get_attribute('class')

    def _navigate(self, locator):
        self.selenium.find_element(*locator).click()

    def click_next_page(self):
        self._navigate(self._next_locator)

    @property
    def is_next_page_disabled(self):
        return 'disabled' in self.selenium.find_element(*self._next_locator).get_attribute('class')

    def click_last_page(self):
        self._navigate(self._last_page_locator)

    @property
    def is_last_page_disabled(self):
        return 'disabled' in self.selenium.find_element(*self._last_page_locator).get_attribute('class')

    @property
    def start_item(self):
        return int(self.selenium.find_element(*self._start_item_number_locator).text)

    @property
    def end_item(self):
        return int(self.selenium.find_element(*self._end_item_number_locator).text)

    @property
    def total_items(self):
        return int(self.selenium.find_element(*self._total_item_number).text)

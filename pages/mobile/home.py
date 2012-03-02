#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from pages.mobile.base import Base


class Home(Base):

    _page_title = 'Add-ons for Firefox'

    _header_locator = (By.CSS_SELECTOR, 'h1.site-title > a')
    _header_logo_locator = (By.CSS_SELECTOR, '.site-title > a > img')
    _header_statement_locator = (By.CSS_SELECTOR, '#home-header > hgroup > h2')
    _learn_more_locator = (By.CSS_SELECTOR, '#learnmore')
    _learn_more_msg_locator = (By.CSS_SELECTOR, '#learnmore-msg')
    _search_box_locator = (By.CSS_SELECTOR, 'form#search > input')
    _search_button_locator = (By.CSS_SELECTOR, 'form#search > button')

    _all_featured_addons_locator = (By.CSS_SELECTOR, '#list-featured > li > a')
    _default_selected_tab_locator = (By.CSS_SELECTOR, 'li.selected a')

    def __init__(self, testsetup):
        Base.__init__(self, testsetup)
        self.selenium.get(self.base_url)

    @property
    def header_text(self):
        return self.selenium.find_element(*self._header_locator).text

    @property
    def header_title(self):
        return self.selenium.find_element(*self._header_locator).get_attribute('title')

    @property
    def header_statement_text(self):
        return self.selenium.find_element(*self._header_statement_locator).text

    @property
    def if_header_firefox_logo_visible(self):
        return self.selenium.find_element(*self._header_logo_locator).is_displayed()

    @property
    def header_firefox_logo_src(self):
        return self.selenium.find_element(*self._header_logo_locator).get_attribute('src')

    @property
    def learn_more_text(self):
        return self.selenium.find_element(*self._learn_more_locator).text

    def click_learn_more(self):
        self.selenium.find_element(*self._learn_more_locator).click()

    @property
    def learn_more_msg_text(self):
        return self.selenium.find_element(*self._learn_more_msg_locator).text

    @property
    def is_learn_more_msg_visible(self):
        return self.is_element_visible(*self._learn_more_msg_locator)

    def click_all_featured_addons_link(self):
        self.selenium.find_element(*self._all_featured_addons_locator).click()
        from pages.mobile.extensions import Extensions
        return Extensions(self.testsetup)

    @property
    def default_selected_tab_text(self):
        return self.selenium.find_element(*self._default_selected_tab_locator).text

    @property
    def is_search_box_visible(self):
        return self.is_element_visible(*self._search_box_locator)

    @property
    def search_box_placeholder(self):
        return self.selenium.find_element(*self._search_box_locator).get_attribute('placeholder')

    @property
    def is_search_button_visible(self):
        return self.is_element_visible(*self._search_button_locator)

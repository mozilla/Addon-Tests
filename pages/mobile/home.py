#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pages.mobile.base import Base
from selenium.webdriver.common.by import By


class Home(Base):

    _page_title = 'Add-ons for Firefox'

    _header_locator = (By.CSS_SELECTOR, 'h1.site-title > a')
    _header_statment_locator = (By.CSS_SELECTOR, '#home-header>hgroup>h2')
    _learn_more_locator = (By.CSS_SELECTOR, '#learnmore')
    _learn_more_msg_locator = (By.CSS_SELECTOR, '#learnmore-msg')

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
    def header_stetement_text(self):
        return self.selenium.find_element(*self._header_statment_locator).text

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

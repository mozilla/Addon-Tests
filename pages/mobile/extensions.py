#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from pages.mobile.base import Base


class Extensions(Base):

    _page_title_locator = (By.CSS_SELECTOR, 'h1.site-title > a')
    _page_header_locator = (By.CSS_SELECTOR, '#content > h2')

    @property
    def page_header(self):
        return self.selenium.find_element(*self._page_header_locator).text

    @property
    def title(self):
        return str(self.selenium.find_element(*self._page_title_locator).text)

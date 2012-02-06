#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import Base


class Category(Base):

    _category_title_locator = (By.CSS_SELECTOR, "div.island > h1")

    @property
    def category_header_title(self):
        return self.selenium.find_element(*self._category_title_locator).text

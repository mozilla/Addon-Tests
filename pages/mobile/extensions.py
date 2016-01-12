# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from pages.mobile.base import Base


class Extensions(Base):

    _page_title_locator = (By.CSS_SELECTOR, 'h1.site-title > a')
    _page_header_locator = (By.CSS_SELECTOR, '#content > h2')
    _sort_by_locator = (By.CSS_SELECTOR, '.label > span')

    @property
    def page_header(self):
        return self.selenium.find_element(*self._page_header_locator).text

    @property
    def title(self):
        return str(self.selenium.find_element(*self._page_title_locator).text)

    def click_sort_by(self):
        self.selenium.find_element(*self._sort_by_locator).click()
        from pages.mobile.regions.sorter import Sorter
        return Sorter(self.base_url, self.selenium)

#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import Base


class Collections(Base):

    _page_title = "Featured Collections :: Add-ons for Firefox"

    #Search box
    _search_button_locator = (By.CSS_SELECTOR, "button.search-button")
    _search_textbox_locator = (By.NAME, "q")
    _collection_name = (By.CSS_SELECTOR, "h2.collection > span")

    @property
    def collection_name(self):
        return self.selenium.find_element(*self._collection_name).text

    def search_for(self, search_term):
        search_box = self.selenium.find_element(*self._search_textbox_locator)
        search_box.send_keys(search_term)
        self.selenium.find_element(*self._search_button_locator).click()
        return CollectionsSearch(self.testsetup)


class CollectionsSearch(Base):

    _results_locator = (By.CSS_SELECTOR, "div.featured-inner div.item")

    @property
    def result_count(self):
        return len(self.selenium.find_elements(*self._results_locator))

#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

from pages.page import Page


class Sorter(Page):

    _sort_by_featured_locator = (By.LINK_TEXT, "Featured")
    _sort_by_relevance_locator = (By.LINK_TEXT, 'Relevance')
    _sort_by_most_users_locator = (By.LINK_TEXT, 'Most Users')
    _sort_by_top_rated_locator = (By.LINK_TEXT, 'Top Rated')
    _sort_by_newest_locator = (By.LINK_TEXT, 'Newest')

    _sort_by_name_locator = (By.XPATH, "//div[@id='sorter']//li/a[normalize-space(text())='Name']")
    _sort_by_weekly_downloads_locator = (By.XPATH, "//div[@id='sorter']//li/a[normalize-space(text())='Weekly Downloads']")
    _sort_by_recently_updated_locator = (By.XPATH, "//div[@id='sorter']//li/a[normalize-space(text())='Recently Updated']")
    _sort_by_up_and_coming_locator = (By.XPATH, "//div[@id='sorter']//li/a[normalize-space(text())='Up & Coming']")

    _hover_more_locator = (By.CSS_SELECTOR, "li.extras > a")
    _updating_locator = (By.CSS_SELECTOR, "div.updating")

    def sort_by(self, type):
        hover_element = self.selenium.find_element(*self._hover_more_locator)
        click_element = self.selenium.find_element(*getattr(self, '_sort_by_%s_locator' % type.replace(' ', '_').lower()))
        ActionChains(self.selenium).move_to_element(hover_element).\
            move_to_element(click_element).\
            click().perform()
        WebDriverWait(self.selenium, 10).until(lambda s: not self.is_element_present(*self._updating_locator))

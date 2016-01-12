# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.page import Page


class Breadcrumbs(Page):
    _breadcrumbs_locator = (By.CSS_SELECTOR, "#breadcrumbs li")

    @property
    def breadcrumbs(self):
        return [self.BreadcrumbItem(self.base_url, self.selenium, breadcrumb_list_item)
                for breadcrumb_list_item in self.selenium.find_elements(*self._breadcrumbs_locator)]

    class BreadcrumbItem(Page):
        _link_locator = (By.CSS_SELECTOR, 'a')

        def __init__(self, base_url, selenium, breadcrumb_list_element):
            Page.__init__(self, base_url, selenium)
            self._root_element = breadcrumb_list_element

        def click(self):
            self._root_element.find_element(*self._link_locator).click()

        @property
        def text(self):
            return self._root_element.text

        @property
        def href_value(self):
            return self._root_element.find_element(*self._link_locator).get_attribute('href')

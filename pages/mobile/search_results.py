# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.mobile.base import Base


class SearchResults(Base):

    _results_locator = (By.CSS_SELECTOR, '.addon-listing .item')

    def __init__(self, base_url, selenium, search_term):
        Base.__init__(self, base_url, selenium)
        self._page_title = "%s :: Search :: Add-ons for Firefox" % search_term

    @property
    def results(self):
        from pages.mobile.regions.addon_list_item import AddonItem
        return [AddonItem(self.base_url, self.selenium, element)
                for element in self.selenium.find_elements(*self._results_locator)]

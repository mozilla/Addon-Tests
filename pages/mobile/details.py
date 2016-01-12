# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re

from selenium.webdriver.common.by import By

from pages.mobile.base import Base


class Details(Base):

    _title_locator = (By.CSS_SELECTOR, 'div.infobox > h3')
    _contribute_button_locator = (By.XPATH, "//a[contains(.,'Contribute')]")

    def __init__(self, base_url, selenium, addon_name=None):
        # formats name for url
        Base.__init__(self, base_url, selenium)
        if (addon_name is not None):
            self.addon_name = addon_name.replace(" ", "-")
            self.addon_name = re.sub(r'[^A-Za-z0-9\-]', '', self.addon_name).lower()
            self.addon_name = self.addon_name[:27]
            self.selenium.get("%s/addon/%s" % (self.base_url, self.addon_name))

    @property
    def _page_title(self):
        return "%s :: Add-ons for Firefox" % self.title

    @property
    def title(self):
        return self.selenium.find_element(*self._title_locator).text

    @property
    def is_contribute_button_present(self):
        return self.is_element_present(*self._contribute_button_locator)

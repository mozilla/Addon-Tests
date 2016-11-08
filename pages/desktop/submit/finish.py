# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.desktop.base import Base


class Finish(Base):

    _manage_listing_locator = (By.CSS_SELECTOR, '.addon-submission-process .button')

    @property
    def is_manage_listing_displayed(self):
        return self.selenium.find_element(*self._manage_listing_locator).is_displayed()

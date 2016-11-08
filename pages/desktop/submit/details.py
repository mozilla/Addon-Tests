# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.desktop.base import Base


class Details(Base):

    _misc_category_locator = (By.CSS_SELECTOR, '.addon-misc-category input')
    _mpl_license_locator = (By.CSS_SELECTOR, '#id_builtin input')
    _submit_addon_locator = (By.CSS_SELECTOR, '.addon-submission-process button[type=submit]')

    def select_misc_category(self):
        return self.selenium.find_element(*self._misc_category_locator).click()

    def select_mpl_license(self):
        return self.selenium.find_element(*self._mpl_license_locator).click()

    def click_submit_addon(self):
        self.selenium.find_element(*self._submit_addon_locator).click()
        from finish import Finish
        return Finish(self.base_url, self.selenium)

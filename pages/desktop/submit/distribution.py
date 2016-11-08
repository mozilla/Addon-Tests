# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.desktop.base import Base


class Distribution(Base):

    _on_this_site_locator = (By.CSS_SELECTOR, '#id_choices input[value=listed]')
    _continue_locator = (By.CSS_SELECTOR, '.addon-submission-process button[type=submit]')

    def select_on_this_site(self):
        self.selenium.find_element(*self._on_this_site_locator).click()

    def click_continue(self):
        self.selenium.find_element(*self._continue_locator).click()
        from upload import Upload
        return Upload(self.base_url, self.selenium)

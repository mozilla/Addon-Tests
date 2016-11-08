# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.desktop.base import Base


class Upload(Base):

    _continue_locator = (By.ID, 'submit-upload-file-finish')
    _upload_addon_locator = (By.ID, 'upload-addon')
    _upload_progress_bar_success_locator = (By.CSS_SELECTOR, '#upload-file>.upload-status>.bar-success')

    @property
    def is_file_uploaded(self):
        return self.selenium.find_element(*self._upload_progress_bar_success_locator).is_displayed()

    def upload_addon(self, path):
        file_selector = self.selenium.find_element(*self._upload_addon_locator)
        file_selector.send_keys(path)
        self.wait.until(lambda s: self.is_file_uploaded)

    def click_continue(self):
        self.selenium.find_element(*self._continue_locator).click()
        from details import Details
        return Details(self.base_url, self.selenium)

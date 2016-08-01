# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait

from pages.page import Page
from pages.desktop.base import Base

import pytest
import time

class Submit(Base):

    _upload_addon_locator = (By.ID, "upload-addon")
    _upload_progress_bar_success_locator = (By.CSS_SELECTOR, "bar-success")
    _misc_category_locator = (By.CSS_SELECTOR, ".addon-misc-category.checkbox-choices>li>label")
    _mpl_license_locator = (By.CSS_SELECTOR, "#id_builtin>li>label")
    _review_button_locator = (By.CSS_SELECTOR, ".submit-buttons>button")
    _done_next_steps_locator = (By.CSS_SELECTOR, ".done-next-steps")
    _continue_to_step_3_locator = (By.ID, "submit-upload-file-finish")
    _continue_to_step_4_locator = (By.CSS_SELECTOR, ".submission-buttons.addon-submission-field>button")
    _continue_to_step_5_locator = (By.CSS_SELECTOR, ".edit-media-button.addon-submission-field>button")
    _continue_to_step_6_locator = (By.CSS_SELECTOR, ".submission-buttons.addon-submission-field>button")

    @property
    def is_file_uploaded(self):
        return self.selenium.find_element(*self._upload_progress_bar_success_locator).is_displayed()

    @property
    def is_next_steps_present(self):
        return self.selenium.find_element(*self._done_next_steps_locator).is_displayed()

    def upload_addon(self, path):
        file_selector = self.selenium.find_element(*self._upload_addon_locator)
        file_selector.send_keys(path)
        self.wait.until(lambda s: self.is_file_uploaded)

    def click_misc_option(self):
        self.selenium.find_element(*self._misc_category_locator).click()

    def click_mpl_license(self):
        self.selenium.find_element(*self._mpl_license_locator).click()

    def click_review_button(self):
        self.selenium.find_element(*self._review_button_locator).click()

    def continue_to_step_three(self):
        self.selenium.find_element(*self._continue_to_step_3_locator).click()

    def continue_to_step_four(self):
        self.selenium.find_element(*self._continue_to_step_4_locator).click()

    def continue_to_step_five(self):
        self.selenium.find_element(*self._continue_to_step_5_locator).click()

    def continue_to_step_six(self):
        self.selenium.find_element(*self._continue_to_step_6_locator).click()

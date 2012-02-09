#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from pages.page import Page
from selenium.webdriver.common.by import By


class BrowserID(Page):

    _email_locator = (By.ID, 'email')
    _password_locator = (By.ID, 'password')

    _log_in_button_locator = (By.CSS_SELECTOR, 'button.returning')
    _next_button_locator = (By.CSS_SELECTOR, 'button.start')
    _sign_in_locator = (By.ID, 'signInButton')

    def __init__(self, testsetup):
        Page.__init__(self, testsetup)
        all_window_handles = self.selenium.window_handles
        for handle in all_window_handles:
            self.selenium.switch_to_window(handle)
            if self.selenium.title == "BrowserID":
                break

    def login_browser_id(self, user):
        credentials = self.testsetup.credentials[user]

        self.selenium.find_element(*self._email_locator).send_keys(credentials['email'])
        self.selenium.find_element(*self._next_button_locator).click()

        self.selenium.find_element(*self._password_locator).send_keys(credentials['password'])
        self.selenium.find_element(*self._log_in_button_locator).click()

    def sign_in(self):
        self.selenium.find_element(*self._sign_in_locator).click()
        self.selenium.switch_to_window('')

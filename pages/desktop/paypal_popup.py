#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from pages.page import Page
from selenium.webdriver.common.by import By


class PayPalPopup(Page):

    _pop_up_id = '_popupFlow'
    _email_locator = (By.ID, 'email')
    _password_locator = (By.ID, 'password')
    _login_locator = (By.CSS_SELECTOR, 'p.buttons > input')
    _log_out_locator = (By.ID, 'logOutLink')

    _pay_button_locator = (By.NAME, '_eventId_submit')
    _order_details_locator = (By.ID, 'order-details')

    def __init__(self, testsetup):
        Page.__init__(self, testsetup)
        self.selenium.switch_to_window(self._pop_up_id)

    def login_paypal(self, user):
        credentials = self.testsetup.credentials[user]
        self.selenium.find_element(*self._email_locator).send_keys(credentials['email'])
        self.selenium.find_element(*self._password_locator).send_keys(credentials['password'])
        self.selenium.find_element(*self._login_locator).click()

    def close_paypal_popup(self):
        self.selenium.find_element(*self._pay_button_locator).click()
        self.selenium.switch_to_window('')

    @property
    def is_user_logged_into_paypal(self):
        return self.is_element_visible(*self._log_out_locator)

    def click_pay(self):
        self.selenium.find_element(*self._pay_button_locator).click()

    @property
    def is_payment_successful(self):
        return self.is_element_visible(*self._order_details_locator)

#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re

from pages.page import Page

from selenium.webdriver.common.by import By


class PayPalFrame(Page):

    _iframe_id = 'PPDGFrame'
    _paypal_login_button = (By.CSS_SELECTOR, 'div.logincnt > p > a.button')

    def __init__(self, testsetup):
        Page.__init__(self, testsetup)
        self.selenium.switch_to_frame(self._iframe_id)

    def login_to_paypal(self, user="paypal"):
        self.selenium.find_element(*self._paypal_login_button).click()

        from pages.paypal_popup import PayPalPopup
        pop_up = PayPalPopup(self.testsetup)
        pop_up.login_paypal(user)
        return PayPalPopup(self.testsetup)

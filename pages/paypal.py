#!/usr/bin/env python

# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is Mozilla WebQA Selenium Tests.
#
# The Initial Developer of the Original Code is
# Mozilla.
# Portions created by the Initial Developer are Copyright (C) 2012
# the Initial Developer. All Rights Reserved.
#
# Contributor(s): Teodosia Pop <teodosia.pop@softvision.ro>
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
#
# ***** END LICENSE BLOCK *****


from pages.page import Page
from selenium.webdriver.common.by import By

class PayPal(Page):

    _pop_up_id = '_wrapper'
    _email_locator = (By.ID, 'email')
    _password_locator = (By.ID, 'password')

    _paypal_login_button = (By.CSS_SELECTOR, 'div.logincnt > p > a.button')
    _log_in_button_locator = (By.ID, 'login')
    _next_button_locator = (By.CSS_SELECTOR, 'button.start')
    _sign_in_locator = (By.ID, 'signInButton')
    _log_out_locator = (By.ID, 'logOutLink')
    _pay_button_locator = (By.ID, '_eventId_submit')
    _order_details_locator = (By.ID, 'order-details')

    def __init__(self, testsetup):
        Page.__init__(self, testsetup)
        #self.selenium.switch_to_frame(self._pop_up_id)

    def login_to_paypal(self, user="paypal"):
        self.selenium.find_element(*self._paypal_login_button).click()
        #from pages.paypal import PayPal
        #pop_up = PayPal(self.testsetup)
        self.login_paypal(user)

    def login_paypal(self, user):
        credentials = self.testsetup.credentials[user]

        self.selenium.find_element(*self._email_locator).send_keys(credentials['email'])
        self.selenium.find_element(*self._password_locator).send_keys(credentials['password'])

    def close(self):
        self.selenium.find_element(*self._pay_button_locator).click()
        self.selenium.switch_to_window('')

    @property
    def is_user_logged_in(self):
        self.is_element_visible(*self._log_out_locator)

    def click_pay(self):
        self.selenium.find_element(*self._pay_button_locator).click()

    @property
    def is_payment_successful(self):
        self.is_element_visible(*self._order_details_locator)

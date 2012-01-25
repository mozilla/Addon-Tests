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

class PayPalFrame(Page):

    _iframe_id = 'PPDGFrame'

    _paypal_login_button = (By.CSS_SELECTOR, 'div.logincnt > p > a.button')
    _finish_purchase_locator = (By.ID, 'addon_info')
    _close_frame_locator = (By.CSS_SELECTOR, 'div#site-nonfx > a.close')

    def __init__(self, testsetup):
        Page.__init__(self, testsetup)
        self.selenium.switch_to_frame(self._iframe_id)

    def login_to_paypal(self, user="paypal"):
        self.selenium.find_element(*self._paypal_login_button).click()
        from pages.paypal_window import PayPal
        pop_up = PayPal(self.testsetup)
        pop_up.login_paypal(user)
        return PayPal(self.testsetup)

    @property
    def is_purchase_successful(self):
        purchase_message = self.selenium.find_element(*self._finish_purchase_locator).text
        return ('Your purchase of Adhaadhoora is complete.' in purchase_message)

    def close_paypal_frame(self):
        self.selenium.find_element(*self._close_frame_locator).click()
        self.selenium.switch_to_window('')

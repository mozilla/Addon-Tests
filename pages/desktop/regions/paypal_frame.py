# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from pages.page import Page

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected


class PayPalFrame(Page):

    _frame_locator = (By.NAME, 'PPDGFrame')
    _logo_locator = (By.CSS_SELECTOR, '.logo > img')
    _paypal_login_button = (By.CSS_SELECTOR, 'div.logincnt > p > a.button')

    def __init__(self, base_url, selenium):
        Page.__init__(self, base_url, selenium)
        frame = self.wait.until(
            expected.presence_of_element_located(self._frame_locator),
            'PayPal frame is not present')
        self.selenium.switch_to_frame(frame)
        # wait for the paypal logo to appear, then we know the frame's contents has loaded
        self.wait.until(
            expected.visibility_of_element_located(self._logo_locator),
            'PayPal logo is not displayed')

    def login_to_paypal(self, email, password):
        self.selenium.find_element(*self._paypal_login_button).click()

        from pages.desktop.paypal_popup import PayPalPopup
        pop_up = PayPalPopup(self.base_url, self.selenium)
        pop_up.login_paypal(email, password)
        return PayPalPopup(self.base_url, self.selenium)

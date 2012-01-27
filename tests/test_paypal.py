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


from unittestzero import Assert

from pages.home import Home
from pages.details import Details


class TestPaypal:
    """
    This test only works with Firefox 7.
    Until Selenium issue http://code.google.com/p/selenium/issues/detail?id=2067 is fixed.
    """

    addon_name = 'Adhaadhoora'

    def test_that_user_can_purchase_an_addon(self, mozwebqa):
        """Test for purchasing an addon using PayPal."""
        addon_page = Home(mozwebqa)

        addon_page.login('browserID')
        Assert.true(addon_page.is_the_current_page)
        Assert.true(addon_page.header.is_user_logged_in)

        addon_page = Details(mozwebqa, self.addon_name)

        eula_page = addon_page.click_purchase_button()
        eula_page.click_purchase_button()
        Assert.true(eula_page.is_purchase_addon_dialog_visible)
        Assert.true(eula_page.is_pay_with_paypal_button_visible)

        paypal_frame = eula_page.click_pay_with_paypal()
        payment_popup = paypal_frame.login_to_paypal(user="paypal")
        Assert.true(payment_popup.is_user_logged_into_paypal)
        payment_popup.click_pay()
        Assert.true(payment_popup.is_payment_successful)
        payment_popup.close_paypal_popup()
        Assert.true(paypal_frame.is_purchase_successful)
        paypal_frame.close_paypal_frame()
        Assert.true(eula_page.is_accept_and_install_button_visible)

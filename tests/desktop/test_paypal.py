# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import pytest


from pages.desktop.details import Details


class TestPaypal:

    addon_name = 'Firebug'

    @pytest.mark.flaky(reruns=1)
    def test_that_user_can_contribute_to_an_addon(self, base_url, selenium, logged_in, paypal_user):
        """Test that checks the Contribute button for an add-on using PayPal."""
        addon_page = Details(base_url, selenium, self.addon_name)
        contribution_snippet = addon_page.click_contribute_button()
        paypal_frame = contribution_snippet.click_make_contribution_button()
        assert addon_page.is_paypal_login_dialog_visible

        payment_popup = paypal_frame.login_to_paypal(paypal_user['email'], paypal_user['password'])
        assert payment_popup.is_user_logged_into_paypal
        payment_popup.click_pay()
        assert payment_popup.is_payment_successful
        payment_popup.close_paypal_popup()
        assert addon_page.is_the_current_page

    @pytest.mark.flaky(reruns=1)
    def test_that_user_can_make_a_contribution_without_logging_into_amo(self, base_url, selenium, paypal_user):
        """Test that checks if the user is able to make a contribution without logging in to AMO."""
        addon_page = Details(base_url, selenium, self.addon_name)
        assert not addon_page.header.is_user_logged_in

        contribution_snippet = addon_page.click_contribute_button()
        paypal_frame = contribution_snippet.click_make_contribution_button()
        assert addon_page.is_paypal_login_dialog_visible

        payment_popup = paypal_frame.login_to_paypal(paypal_user['email'], paypal_user['password'])
        assert payment_popup.is_user_logged_into_paypal
        payment_popup.click_pay()
        assert payment_popup.is_payment_successful
        payment_popup.close_paypal_popup()
        assert addon_page.is_the_current_page

    @pytest.mark.smoke
    @pytest.mark.nondestructive
    def test_that_make_contribution_button_is_clickable_and_loads_paypal_frame_while_user_is_logged_out(self, base_url, selenium):
        addon_page = Details(base_url, selenium, self.addon_name)
        assert not addon_page.header.is_user_logged_in

        contribution_snippet = addon_page.click_contribute_button()
        assert contribution_snippet.is_make_contribution_button_visible
        assert 'Make Contribution' == contribution_snippet.make_contribution_button_name

        contribution_snippet.click_make_contribution_button()
        assert addon_page.is_paypal_login_dialog_visible

    @pytest.mark.smoke
    def test_that_make_contribution_button_is_clickable_and_loads_paypal_frame_while_user_is_logged_in(self, base_url, selenium, logged_in):
        addon_page = Details(base_url, selenium, self.addon_name)
        contribution_snippet = addon_page.click_contribute_button()
        assert contribution_snippet.is_make_contribution_button_visible
        assert 'Make Contribution' == contribution_snippet.make_contribution_button_name

        contribution_snippet.click_make_contribution_button()
        assert addon_page.is_paypal_login_dialog_visible

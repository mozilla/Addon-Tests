#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
import random
from copy import deepcopy

from unittestzero import Assert

from pages.desktop.home import Home


class TestAccounts:

    @pytest.mark.nondestructive
    @pytest.mark.login
    def test_user_can_login_and_logout(self, mozwebqa):
        """
        Test for Litmus 7857 and 4859.
        https://litmus.mozilla.org/show_test.cgi?id=7857
        https://litmus.mozilla.org/show_test.cgi?id=4859
        """

        home_page = Home(mozwebqa)
        home_page.login("normal")
        Assert.true(home_page.is_the_current_page)
        Assert.true(home_page.header.is_user_logged_in)

        home_page.header.click_logout()
        Assert.false(home_page.header.is_user_logged_in)

    @pytest.mark.nondestructive
    @pytest.mark.login
    def test_user_can_login_and_logout_using_browser_id(self, mozwebqa):
        """
        Test for Litmus 7857 and 4859.
        https://litmus.mozilla.org/show_test.cgi?id=7857
        https://litmus.mozilla.org/show_test.cgi?id=4859
        """

        home_page = Home(mozwebqa)
        home_page.login("browserID")
        Assert.true(home_page.is_the_current_page)
        Assert.true(home_page.header.is_user_logged_in)

        home_page.header.click_logout()
        Assert.false(home_page.header.is_user_logged_in)

    @pytest.mark.native
    @pytest.mark.nondestructive
    @pytest.mark.login
    def test_user_can_access_the_edit_profile_page(self, mozwebqa):
        """
        Test for Litmus 5039.
        https://litmus.mozilla.org/show_test.cgi?id=5039
        """

        home_page = Home(mozwebqa)
        home_page.login("browserID")
        Assert.true(home_page.is_the_current_page)
        Assert.true(home_page.header.is_user_logged_in)

        amo_user_edit_page = home_page.header.click_edit_profile()
        Assert.contains("/users/edit", amo_user_edit_page.get_url_current_page())
        Assert.true(amo_user_edit_page.is_the_current_page)

        Assert.equal("My Account", amo_user_edit_page.account_header_text)
        Assert.equal("Profile", amo_user_edit_page.profile_header_text)
        Assert.equal("Details", amo_user_edit_page.details_header_text)
        Assert.equal("Notifications", amo_user_edit_page.notification_header_text)

    @pytest.mark.native
    @pytest.mark.nondestructive
    @pytest.mark.login
    @pytest.mark.xfail(reason="bugzilla 731880")
    def test_user_can_access_the_view_profile_page(self, mozwebqa):
        """
        Test for litmus 15400.
        https://litmus.mozilla.org/show_test.cgi?id=15400
        """

        home_page = Home(mozwebqa)
        home_page.login("browserID")
        Assert.true(home_page.is_the_current_page)
        Assert.true(home_page.header.is_user_logged_in)

        view_profile_page = home_page.header.click_view_profile()

        Assert.equal(view_profile_page.about_me, 'About me')

    @pytest.mark.native
    @pytest.mark.xfail(reason="https://www.pivotaltracker.com/story/show/23966893")
    @pytest.mark.login
    def test_hide_email_checkbox_works(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.login("browserID")

        Assert.true(home_page.is_the_current_page)
        Assert.true(home_page.header.is_user_logged_in)

        view_profile_page = home_page.header.click_view_profile()
        initial_state = view_profile_page.is_email_field_present

        edit_profile_page = home_page.header.click_edit_profile()
        edit_profile_page.change_hide_email_state()
        edit_profile_page.click_update_account()

        view_profile_page = home_page.header.click_view_profile()
        final_state = view_profile_page.is_email_field_present

        try:
            Assert.not_equal(initial_state, final_state, 'The initial and final states are the same. The profile change failed.')
            if final_state is True:
                credentials = mozwebqa.credentials['default']
                Assert.equal(credentials['email'], view_profile_page.email_value, 'Actual value is not equal with the expected one.')

        except Exception as exception:
            Assert.fail(exception.msg)

        finally:
            if initial_state != final_state:
                edit_profile_page = home_page.header.click_edit_profile()
                edit_profile_page.change_hide_email_state()
                edit_profile_page.click_update_account()
                view_profile_page = home_page.header.click_view_profile()

            Assert.equal(view_profile_page.is_email_field_present, initial_state, 'Could not restore profile to initial state.')

    @pytest.mark.native
    @pytest.mark.login
    def test_user_can_update_profile_information_in_account_settings_page(self, mozwebqa):
        """
        Test for Litmus 11563.
        https://litmus.mozilla.org/show_test.cgi?id=11563
        """
        home_page = Home(mozwebqa)
        home_page.login(method="browserID", user="user.edit")

        Assert.true(home_page.is_the_current_page)
        Assert.true(home_page.header.is_user_logged_in)

        user_edit_page = home_page.header.click_edit_profile()
        Assert.true(user_edit_page.is_the_current_page)

        # save initial values to restore them after the test is finished
        fields_no = len(user_edit_page.profile_fields) - 1
        initial_value = [None] * fields_no
        random_name = "test%s" % random.randrange(1, 100)

        # enter new values
        for i in range(0, fields_no):
            initial_value[i] = deepcopy(user_edit_page.profile_fields[i].field_value)
            user_edit_page.profile_fields[i].clear_field()
            user_edit_page.profile_fields[i].type_value(random_name)

        user_edit_page.click_update_account()
        Assert.equal(user_edit_page.update_message, "Profile Updated")

        # using try finally to ensure that the initial values are restore even if the Asserts fail.
        try:
            for i in range(0, fields_no):
                Assert.contains(random_name, user_edit_page.profile_fields[i].field_value)

        except Exception as exception:
            Assert.fail(exception.msg)

        finally:
            # restore initial values
            for i in range(0, fields_no):
                user_edit_page.profile_fields[i].clear_field()
                user_edit_page.profile_fields[i].type_value(initial_value[i])

            user_edit_page.click_update_account()

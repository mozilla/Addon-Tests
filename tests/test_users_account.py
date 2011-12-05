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
# Portions created by the Initial Developer are Copyright (C) 2011
# the Initial Developer. All Rights Reserved.
#
# Contributor(s): Bebe <florin.strugariu@softvision.ro>
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

import pytest

from unittestzero import Assert

from pages.home import Home

nondestructive = pytest.mark.nondestructive
destructive = pytest.mark.destructive


class TestAccounts:

    @nondestructive
    def test_user_can_login_and_logout(self, mozwebqa):
        """ Test for litmus 7857
            https://litmus.mozilla.org/show_test.cgi?id=7857
            Test for litmus 4859
            https://litmus.mozilla.org/show_test.cgi?id=4859
        """

        home_page = Home(mozwebqa)
        home_page.login()
        Assert.true(home_page.is_the_current_page)
        Assert.true(home_page.header.is_user_logged_in)

        home_page.header.click_logout()
        Assert.false(home_page.header.is_user_logged_in)

    @nondestructive
    def test_user_can_access_the_edit_profile_page(self, mozwebqa):
        """
            Test for litmus 5039
            https://litmus.mozilla.org/show_test.cgi?id=5039
        """

        home_page = Home(mozwebqa)
        home_page.login()
        Assert.true(home_page.is_the_current_page)
        Assert.true(home_page.header.is_user_logged_in)

        amo_user_edit_page = home_page.header.click_edit_profile()
        Assert.contains("/users/edit", amo_user_edit_page.get_url_current_page())
        Assert.true(amo_user_edit_page.is_the_current_page)

        Assert.equal("My Account", amo_user_edit_page.account_header_text)
        Assert.equal("Profile", amo_user_edit_page.profile_header_text)
        Assert.equal("Details", amo_user_edit_page.details_header_text)
        Assert.equal("Notifications", amo_user_edit_page.notification_header_text)

    @nondestructive
    def test_user_can_access_the_view_profile_page(self, mozwebqa):
        """
        Test for litmus 15400
        https://litmus.mozilla.org/show_test.cgi?id=15400
        """

        home_page = Home(mozwebqa)
        home_page.login()
        Assert.true(home_page.is_the_current_page)
        Assert.true(home_page.header.is_user_logged_in)

        view_profile_page = home_page.header.click_view_profile()

        Assert.equal(view_profile_page.about_me, 'About me')

    @destructive
    def test_hide_email_checkbox_works(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.login()

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

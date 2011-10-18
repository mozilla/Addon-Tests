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
#                 Stephen Donner
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

from base_page import BasePage


class LoginPage(BasePage):

    _page_title = 'User Login :: Add-ons for Firefox'
    _email_locator = 'id=id_username'
    _password_locator = 'id=id_password'
    _login_button_locator = 'id=login-submit'

    def login_user(self, user):
        credentials = self.testsetup.credentials[user]
        self.wait_for_element_present(self._email_locator)
        self.selenium.type(self._email_locator, credentials['email'])
        self.selenium.type(self._password_locator, credentials['password'])
        self.selenium.click(self._login_button_locator)
        self.selenium.wait_for_page_to_load(self.timeout)


class ViewProfilePage(BasePage):

    _page_title = 'User Info for Test :: Add-ons for Firefox'
    _about_locator = 'css=div.island > section.primary > h2'

    @property
    def about_me(self):
        return self.selenium.get_text(self._about_locator)


class UserPage(BasePage):

        _username_locator = "css=div.vcard h2.fn"

        @property
        def username(self):
            return self.selenium.get_text(self._username_locator)


class EditProfilePage(BasePage):

    _page_title = 'Account Settings :: Add-ons for Firefox'
    _account_locator = "css=#acct-account > legend"
    _profile_locator = "css=#profile-personal > legend"
    _details_locator = "css=#profile-detail > legend"
    _notification_locator = "css=#acct-notify > legend"

    @property
    def is_account_visible(self):
        return self.selenium.get_text(self._account_locator)

    @property
    def is_profile_visible(self):
        return self.selenium.get_text(self._profile_locator)

    @property
    def is_details_visible(self):
        return self.selenium.get_text(self._details_locator)

    @property
    def is_notification_visible(self):
        return self.selenium.get_text(self._notification_locator)

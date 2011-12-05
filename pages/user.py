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

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from pages.base import Base


class Login(Base):

    _page_title = 'User Login :: Add-ons for Firefox'

    _email_locator = (By.ID, 'id_username')
    _password_locator = (By.ID, 'id_password')
    _login_button_locator = (By.ID, 'login-submit')
    _normal_login_locator = (By.ID, 'show-normal-login')

    def login_user(self, user):
        credentials = self.testsetup.credentials[user]
        self.selenium.find_element(*self._normal_login_locator).click()

        email = self.selenium.find_element(*self._email_locator)
        email.send_keys(credentials['email'])

        password = self.selenium.find_element(*self._password_locator)
        password.send_keys(credentials['password'])

        password.send_keys(Keys.RETURN)


class ViewProfile(Base):

    _page_title = 'User Info for Test :: Add-ons for Firefox'

    _about_locator = (By.CSS_SELECTOR, "div.island > section.primary > h2")
    _email_locator = (By.CSS_SELECTOR, 'a.email')

    @property
    def about_me(self):
        return self.selenium.find_element(*self._about_locator).text

    @property
    def is_email_field_present(self):
        return self.is_element_present(*self._email_locator)

    @property
    def email_value(self):
        email = self.selenium.find_element(*self._email_locator).text
        return email[::-1]


class User(Base):

        _username_locator = (By.CSS_SELECTOR, "div#page > h1")

        @property
        def username(self):
            return self.selenium.find_element(*self._username_locator).text


class EditProfile(Base):

    _page_title = 'Account Settings :: Add-ons for Firefox'

    _account_locator = (By.CSS_SELECTOR, "#acct-account > legend")
    _profile_locator = (By.CSS_SELECTOR, "#profile-personal > legend")
    _details_locator = (By.CSS_SELECTOR, "#profile-detail > legend")
    _notification_locator = (By.CSS_SELECTOR, "#acct-notify > legend")
    _hide_email_checkbox = (By.ID, 'id_emailhidden')
    _update_account_locator = (By.CSS_SELECTOR, 'p.footer-submit > button.prominent')

    @property
    def account_header_text(self):
        return self.selenium.find_element(*self._account_locator).text

    @property
    def profile_header_text(self):
        return self.selenium.find_element(*self._profile_locator).text

    @property
    def details_header_text(self):
        return self.selenium.find_element(*self._details_locator).text

    @property
    def notification_header_text(self):
        return self.selenium.find_element(*self._notification_locator).text

    def click_update_account(self):
        self.selenium.find_element(*self._update_account_locator).click()

    def change_hide_email_state(self):
        self.selenium.find_element(*self._hide_email_checkbox).click()

#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from pages.desktop.base import Base
from pages.page import Page


class Login(Base):

    _page_title = 'User Login :: Add-ons for Firefox'

    _email_locator = (By.ID, 'id_username')
    _password_locator = (By.ID, 'id_password')
    _login_button_locator = (By.ID, 'login-submit')
    _logout_locator = (By.CSS_SELECTOR, '.logout')
    _normal_login_locator = (By.ID, 'show-normal-login')
    _browser_id_locator = (By.CSS_SELECTOR, 'button.browserid-login')

    _pop_up_id = '_mozid_signin'

    def login_user_normal(self, user):
        credentials = self.testsetup.credentials[user]

        email = self.selenium.find_element(*self._email_locator)
        email.send_keys(credentials['email'])

        password = self.selenium.find_element(*self._password_locator)
        password.send_keys(credentials['password'])

        password.send_keys(Keys.RETURN)

    def login_user_browser_id(self, user):
        credentials = self.testsetup.credentials[user]
        from browserid import BrowserID
        pop_up = BrowserID(self.selenium, self.timeout)
        pop_up.sign_in(credentials['email'], credentials['password'])
        WebDriverWait(self.selenium, 20).until(lambda s: s.find_element(*self._logout_locator))

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

        _username_locator = (By.CSS_SELECTOR, ".fn.n")

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
    _profile_fields_locator = (By.CSS_SELECTOR, '#profile-personal > ol.formfields li')
    _update_message_locator = (By.CSS_SELECTOR, 'div.notification-box > h2')

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

    @property
    def profile_fields(self):
        return [self.ProfileSection(self.testsetup, web_element)
                        for web_element in self.selenium.find_elements(*self._profile_fields_locator)]

    @property
    def update_message(self):
        return self.selenium.find_element(*self._update_message_locator).text

    class ProfileSection(Page):

        _input_field_locator = (By.CSS_SELECTOR, ' input')
        _field_name = (By.CSS_SELECTOR, ' label')

        def __init__(self, testsetup, element):
            Page.__init__(self, testsetup)
            self._root_element = element

        @property
        def field_value(self):
            try:
                return self._root_element.find_element(*self._input_field_locator).get_attribute('value')
            except Exception.NoSuchAttributeException:
                return " "

        @property
        def field_name(self):
            return self._root_element.find_element(*self._field_name).text

        def type_value(self, value):
            if self.field_name == 'Homepage' and value != '':
                self._root_element.find_element(*self._input_field_locator).send_keys('http://example.com/' + value)
            else:
                self._root_element.find_element(*self._input_field_locator).send_keys(value)

        def clear_field(self):
            self._root_element.find_element(*self._input_field_locator).clear()


class MyCollections(Base):

    _header_locator = (By.CSS_SELECTOR, "h2")

    @property
    def my_collections_header_text(self):
        return self.selenium.find_element(*self._header_locator).text


class MyFavorites(Base):

    _header_locator = (By.CSS_SELECTOR, 'h2.collection > span')
    _page_title = 'My Favorite Add-ons :: Collections :: Add-ons for Firefox'

    @property
    def my_favorites_header_text(self):
        return self.selenium.find_element(*self._header_locator).text

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchAttributeException

from pages.desktop.base import Base
from pages.page import Page


class Login(Base):

    _page_title = 'User Login :: Add-ons for Firefox'

    _email_locator = (By.ID, 'id_username')
    _password_locator = (By.ID, 'id_password')

    def login(self, email, password):
        self.selenium.find_element(*self._email_locator).send_keys(email)
        self.selenium.find_element(*self._password_locator).send_keys(password + Keys.RETURN)


class ViewProfile(Base):

    _page_title = 'User Info for amo.account :: Add-ons for Firefox'

    _about_locator = (By.CSS_SELECTOR, "div.island > section.primary > h2")
    _email_locator = (By.CSS_SELECTOR, 'a.email')

    def __init__(self, base_url, selenium):
        Base.__init__(self, base_url, selenium)
        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: (s.find_element(*self._about_locator)).is_displayed())

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

    def __init__(self, base_url, selenium):
        Base.__init__(self, base_url, selenium)
        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: (s.find_element(*self._account_locator)).is_displayed())

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
        WebDriverWait(self.selenium, self.timeout).until(lambda s: self.update_message == "Profile Updated")

    def change_hide_email_state(self):
        self.selenium.find_element(*self._hide_email_checkbox).click()

    @property
    def profile_fields(self):
        return [self.ProfileSection(self.base_url, self.selenium, web_element)
                for web_element in self.selenium.find_elements(*self._profile_fields_locator)]

    @property
    def update_message(self):
        return self.selenium.find_element(*self._update_message_locator).text

    class ProfileSection(Page):

        _input_field_locator = (By.CSS_SELECTOR, ' input')
        _field_name = (By.CSS_SELECTOR, ' label')

        def __init__(self, base_url, selenium, element):
            Page.__init__(self, base_url, selenium)
            self._root_element = element

        @property
        def field_value(self):
            try:
                return self._root_element.find_element(*self._input_field_locator).get_attribute('value')
            except NoSuchAttributeException:
                return ' '

        @property
        def input_type(self):
            try:
                return self._root_element.find_element(*self._input_field_locator).get_attribute('type')
            except (NoSuchElementException, NoSuchAttributeException):
                return ' '

        @property
        def is_field_editable(self):
            return self.input_type == 'text' or self.input_type == 'url'

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

    _header_locator = (By.CSS_SELECTOR, ".primary > header > h2")

    @property
    def my_collections_header_text(self):
        return self.selenium.find_element(*self._header_locator).text


class MyFavorites(Base):

    _header_locator = (By.CSS_SELECTOR, 'h2.collection > span')
    _page_title = 'My Favorite Add-ons :: Collections :: Add-ons for Firefox'

    @property
    def my_favorites_header_text(self):
        return self.selenium.find_element(*self._header_locator).text

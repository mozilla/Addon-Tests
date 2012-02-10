#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.desktop.base import Base
from pages.page import Page


class Collections(Base):

    _page_title = "Featured Collections :: Add-ons for Firefox"

    #Search box
    _search_button_locator = (By.CSS_SELECTOR, "button.search-button")
    _search_textbox_locator = (By.NAME, "q")
    _collection_name = (By.CSS_SELECTOR, "h2.collection > span")

    _create_a_collection_locator = (By.CSS_SELECTOR, "#side-nav .button")

    @property
    def collection_name(self):
        return self.selenium.find_element(*self._collection_name).text

    def search_for(self, search_term):
        search_box = self.selenium.find_element(*self._search_textbox_locator)
        search_box.send_keys(search_term)
        self.selenium.find_element(*self._search_button_locator).click()
        return CollectionsSearch(self.testsetup)

    def click_create_collection_button(self):
        self.selenium.find_element(*self._create_a_collection_locator).click()
        return self.CreateNewCollection(self.testsetup)

    class UserCollections(Page):

        _collections_locator = (By.CSS_SELECTOR, ".featured-inner")
        _collection_text_locator = (By.CSS_SELECTOR, ".item > h3 > a")

        @property
        def collection_text(self):
            return self.selenium.find_element(*self._collections_locator).text

        @property
        def collections(self):
            return self.selenium.find_elements(*self._collections_locator)

    class CreateNewCollection(Page):

        _name_field_locator = (By.ID, "id_name")
        _description_field_locator = (By.ID, "id_description")
        _create_collection_button_locator = (By.CSS_SELECTOR, ".featured-inner>form>p>input")

        def type_name(self, value):
            self.selenium.find_element(*self._name_field_locator).send_keys(value)

        def type_description(self, value):
            self.selenium.find_element(*self._description_field_locator).send_keys('Description is ' + value)

        def click_create_collection(self):
            self.selenium.find_element(*self._create_collection_button_locator).click()
            return Collection(self.testsetup)


class Collection(Base):

    _notification_locator = (By.CSS_SELECTOR, ".notification-box.success h2")
    _collection_name_locator = (By.CSS_SELECTOR, ".collection > span")
    _delete_collection_locator = (By.CSS_SELECTOR, ".delete")
    _delete_confirmation_locator = (By.CSS_SELECTOR, ".section > form > button")

    @property
    def notification(self):
        return self.selenium.find_element(*self._notification_locator).text

    @property
    def collection_name(self):
        return self.selenium.find_element(*self._collection_name_locator).text

    def delete(self):
        self.selenium.find_element(*self._delete_collection_locator).click()

    def delete_confirmation(self):
        self.selenium.find_element(*self._delete_confirmation_locator).click()
        return Collections.UserCollections(self.testsetup)


class CollectionsSearch(Base):

    _results_locator = (By.CSS_SELECTOR, "div.featured-inner div.item")

    @property
    def result_count(self):
        return len(self.selenium.find_elements(*self._results_locator))

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
#                 Alex Rodionov <p0deje@gmail.com>
#                 Teodosia Pop <teodosia.pop@softvision.ro>
#                 Alex Lakatos <alex@greensqr.com>
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

import re

from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait

from pages.page import Page


class Base(Page):

    _current_page_locator = (By.CSS_SELECTOR, ".paginator .num > a:nth-child(1)")

    _amo_logo_link_locator = (By.CSS_SELECTOR, ".site-title a")
    _amo_logo_image_locator = (By.CSS_SELECTOR, ".site-title img")

    _mozilla_logo_link_locator = (By.CSS_SELECTOR, "#global-header-tab a")

    _breadcrumbs_locator = (By.CSS_SELECTOR, "#breadcrumbs > ol  li")
    _footer_locator = (By.CSS_SELECTOR, "#footer")

    def login(self, type="normal", user="default"):
        if type == "normal":
            self.selenium.get(self.base_url + "/en-US/firefox/users/login")
            from pages.user import Login
            login = Login(self.testsetup)
            login.login_user_normal(user)
        elif type == "browserID":
            login = self.header.click_login_browser_id()
            login.login_user_browser_id(user)

    @property
    def page_title(self):
        WebDriverWait(self.selenium, 10).until(lambda s: self.selenium.title)
        return self.selenium.title

    @property
    def amo_logo_title(self):
        return self.selenium.find_element(*self._amo_logo_link_locator).get_attribute('title')

    @property
    def amo_logo_image_source(self):
        return self.selenium.find_element(*self._amo_logo_image_locator).get_attribute('src')

    @property
    def is_mozilla_logo_visible(self):
        return self.is_element_visible(*self._mozilla_logo_link_locator)

    def click_mozilla_logo(self):
        self.selenium.find_element(*self._mozilla_logo_link_locator).click()

    @property
    def current_page(self):
        return int(self.selenium.find_element(*self._current_page_locator).text)

    def credentials_of_user(self, user):
        return self.parse_yaml_file(self.credentials)[user]

    @property
    def header(self):
        return Base.HeaderRegion(self.testsetup)

    @property
    def breadcrumbs(self):
        return [self.BreadcrumbsRegion(self.testsetup, element)
                for element in self.selenium.find_elements(*self._breadcrumbs_locator)]

    def _extract_iso_dates(self, date_format, *locator):
        """
        Returns a list of iso formatted date strings extracted from
        the text elements matched by the given xpath_locator and
        original date_format.

        So for example, given the following elements:
          <p>Added May 09, 2010</p>
          <p>Added June 11, 2011</p>

        A call to:
          _extract_iso_dates("//p", "Added %B %d, %Y", 2)

        Returns:
          ['2010-05-09T00:00:00','2011-06-11T00:00:00']

        """
        addon_dates = [element.text for element in self.selenium.find_elements(*locator)]

        iso_dates = [
            datetime.strptime(s, date_format).isoformat()
            for s in addon_dates
        ]
        return iso_dates

    def _extract_integers(self, regex_pattern, *locator):
        """
        Returns a list of integers extracted from the text elements
        matched by the given xpath_locator and regex_pattern.
        """
        addon_numbers = [element.text for element in self.selenium.find_elements(*locator)]

        integer_numbers = [
            int(re.search(regex_pattern, str(x).replace(",", "")).group(1))
            for x in addon_numbers
        ]
        return integer_numbers

    class HeaderRegion(Page):

        #other applications
        _other_applications_locator = (By.ID, "other-apps")

        #Search box
        _search_button_locator = (By.CSS_SELECTOR, ".search-button")
        _search_textbox_locator = (By.NAME, "q")

        #Not LoggedIn
        _login_browser_id_locator = (By.CSS_SELECTOR, "a.browserid-login")
        _register_locator = (By.CSS_SELECTOR, "#aux-nav li.account a:nth-child(1)")

        #LoggedIn
        _account_controller_locator = (By.CSS_SELECTOR, "#aux-nav .account a.user")
        _account_dropdown_locator = (By.CSS_SELECTOR, "#aux-nav .account ul")
        _logout_locator = (By.CSS_SELECTOR, "li.nomenu.logout > a")

        def site_nav(self, lookup):
            from pages.regions.header_menu import HeaderMenu
            return HeaderMenu(self.testsetup, lookup)

        def click_other_application(self, other_app):
            hover_locator = self.selenium.find_element(*self._other_applications_locator)
            app_locator = self.selenium.find_element(By.CSS_SELECTOR,
                                                     "#app-%s > a" % other_app.lower())
            ActionChains(self.selenium).move_to_element(hover_locator).\
                move_to_element(app_locator).\
                click().perform()

        def is_other_application_visible(self, other_app):
            hover_locator = self.selenium.find_element(*self._other_applications_locator)
            app_locator = (By.CSS_SELECTOR, "#app-%s" % other_app.lower())
            ActionChains(self.selenium).move_to_element(hover_locator).perform()
            return self.is_element_visible(*app_locator)

        def search_for(self, search_term):
            search_box = self.selenium.find_element(*self._search_textbox_locator)
            search_box.send_keys(search_term)
            self.selenium.find_element(*self._search_button_locator).click()
            from pages.search import SearchHome
            return SearchHome(self.testsetup)

        @property
        def search_field_placeholder(self):
            return self.selenium.find_element(*self._search_textbox_locator).get_attribute('placeholder')

        def click_login_browser_id(self):
            self.selenium.find_element(*self._login_browser_id_locator).click()
            from pages.user import Login
            return Login(self.testsetup)

        def click_logout(self):
            self.selenium.find_element(*self._logout_locator).click()

        def click_edit_profile(self):
            item_locator = (By.CSS_SELECTOR, " li:nth-child(2) a")
            hover_element = self.selenium.find_element(*self._account_controller_locator)
            click_element = self.selenium.find_element(*self._account_dropdown_locator).find_element(*item_locator)
            ActionChains(self.selenium).move_to_element(hover_element).\
                move_to_element(click_element).\
                click().perform()

            from pages.user import EditProfile
            return EditProfile(self.testsetup)

        def click_view_profile(self):
            item_locator = (By.CSS_SELECTOR, " li:nth-child(1) a")
            hover_element = self.selenium.find_element(*self._account_controller_locator)
            click_element = self.selenium.find_element(*self._account_dropdown_locator).find_element(*item_locator)
            ActionChains(self.selenium).move_to_element(hover_element).\
                move_to_element(click_element).\
                click().perform()

            from pages.user import ViewProfile
            return ViewProfile(self.testsetup)

        def click_my_collections(self):
            item_locator = (By.CSS_SELECTOR, " li:nth-child(3) a")
            hover_element = self.selenium.find_element(*self._account_controller_locator)
            click_element = self.selenium.find_element(*self._account_dropdown_locator).find_element(*item_locator)
            ActionChains(self.selenium).move_to_element(hover_element).\
                move_to_element(click_element).\
                click().perform()

            from pages.user import MyCollections
            return MyCollections(self.testsetup)

        @property
        def is_user_logged_in(self):
            return self.is_element_visible(*self._account_controller_locator)

    class BreadcrumbsRegion(Page):

        _breadcrumb_locator = (By.CSS_SELECTOR, '#breadcrumbs>ol')  # Base locator
        _link_locator = (By.CSS_SELECTOR, ' a')

        def __init__(self, testsetup, element):
            Page.__init__(self, testsetup)
            self._root_element = element

        def click_breadcrumb(self):
            self._root_element.find_element(*self._link_locator).click()

        @property
        def name(self):
            return self._root_element.text

        @property
        def link_value(self):
            return self._root_element.find_element(*self._link_locator).get_attribute('href')

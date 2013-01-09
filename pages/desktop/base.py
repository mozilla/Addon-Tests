#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re

from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait

from pages.page import Page


class Base(Page):

    _amo_logo_locator = (By.CSS_SELECTOR, ".site-title")
    _amo_logo_link_locator = (By.CSS_SELECTOR, ".site-title a")
    _amo_logo_image_locator = (By.CSS_SELECTOR, ".site-title img")

    _mozilla_logo_link_locator = (By.CSS_SELECTOR, "#global-header-tab a")

    _footer_locator = (By.CSS_SELECTOR, "#footer")

    def login(self, method="normal", user="default"):
        from pages.desktop.user import Login

        if method == "normal":
            login = self.header.click_login_normal()
            login.login_user_normal(user)

        elif method == "browserID":
            is_browserid_login_available = self.header.is_browserid_login_available

            if is_browserid_login_available:
                login = self.header.click_login_browser_id()
                login.login_user_browser_id(user)
            else:
                login = self.header.click_login_normal()
                login.login_user_normal(user)

    @property
    def page_title(self):
        WebDriverWait(self.selenium, self.timeout).until(lambda s: self.selenium.title)
        return self.selenium.title

    @property
    def is_amo_logo_visible(self):
        return self.is_element_visible(*self._amo_logo_locator)

    def click_amo_logo(self):
        self.selenium.find_element(*self._amo_logo_locator).click()
        from pages.desktop.home import Home
        return Home(self.testsetup)

    @property
    def amo_logo_title(self):
        return self.selenium.find_element(*self._amo_logo_link_locator).get_attribute('title')

    @property
    def amo_logo_text(self):
        return self.selenium.find_element(*self._amo_logo_link_locator).text

    @property
    def amo_logo_image_source(self):
        return self.selenium.find_element(*self._amo_logo_image_locator).get_attribute('src')

    @property
    def is_mozilla_logo_visible(self):
        return self.is_element_visible(*self._mozilla_logo_link_locator)

    def click_mozilla_logo(self):
        self.selenium.find_element(*self._mozilla_logo_link_locator).click()

    def credentials_of_user(self, user):
        return self.parse_yaml_file(self.credentials)[user]

    @property
    def header(self):
        return Base.HeaderRegion(self.testsetup)

    def search_for(self, search_term):
        self.header.search_for(search_term)
        from pages.desktop.collections import Collections, CollectionSearchResultList
        from pages.desktop.personas import Personas, PersonasSearchResultList
        from pages.desktop.themes import Themes, ThemesSearchResultList
        if isinstance(self, (Collections, CollectionSearchResultList)):
            return CollectionSearchResultList(self.testsetup)
        elif isinstance(self, (Personas, PersonasSearchResultList)):
            return PersonasSearchResultList(self.testsetup)
        elif isinstance(self, (Themes, ThemesSearchResultList)):
            return ThemesSearchResultList(self.testsetup)
        else:
            from pages.desktop.search import SearchResultList
            return SearchResultList(self.testsetup)

    @property
    def breadcrumbs(self):
        from pages.desktop.regions.breadcrumbs import Breadcrumbs
        return Breadcrumbs(self.testsetup).breadcrumbs

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
        _other_applications_menu_locator = (By.CSS_SELECTOR, "[class='other-apps']")

        #Search box
        _search_button_locator = (By.CSS_SELECTOR, ".search-button")
        _search_textbox_locator = (By.NAME, "q")

        #Not LoggedIn
        _login_browser_id_locator = (By.CSS_SELECTOR, "a.browserid-login")
        _register_locator = (By.CSS_SELECTOR, "#aux-nav li.account a:nth-child(1)")
        _login_normal_locator = (By.CSS_SELECTOR, "#aux-nav li.account a:nth-child(2)")

        #LoggedIn
        _account_controller_locator = (By.CSS_SELECTOR, "#aux-nav .account a.user")
        _account_dropdown_locator = (By.CSS_SELECTOR, "#aux-nav .account ul")
        _logout_locator = (By.CSS_SELECTOR, "li.nomenu.logout > a")

        _site_navigation_menus_locator = (By.CSS_SELECTOR, "#site-nav > ul > li")
        _site_navigation_min_number_menus = 5

        def site_navigation_menu(self, value):
            #used to access one specific menu
            for menu in self.site_navigation_menus:
                if menu.name == value.upper():
                    return menu
            raise Exception("Menu not found: '%s'. Menus: %s" % (value, [menu.name for menu in self.site_navigation_menus]))

        @property
        def site_navigation_menus(self):
            #returns a list containing all the site navigation menus
            WebDriverWait(self.selenium, self.timeout).until(lambda s: len(s.find_elements(*self._site_navigation_menus_locator)) >= self._site_navigation_min_number_menus)
            from pages.desktop.regions.header_menu import HeaderMenu
            return [HeaderMenu(self.testsetup, web_element) for web_element in self.selenium.find_elements(*self._site_navigation_menus_locator)]

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

        @property
        def search_field_placeholder(self):
            return self.selenium.find_element(*self._search_textbox_locator).get_attribute('placeholder')

        @property
        def is_search_button_visible(self):
            return self.is_element_visible(*self._search_button_locator)

        @property
        def is_search_textbox_visible(self):
            return self.is_element_visible(*self._search_textbox_locator)

        @property
        def search_button_title(self):
            return self.selenium.find_element(*self._search_button_locator).get_attribute('title')

        def click_login_browser_id(self):
            self.selenium.find_element(*self._login_browser_id_locator).click()
            from pages.desktop.user import Login
            return Login(self.testsetup)

        def click_login_normal(self):
            self.selenium.find_element(*self._login_normal_locator).click()
            from pages.desktop.user import Login
            return Login(self.testsetup)

        @property
        def is_browserid_login_available(self):
            return self.is_element_present(*self._login_browser_id_locator)

        @property
        def is_login_link_visible(self):
            return self.is_element_visible(*self._login_normal_locator)

        @property
        def is_register_link_visible(self):
            return self.is_element_visible(*self._register_locator)

        def click_logout(self):
            hover_element = self.selenium.find_element(*self._account_controller_locator)
            click_element = self.selenium.find_element(*self._logout_locator)
            ActionChains(self.selenium).move_to_element(hover_element).\
                move_to_element(click_element).\
                click().perform()

        def click_edit_profile(self):
            item_locator = (By.CSS_SELECTOR, " li:nth-child(2) a")
            hover_element = self.selenium.find_element(*self._account_controller_locator)
            click_element = self.selenium.find_element(*self._account_dropdown_locator).find_element(*item_locator)
            ActionChains(self.selenium).move_to_element(hover_element).\
                move_to_element(click_element).\
                click().perform()

            from pages.desktop.user import EditProfile
            return EditProfile(self.testsetup)

        def click_view_profile(self):
            item_locator = (By.CSS_SELECTOR, " li:nth-child(1) a")
            hover_element = self.selenium.find_element(*self._account_controller_locator)
            click_element = self.selenium.find_element(*self._account_dropdown_locator).find_element(*item_locator)
            ActionChains(self.selenium).move_to_element(hover_element).\
                move_to_element(click_element).\
                click().perform()

            from pages.desktop.user import ViewProfile
            view_profile_page = ViewProfile(self.testsetup)
            # Force a wait for the view_profile_page
            view_profile_page.is_the_current_page
            return ViewProfile(self.testsetup)

        def click_my_collections(self):
            item_locator = (By.CSS_SELECTOR, " li:nth-child(3) a")
            hover_element = self.selenium.find_element(*self._account_controller_locator)
            click_element = self.selenium.find_element(*self._account_dropdown_locator).find_element(*item_locator)
            ActionChains(self.selenium).move_to_element(hover_element).\
                move_to_element(click_element).\
                click().perform()

            from pages.desktop.user import MyCollections
            return MyCollections(self.testsetup)

        def click_my_favorites(self):
            item_locator = (By.CSS_SELECTOR, " li:nth-child(4) a")
            hover_element = self.selenium.find_element(*self._account_controller_locator)
            click_element = self.selenium.find_element(*self._account_dropdown_locator).find_element(*item_locator)

            # this method is flakey, it sometimes does not actually click
            ActionChains(self.selenium).move_to_element(hover_element).\
                move_to_element(click_element).\
                click().perform()

            from pages.desktop.user import MyFavorites
            return MyFavorites(self.testsetup)

        @property
        def is_my_favorites_menu_present(self):
            hover_element = self.selenium.find_element(*self._account_controller_locator)

            ActionChains(self.selenium).move_to_element(hover_element).perform()
            menu_text = self.selenium.find_element(*self._account_dropdown_locator).text

            if not 'My Profile' in menu_text:
                print "ActionChains is being flakey again"
            return 'My Favorites' in menu_text

        @property
        def is_user_logged_in(self):
            return self.is_element_visible(*self._account_controller_locator)

        @property
        def menu_name(self):
            return self.selenium.find_element(*self._other_applications_locator).text

        def hover_over_other_apps_menu(self):
            hover_element = self.selenium.find_element(*self._other_applications_locator)
            ActionChains(self.selenium).\
                move_to_element(hover_element).\
                perform()

        @property
        def is_other_apps_dropdown_menu_visible(self):
            return self.selenium.find_element(*self._other_applications_menu_locator).is_displayed()

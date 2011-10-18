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

from page import Page
from datetime import datetime


class Base(Page):

    _next_link_locator = "css=.paginator .rel > a:nth(2)"
    _previous_link_locator = "css=.paginator .rel > a:nth(1)"
    _current_page_locator = "css=.paginator .num > a:nth(0)"
    _last_page_link_locator = "css=.paginator .rel > a:nth(3)"
    _first_page_link_locator = "css=.paginator .rel > a:nth(0)"
    _results_displayed_text_locator = "css=.paginator .pos"


    _amo_logo_link_locator = "css=.site-title a"
    _amo_logo_image_locator = "css=.site-title img"

    _mozilla_logo_link_locator = "css=#global-header-tab a"

    _breadcrumbs_locator = "css=#breadcrumbs>ol>li"

    def login (self, user="default"):
        login = self.header.click_login()
        login.login_user(user)

    @property
    def page_title(self):
        return self.selenium.get_title()

    @property
    def amo_logo_title(self):
        return self.selenium.get_attribute("%s@title" % self._amo_logo_link_locator)

    @property
    def is_amo_logo_visible(self):
        return self.selenium.is_visible(self._amo_logo_link_locator)

    @property
    def amo_logo_image_source(self):
        return self.selenium.get_attribute("%s@src" % self._amo_logo_image_locator)

    @property
    def is_amo_logo_image_visible(self):
        return self.selenium.is_visible(self._amo_logo_image_locator)

    @property
    def is_mozilla_logo_visible(self):
        return self.selenium.is_visible(self._mozilla_logo_link_locator)

    def click_mozilla_logo(self):
        self.selenium.click(self._mozilla_logo_link_locator)
        self.selenium.wait_for_page_to_load(self.timeout)

    def page_forward(self):
        self.selenium.click(self._next_link_locator)
        self.selenium.wait_for_page_to_load(self.timeout)

    def page_back(self):
        self.selenium.click(self._previous_link_locator)
        self.selenium.wait_for_page_to_load(self.timeout)

    @property
    def is_prev_link_disabled(self):
        button = self.selenium.get_attribute(self._previous_link_locator + "%s" % "@class")
        return ("disabled" in button)

    @property
    def is_prev_link_visible(self):
        return self.selenium.is_visible(self._previous_link_locator)

    @property
    def is_next_link_disabled(self):
        button = self.selenium.get_attribute(self._next_link_locator + "%s" % "@class")
        return ("disabled" in button)

    @property
    def is_next_link_visible(self):
        return self.selenium.is_visible(self._next_link_locator)

    @property
    def current_page(self):
        return int(self.selenium.get_text(self._current_page_locator))

    @property
    def results_displayed(self):
        return self.selenium.get_text(self._results_displayed_text_locator)

    def go_to_last_page(self):
        self.selenium.click(self._last_page_link_locator)
        self.selenium.wait_for_page_to_load(self.timeout)

    def go_to_first_page(self):
        self.selenium.click(self._first_page_link_locator)
        self.selenium.wait_for_page_to_load(self.timeout)

    def credentials_of_user(self, user):
        return self.parse_yaml_file(self.credentials)[user]

    @property
    def header(self):
        return Base.HeaderRegion(self.testsetup)

    @property
    def breadcrumb_name(self):
        return self.selenium.get_text("%s > span" % self._breadcrumbs_locator)

    @property
    def breadcrumbs(self):
        return [self.BreadcrumbsRegion(self.testsetup, i) for i in range(self.breadcrumbs_count)]

    @property
    def breadcrumbs_count(self):
        return self.selenium.get_css_count(self._breadcrumbs_locator)

    @property
    def is_breadcrumb_menu_visible(self):
        return self.selenium.is_visible(self._breadcrumbs_locator)

    def _extract_iso_dates(self, xpath_locator, date_format, count):
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
        addon_dates = [
            self.selenium.get_text("xpath=(%s)[%d]" % (xpath_locator, i))
            for i in xrange(1, count + 1)
        ]
        iso_dates = [
            datetime.strptime(s, date_format).isoformat()
            for s in addon_dates
        ]
        return iso_dates

    def _extract_integers(self, xpath_locator, regex_pattern, count):
        """
        Returns a list of integers extracted from the text elements
        matched by the given xpath_locator and regex_pattern.
        """
        addon_numbers = [
            self.selenium.get_text("xpath=(%s)[%d]" % (xpath_locator, i))
            for i in xrange(1, count + 1)
        ]
        integer_numbers = [
            int(re.search(regex_pattern, str(x).replace(",", "")).group(1))
            for x in addon_numbers
        ]
        return integer_numbers

    class HeaderRegion(Page):

        #other applications
        _other_applications_locator = "id=other-apps"
        _other_apps_list_locator = "css=ul.other-apps"
        _app_thunderbird = "css=#app-thunderbird a"

        #Search box
        _search_button_locator = "css=.search-button"
        _search_textbox_locator = "name=q"

        #Not LogedIn
        _login_locator = "css=#aux-nav li.account a:nth(1)"
        _register_locator = "css=#aux-nav li.account a:nth(0)"

        #LogedIn
        _account_controller_locator = 'css=#aux-nav .account .user'
        _account_dropdown_locator = "css=#aux-nav .account ul"
        _logout_locator = 'css=li.nomenu.logout > a'

        #TODO:hover other apps
        def click_other_applications(self):
            self.selenium.click(self._other_applications_locator)

        def click_thunderbird(self):
            self.selenium.click(self._app_thunderbird)
            self.selenium.wait_for_page_to_load(self.timeout)

        def is_thunderbird_visible(self):
            return self.is_element_present(self._app_thunderbird)

        def search_for(self, search_term):
            self.selenium.type(self._search_textbox_locator, search_term)
            self.selenium.click(self._search_button_locator)
            self.selenium.wait_for_page_to_load(self.timeout)
            from pages.search import SearchHome
            return SearchHome(self.testsetup)

        @property
        def search_field_placeholder(self):
            return self.selenium.get_attribute(self._search_textbox_locator + '@placeholder')

        def click_my_account(self):
            self.selenium.click(self._account_controller_locator)
            self.wait_for_element_visible(self._account_dropdown_locator)

        def click_login(self):
            self.selenium.click(self._login_locator)
            self.selenium.wait_for_page_to_load(self.timeout)
            from pages.user import Login
            return Login(self.testsetup)

        def click_logout(self):
            self.selenium.click(self._logout_locator)
            self.selenium.wait_for_page_to_load(self.timeout)

        def click_edit_profile(self):
            self.click_my_account
            self.selenium.click('%s > li:nth(1) a' % self._account_dropdown_locator)
            self.selenium.wait_for_page_to_load(self.timeout)
            from pages.user import EditProfile
            return EditProfile(self.testsetup)

        def click_view_profile(self):
            self.click_my_account
            self.selenium.click('%s > li:nth(0) a' % self._account_dropdown_locator)
            self.selenium.wait_for_page_to_load(self.timeout)
            from pages.user import ViewProfile
            return ViewProfile(self.testsetup)

        @property
        def is_user_logged_in(self):
            try:
                return self.selenium.is_visible(self._account_controller_locator)
            except:
                return False

        @property
        def other_applications_count(self):
            return int(self.selenium.get_css_count("%s li" % self._other_apps_list_locator))

        @property
        def other_applications(self):
            return [self.OtherApplications(self.testsetup, i) for i in range(self.other_applications_count)]

        class OtherApplications(Page):

            _name_locator = " > a"
            _other_apps_locator = "css=ul.other-apps > li"

            def __init__(self, testsetup, lookup):
                Page.__init__(self, testsetup)
                self.lookup = lookup

            def absolute_locator(self, relative_locator):
                return self.root_locator + relative_locator

            @property
            def root_locator(self):
                if type(self.lookup) == int:
                #   lookup by index
                    return "%s:nth(%s)" % (self._other_apps_locator, self.lookup)
                else:
                    # lookup by name
                    return "%s:contains(%s)" % (self._other_apps_locator, self.lookup)

            @property
            def name(self):
                return self.selenium.get_text(self.absolute_locator(self._name_locator))

            @property
            def is_application_visible(self):
                return self.is_element_present(self.absolute_locator(self._name_locator))

            @property
            def index(self):
                return self.lookup

    class BreadcrumbsRegion(Page):

        _breadcrumb_locator = "css=#breadcrumbs>ol"  # Base locator
        _link_locator = " a"
        _link_value_locator = " a@href"

        def __init__(self, testsetup, lookup):
            Page.__init__(self, testsetup)
            self.lookup = lookup

        def absolute_locator(self, relative_locator=""):
            return "%s>li:nth(%s)%s" % (self._breadcrumb_locator, self.lookup, relative_locator)

        def click(self):
            self.selenium.click(self.absolute_locator(self._link_locator))
            self.selenium.wait_for_page_to_load(self.timeout)

        @property
        def name(self):
            return self.selenium.get_text(self.absolute_locator())

        @property
        def link_value(self):
            return self.selenium.get_attribute(self.absolute_locator(self._link_value_locator))

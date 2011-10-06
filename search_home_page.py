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

from time import strptime, mktime

from base_page import BasePage
from page import Page
import addons_site
import refine_results_region


class SearchHomePage(BasePage):

    _results_summary_locator = "css=h3.results-count"
    _results_displayed_locator = "css=div.num-results"
    _results_locator = "css=div.results-inner div.item"

    _pagination_loctor = "css=div.listing-footer li"
    _next_link_locator = "link=Next"
    _previous_link_locator = "link=Prev"

    _breadcrumbs_locator = "css=ol.breadcrumbs"

    _sort_by_keyword_match_locator = "css=div.listing-header a:contains('Keyword Match')"
    _sort_by_created_locator = "css=div.listing-header a:contains('Created')"
    _sort_by_updated_locator = "css=div.listing-header a:contains('Updated')"
    _sort_by_rating_locator = "css=div.listing-header a:contains('Rating')"
    _sort_by_downloads_locator = "css=div.listing-header a:contains('Downloads')"
    _sort_by_users_locator = "css=div.listing-header a:contains('Users')"

    def page_forward(self):
        self.selenium.click(self._next_link_locator)
        self.selenium.wait_for_page_to_load(self.timeout)

    def page_back(self):
        self.selenium.click(self._previous_link_locator)
        self.selenium.wait_for_page_to_load(self.timeout)

    @property
    def is_forword_present(self):
        return self.is_element_present(self._next_link_locator)

    @property
    def refine_results(self):
        return refine_results_region.RefineResults(self.testsetup)

    @property
    def breadcrumbs_value(self):
        return self.selenium.get_text(self._breadcrumbs_locator)

    @property
    def page_title(self):
        return self.selenium.get_title()

    @property
    def results_summary(self):
        return self.selenium.get_text(self._results_summary_locator)

    @property
    def results_displayed(self):
        return self.selenium.get_text(self._results_displayed_locator)

    @property
    def result_count(self):
        return int(self.selenium.get_css_count(self._results_locator))

    def click_addon(self, addon_name):
        self.selenium.click("link=" + addon_name)
        from details_page import DetailsPage
        return DetailsPage(self.testsetup, addon_name)

    def sort_by(self, type):
        self.selenium.click(getattr(self, '_sort_by_%s_locator' % type))
        self.selenium.wait_for_page_to_load(self.timeout)
        return self

    def result(self, lookup):
        return self.SearchResult(self.testsetup, lookup)

    def results(self):
        return [self.SearchResult(self.testsetup, i) for i in range(self.result_count)]

    def click_last_results_page(self):
        count = self.selenium.get_css_count(self._pagination_loctor)
        if self.selenium.get_text("%s:nth(%s) a" % (self._pagination_loctor, count - 1)) == "Next":
            self.selenium.click("%s:nth(%s) a" % (self._pagination_loctor, count - 2))
            self.selenium.wait_for_page_to_load(self.timeout)

    class SearchResult(Page):
        _name_locator = " h3 a"

        def __init__(self, testsetup, lookup):
            Page.__init__(self, testsetup)
            self.lookup = lookup

        def absolute_locator(self, relative_locator):
            return self.root_locator + relative_locator

        @property
        def root_locator(self):
            if type(self.lookup) == int:
                # lookup by index
                return "css=div.results-inner div.item:nth(%s)" % self.lookup
            else:
                # lookup by name
                return "css=div.results-inner div.item:contains(%s)" % self.lookup

        @property
        def name(self):
            return self.selenium.get_text(self.absolute_locator(self._name_locator))

        def click(self):
            self.selenium.click(self.absolute_locator(self._name_locator))
            self.selenium.wait_for_page_to_load(self.timeout)

        @property
        def downloads(self):
            locator = self.root_locator + ' div.item-info p.downloads strong'
            return int(self.selenium.get_text(locator).replace(',', ''))

        @property
        def users(self):
            """ Alias for self.downloads """
            return self.downloads

        @property
        def rating(self):
            locator = self.root_locator + ' div.item-info p.addon-rating span span'
            return int(self.selenium.get_text(locator))

        @property
        def created_date(self):
            """ Returns created date of result in POSIX format """
            locator = self.root_locator + ' div.item-info p.updated'
            date = self.selenium.get_text(locator).strip().replace('Added ', '')
            # convert to POSIX format
            date = strptime(date, '%B %d, %Y')
            return mktime(date)

        @property
        def updated_date(self):
            """ Returns updated date of result in POSIX format """
            locator = self.root_locator + ' div.item-info p.updated'
            date = self.selenium.get_text(locator).strip().replace('Updated ', '')
            # convert to POSIX format
            date = strptime(date, '%B %d, %Y')
            return mktime(date)

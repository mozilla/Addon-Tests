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

from pages.page import Page
from time import strptime, mktime
from pages.base import Base
from pages.regions.search_filter import FilterBase


class SearchHome(Base):

    _number_of_results_found = 'css=#search-facets > p'

    _no_results_locator = 'css=p.no-results'
    _search_results_title_locator = 'css=section.primary>h1'
    _results_locator = 'css=div.items div.item.addon'

    _sort_by_relevance_locator = "css=#sorter > ul > li > a:contains('Relevance')"
    _sort_by_most_users_locator = "css=#sorter > ul > li > a:contains('Most Users')"
    _sort_by_top_reated_locator = "css=#sorter > ul > li > a:contains('Top Rated')"
    _sort_by_newest_locator = "css=#sorter > ul > li > a:contains('Newest')"

    _sort_by_name_locator = "css=#sorter >ul > li > ul > li > a:contains('Name')"
    _sort_by_weekly_downloads_locator = "css=#sorter >ul > li > ul > li > a:contains('Weekly Downloads')"
    _sort_by_recently_updated_locator = "css=#sorter >ul > li > ul > li > a:contains('Recently Updated')"
    _sort_by_up_and_coming_locator = "css=#sorter >ul > li > ul > li > a:contains('Up & Coming')"

    @property
    def is_no_results_present(self):
        return self.is_element_present(self._no_results_locator)

    @property
    def no_results_text(self):
        return self.selenium.get_text(self._no_results_locator)

    @property
    def number_of_results_text(self):
        return self.selenium.get_text(self._number_of_results_found)

    @property
    def search_results_title(self):
        return self.selenium.get_text(self._search_results_title_locator)

    @property
    def filter(self):
        return FilterBase(self.testsetup)

    @property
    def result_count(self):
        return int(self.selenium.get_css_count(self._results_locator))

    def sort_by(self, type):
        self.selenium.click(getattr(self, '_sort_by_%s_locator' % type.replace(' ', '_').lower()))
        self.selenium.wait_for_page_to_load(self.timeout)
        return self

    def result(self, lookup):
        return self.SearchResult(self.testsetup, lookup)

    def results(self):
        return [self.SearchResult(self.testsetup, i) for i in range(self.result_count)]

    class SearchResult(Page):
        _name_locator = '> div.info > h3 > a'
        _created_date = '> div.info > div.vitals > div.updated'
        _sort_criteria = '> div.info > div.vitals > div.adu'

        def __init__(self, testsetup, lookup):
            Page.__init__(self, testsetup)
            self.lookup = lookup

        def absolute_locator(self, relative_locator):
            return self.root_locator + relative_locator

        @property
        def root_locator(self):
            if type(self.lookup) == int:
                # lookup by index
                return 'css=div.items > div.item.addon:nth(%s) ' % self.lookup
            else:
                # lookup by name
                return 'css=div.items > div.item.addon:contains(%s) ' % self.lookup

        @property
        def name(self):
            return self.selenium.get_text(self.absolute_locator(self._name_locator))

        @property
        def text(self):
            return self.selenium.get_text(self.root_locator)

        @property
        def downloads(self):
            number = self.selenium.get_text(self.absolute_locator(self._sort_criteria))
            return int(number.split()[0].replace(',', ''))

        @property
        def users(self):
            number = self.selenium.get_text(self.absolute_locator(self._sort_criteria))
            return int(number.split()[0].replace(',', ''))

        @property
        def created_date(self):
            """ Returns created date of result in POSIX format """
            date = self.selenium.get_text(self.absolute_locator(self._created_date)).strip().replace('Added ', '')
            # convert to POSIX format
            date = strptime(date, '%B %d, %Y')
            return mktime(date)

        @property
        def updated_date(self):
            """ Returns updated date of result in POSIX format """
            date = self.selenium.get_text(self.absolute_locator(self._created_date)).replace('Updated ', '')
            # convert to POSIX format
            date = strptime(date, '%B %d, %Y')
            return mktime(date)

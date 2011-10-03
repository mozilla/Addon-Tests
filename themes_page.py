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
# Contributor(s): David Burns
#                 Marc George
#                 Dave Hunt <dhunt@mozilla.com>
#                 Alex Rodionov <p0deje@gmail.com>
#                 Joel Andersson <janderssn@gmail.com>
#                 Bebe <florin.strugariu@softvision.ro>
#                 Marlena Compton <mcompton@mozilla.com>
#                 Teodosia Pop <teodosia.pop@softvision.ro>
#                 Alex Lakatos <alex@greensqr.com>
#                 Alin Trif <alin.trif@softvision.ro>
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


from page import Page
from base_page import BasePage


class ThemesPage(BasePage):

    _sort_by_name_locator = 'name=_t-name'
    _sort_by_updated_locator = 'name=_t-updated'
    _sort_by_created_locator = 'name=_t-created'
    _sort_by_popular_locator = 'name=_t-popular'
    _sort_by_rating_locator = 'name=_t-rating'
    _addons_root_locator = " // div[@class = 'details']"
    _addon_name_locator = _addons_root_locator + " / h4 / a"
    _addons_metadata_locator = _addons_root_locator + " / p[@class = 'meta']"
    _addons_rating_locator = _addons_metadata_locator + " / span / span"
    _breadcrumb_locator = "css = ol.breadcrumbs"
    _category_locator = "css = #c-30 > a"
    _addons_root_locator = "//div[@class='details']"
    _addon_name_locator = _addons_root_locator + "/h4/a"
    _addons_metadata_locator = _addons_root_locator + "/p[@class='meta']"
    _addons_rating_locator = _addons_metadata_locator + "/span/span"
    _breadcrumb_locator = "css=ol.breadcrumbs"
    _category_locator = "css=#c-30 > a"
    _categories_locator = "css=.other-categories ul:nth-of-type(2) li"
    _category_link_locator = _categories_locator + ":nth-of-type(%s) a"
    _top_counter_locator = "css=div.primary>header b"
    _bottom_counter_locator = "css=div.num-results > strong:nth(2)"

    # TODO: remove pagination locators when impala pages are available for themes
    _next_link_locator = "link=Next"

    def __init__(self, testsetup):
        BasePage.__init__(self, testsetup)

    # TODO: remove method when impala pages are available for themes
    def page_forward(self):
        self.selenium.click(self._next_link_locator)
        self.selenium.wait_for_page_to_load(self.timeout)

    def click_sort_by(self, type_):
        self.selenium.click(getattr(self, "_sort_by_%s_locator" % type_))
        self.selenium.wait_for_page_to_load(self.timeout)

    def click_on_first_addon(self):
        self.selenium.click(self._addon_name_locator)
        self.selenium.wait_for_page_to_load(self.timeout)
        return ThemePage(self.testsetup)

    def click_on_first_category(self):
        self.selenium.click(self._category_locator)
        self.selenium.wait_for_page_to_load(self.timeout)
        return ThemesCategoryPage(self.testsetup)

    def get_category(self, lookup):
        return self.selenium.get_text(self._category_link_locator % lookup)

    @property
    def page_title(self):
        return self.selenium.get_title()

    @property
    def themes_breadcrumb(self):
        return self.selenium.get_text(self._breadcrumb_locator)

    @property
    def themes_category(self):
        return self.selenium.get_text(self._category_locator)

    @property
    def categories_count(self):
        return self.selenium.get_css_count(self._categories_locator)

    @property
    def addon_names(self):
        addon_count = int(self.selenium.get_xpath_count(self._addon_name_locator))
        _addon_names = [self.selenium.get_text("xpath=(" + self._addon_name_locator + ")[%s]" % str(i + 1))
                        for i in xrange(addon_count)]
        return _addon_names

    @property
    def addon_count(self):
        count = self.selenium.get_xpath_count(self._addon_name_locator)
        return int(count)

    @property
    def addon_updated_dates(self):
        count = self.addon_count
        return self._extract_iso_dates(self._addons_metadata_locator, "Updated %B %d, %Y", count)

    @property
    def addon_created_dates(self):
        count = self.addon_count
        return self._extract_iso_dates(self._addons_metadata_locator, "Added %B %d, %Y", count)

    @property
    def addon_download_number(self):
        pattern = "(\d+(?:[,]\d+)*) weekly downloads"
        downloads_locator = self._addons_metadata_locator
        downloads = self._extract_integers(downloads_locator, pattern, self.addon_count)
        return downloads

    @property
    def addon_rating(self):
        pattern = "(\d)"
        ratings_locator = self._addons_rating_locator
        ratings = self._extract_integers(ratings_locator, pattern, self.addon_count)
        return ratings

    @property
    def top_counter(self):
        return self.selenium.get_text(self._top_counter_locator)

    @property
    def bottom_counter(self):
        return self.selenium.get_text(self._bottom_counter_locator)


class ThemePage(BasePage):

    _addon_title = "css=h1.addon"

    @property
    def addon_title(self):
        return self.selenium.get_text(self._addon_title)


class ThemesCategoryPage(BasePage):

    _title_locator = "css=h2"
    _breadcrumb_locator = "css=ol.breadcrumbs"

    @property
    def title(self):
        return self.selenium.get_text(self._title_locator)

    @property
    def breadcrumb(self):
        return self.selenium.get_text(self._breadcrumb_locator)

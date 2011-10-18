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
#                 David Burns
#                 Marc George
#                 Dave Hunt <dhunt@mozilla.com>
#                 Alex Rodionov <p0deje@gmail.com>
#                 Joel Andersson <janderssn@gmail.com>
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


from base_page import BasePage
import re


class PersonasPage(BasePage):

    _page_title = "Personas :: Add-ons for Firefox"
    _personas_locator = "//div[@class='persona persona-small']"
    _start_exploring_locator = "css=#featured-addons.personas-home a.more-info"
    _featured_addons_locator = "css=#featured-addons.personas-home"
    _featured_personas_locator = "css=.personas-featured .persona.persona-small"
    _addons_column_locator = '//div[@class="addons-column"]'

    _persona_header_locator = "css=.featured-inner>h2"

    def __init__(self, testsetup):
        BasePage.__init__(self, testsetup)

    @property
    def persona_count(self):
        """ Returns the total number of persona links in the page. """
        return self.selenium.get_xpath_count(self._personas_locator)

    def click_persona(self, index):
        """ Clicks on the persona with the given index in the page. """
        self.selenium.click("xpath=(%s)[%d]//a" % (self._personas_locator, index))
        self.selenium.wait_for_page_to_load(self.timeout)
        return PersonasDetailPage(self.testsetup)

    def open_persona_detail_page(self, persona_key):
        self.selenium.open("%s/addon/%s" % (self.site_version, persona_key))
        self.selenium.wait_for_page_to_load(self.timeout)
        return PersonasDetailPage(self.testsetup)

    @property
    def is_featured_addons_present(self):
        return self.selenium.get_css_count(self._featured_addons_locator) > 0

    def click_start_exploring(self):
        self.selenium.click(self._start_exploring_locator)
        self.selenium.wait_for_page_to_load(self.timeout)
        return PersonasBrowsePage(self.testsetup)

    @property
    def featured_personas_count(self):
        return self.selenium.get_css_count(self._featured_personas_locator)

    def _persona_in_column_locator(self, column_index):
        """ Returns a locator for personas in the column with the given index. """
        return "%s[%d]%s" % (self._addons_column_locator, column_index, self._personas_locator)

    @property
    def recently_added_count(self):
        locator = self._persona_in_column_locator(1)
        return self.selenium.get_xpath_count(locator)

    @property
    def recently_added_dates(self):
        locator = self._persona_in_column_locator(1)
        iso_dates = self._extract_iso_dates(locator, "Added %B %d, %Y", self.recently_added_count)
        return iso_dates

    @property
    def most_popular_count(self):
        locator = self._persona_in_column_locator(2)
        return self.selenium.get_xpath_count(locator)

    @property
    def most_popular_downloads(self):
        locator = self._persona_in_column_locator(2)
        pattern = "(\d+(?:[,]\d+)*)\s+users"
        return self._extract_integers(locator, pattern, self.most_popular_count)

    @property
    def top_rated_count(self):
        locator = self._persona_in_column_locator(3)
        return self.selenium.get_xpath_count(locator)

    @property
    def top_rated_ratings(self):
        locator = self._persona_in_column_locator(3)
        pattern = "Rated\s+(\d)\s+.*"
        return self._extract_integers(locator, pattern, self.top_rated_count)

    @property
    def persona_header(self):
        return self.selenium.get_text(self._persona_header_locator)


class PersonasDetailPage(BasePage):

    _page_title_regex = '.+ :: Add-ons for Firefox'
    _personas_title_locator = 'css=h2.addon'
    _breadcrumb_locator = '//ol[@class="breadcrumbs"]'
    _breadcrumb_item_index_locator = '/li[%s]//'
    _breadcrumb_item_text_locator = '/li//*[text()="%s"]'

    def __init__(self, testsetup):
        BasePage.__init__(self, testsetup)

    @property
    def is_the_current_page(self):
        # This overrides the method in the Page super class.
        if not (re.match(self._page_title_regex, self.selenium.get_title())):
            self.record_error()
            raise Exception('Expected the current page to be the personas detail page.')
        return True

    @property
    def personas_title(self):
        """ Returns the title of the currently displayed persona. """
        return self.selenium.get_text(self._personas_title_locator)

    def get_breadcrumb_item_locator(self, item):
        """ Returns an xpath locator for the given item.
            If item is an int, the item with the given index (1..N) will be located.
            If item is a str, the item with the given link text will be located.
        """
        if isinstance(item, int):
            return (self._breadcrumb_locator + self._breadcrumb_item_index_locator) % str(item)
        elif isinstance(item, str):
            return (self._breadcrumb_locator + self._breadcrumb_item_text_locator) % str(item)

    def get_breadcrumb_item_text(self, item):
        """ Returns the label of the given item in the breadcrumb menu. """
        locator = self.get_breadcrumb_item_locator(item) + 'text()'
        return self.selenium.get_text(locator)

    def get_breadcrumb_item_href(self, item):
        """ Returns the value of the href attribute for the given item in the breadcrumb menu. """
        locator = self.get_breadcrumb_item_locator(item) + '@href'
        return self.selenium.get_attribute(locator)

    def click_breadcrumb_item(self, item):
        """ Clicks on the given item in the breadcrumb menu. """
        locator = self.get_breadcrumb_item_locator(item)
        self.selenium.click(locator)
        self.selenium.wait_for_page_to_load(self.timeout)


class PersonasBrowsePage(BasePage):
    """
    The personas browse page allows browsing the personas according to
    some sort criteria (eg. top rated or most downloaded).

    """

    _selected_sort_by_locator = "css=#addon-list-options li.selected a"
    _personas_grid_locator = "css=.featured.listing ul.personas-grid"

    def __init__(self, testsetup):
        BasePage.__init__(self, testsetup)

    @property
    def sort_key(self):
        """ Returns the current value of the sort request parameter. """
        url = self.get_url_current_page()
        return re.search("[/][?]sort=(.+)[&]?", url).group(1)

    @property
    def sort_by(self):
        """ Returns the label of the currently selected sort option. """
        return self.selenium.get_text(self._selected_sort_by_locator)

    @property
    def is_the_current_page(self):
        # This overrides the method in the Page super class.
        if not (self.is_element_present(self._personas_grid_locator)):
            self.record_error()
            raise Exception('Expected the current page to be the personas browse page.')
        return True

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

from addons_base_page import AddonsBasePage
from datetime import datetime
import re

class AddonsHomePage(AddonsBasePage):

    _page_title = "Add-ons for Firefox"

    _themes_link_locator = "css=#themes > a"
    _personas_link_locator = "css=#personas > a"
    _collections_link_locator = "css=#collections > a"
    _first_addon_locator = "css=div.summary > a > h3"

    #Most Popular List
    _most_popular_list_locator = "css=#homepage > .secondary"
    _most_popular_item_locator = "css=ol.toplist li"
    _most_popular_list_heading_locator = _most_popular_list_locator + " h2"

    _featured_personas_see_all_link = "css=#featured-personas h2 a"
    _featured_personas_locator = "id=featured-personas"
    _featured_personas_title_locator = "css=#featured-personas h2"
    _featured_personas_items_locator = "css=#featured-personas li"

    def __init__(self, testsetup):
        ''' Creates a new instance of the class and gets the page ready for testing '''
        AddonsBasePage.__init__(self, testsetup)
        self.selenium.open("%s/" % self.site_version)
        self.selenium.window_maximize()

    def click_featured_personas_see_all_link(self):
        self.selenium.click(self._featured_personas_see_all_link)
        self.selenium.wait_for_page_to_load(self.timeout)
        from addons_site import AddonsPersonasPage
        return AddonsPersonasPage(self.testsetup)

    def click_personas(self):
        self.selenium.click(self._personas_link_locator)
        self.selenium.wait_for_page_to_load(self.timeout)
        from addons_site import AddonsPersonasPage
        return AddonsPersonasPage(self.testsetup)

    def click_themes(self):
        self.wait_for_element_visible(self._themes_link_locator)
        self.selenium.click(self._themes_link_locator)
        self.selenium.wait_for_page_to_load(self.timeout)
        from addons_site import AddonsThemesPage
        return AddonsThemesPage(self.testsetup)

    def click_collections(self):
        self.selenium.click(self._collections_link_locator)
        self.selenium.wait_for_page_to_load(self.timeout)
        from addons_collection_page import AddonsCollectionsPage
        return AddonsCollectionsPage(self.testsetup)

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

    @property
    def most_popular_count(self):
        return self.selenium.get_css_count(self._most_popular_item_locator)

    @property
    def is_most_popular_list_visible(self):
        return self.selenium.is_visible(self._most_popular_list_locator)

    @property
    def most_popular_list_heading(self):
        return self.selenium.get_text(self._most_popular_list_heading_locator)

    @property
    def is_featured_personas_visible(self):
        return self.selenium.is_visible(self._featured_personas_locator)

    @property
    def featured_personas_count(self):
        return self.selenium.get_css_count(self._featured_personas_items_locator)

    @property
    def fetaured_personas_title(self):
        return self.selenium.get_text(self._featured_personas_title_locator)

    def click_on_first_addon(self):
        self.selenium.click(self._first_addon_locator)
        self.selenium.wait_for_page_to_load(self.timeout)
        from addons_site import AddonsDetailsPage
        return AddonsDetailsPage(self.testsetup)


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
#                 Alex Lakatos <alex@greensqr.com>
#                 Teodosia Pop <teodosia.pop@softvision.ro>
#                 Alin Trif <alin.trif@softvision.ro>
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

from unittestzero import Assert
from homepage import HomePage
import pytest


class TestHomePage:

    def test_that_checks_the_most_popular_section_exists(self, mozwebqa):
        """
        Litmus 25807
        https://litmus.mozilla.org/show_test.cgi?id=25807
        """
        home_page = HomePage(mozwebqa)
        Assert.true(home_page.is_most_popular_list_visible)
        Assert.contains('Most Popular', home_page.most_popular_list_heading)
        Assert.equal(home_page.most_popular_count, 10)

    def test_that_checks_the_tooltip_for_amo_logo(self, mozwebqa):
        """
        Litmus 22924
        https://litmus.mozilla.org/show_test.cgi?id=22924
        """
        home_page = HomePage(mozwebqa)
        Assert.true(home_page.is_amo_logo_visible)
        Assert.equal(home_page.amo_logo_title, "Return to the Firefox Add-ons homepage")

    def test_that_checks_the_image_for_amo_logo(self, mozwebqa):
        """
        Litmus 25742
        https://litmus.mozilla.org/show_test.cgi?id=25742
        """
        home_page = HomePage(mozwebqa)
        Assert.true(home_page.is_amo_logo_image_visible)
        Assert.contains("-cdn.allizom.org/media/img/app-icons/med/firefox.png", home_page.amo_logo_image_source)

    def test_that_clicking_mozilla_logo_loads_mozilla_dot_org(self, mozwebqa):
        """
        Litmus 22922
        https://litmus.mozilla.org/show_test.cgi?id=22922
        """
        home_page = HomePage(mozwebqa)
        Assert.true(home_page.is_mozilla_logo_visible)
        home_page.click_mozilla_logo()
        Assert.equal(home_page.get_url_current_page(), "http://www.mozilla.org/")

    def test_that_clicking_on_addon_name_loads_details_page(self, mozwebqa):
        """ Litmus 25812
            https://litmus.mozilla.org/show_test.cgi?id=25812"""
        home_page = HomePage(mozwebqa)
        details_page = home_page.click_on_first_addon()
        Assert.true(details_page.is_the_current_page)

    def test_that_featured_personas_exist_on_the_homepage(self, mozwebqa):
        """
        Litmus29698
        https://litmus.mozilla.org/show_test.cgi?id=29698
        """
        home_page = HomePage(mozwebqa)

        Assert.true(home_page.is_featured_personas_visible, "Featured Personas region is not visible")
        Assert.equal(home_page.fetaured_personas_title, u"Featured Personas See all \xbb", "Featured Personas region title doesn't match")

        Assert.equal(home_page.featured_personas_count, 6)

    def test_that_clicking_see_all_personas_link_works(self, mozwebqa):
        """
        Litmus 29699
        https://litmus.mozilla.org/show_test.cgi?id=29699
        """
        home_page = HomePage(mozwebqa)
        featured_persona_page = home_page.click_featured_personas_see_all_link()

        Assert.true(featured_persona_page.is_the_current_page)
        Assert.equal(featured_persona_page.persona_header, 'Personas')

    def test_that_other_applications_link_has_tooltip(self, mozwebqa):
        """ Litmus 22925
            https://litmus.mozilla.org/show_test.cgi?id=22925 """
        home_page = HomePage(mozwebqa)
        tooltip = home_page.get_title_of_link('Other applications')
        Assert.equal(tooltip, 'Find add-ons for other applications')

    def test_that_extensions_link_loads_extensions_page(self, mozwebqa):
        """
        Litmus 25746
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=25746
        """
        home_page = HomePage(mozwebqa)
        extensions_page = home_page.click_extensions()
        Assert.true(extensions_page.is_the_current_page)

    def test_that_most_popular_section_is_ordered_by_users(self, mozwebqa):
        """
        Litmus 25808
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=25808
        """
        home_page = HomePage(mozwebqa)
        Assert.true(home_page.is_most_popular_list_visible)
        most_popular_items = home_page.most_popular_items
        Assert.is_sorted_descending([i.users_number for i in most_popular_items])

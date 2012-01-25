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

import pytest

from unittestzero import Assert

from pages.home import Home

xfail = pytest.mark.xfail
nondestructive = pytest.mark.nondestructive


class TestHome:

    expected_header_menus = {
                "EXTENSIONS":       ["Featured", "Most Popular", "Top Rated", "Alerts & Updates", "Appearance", "Bookmarks",
                                     "Download Management", "Feeds, News & Blogging", "Games & Entertainment",
                                     "Language Support", "Photos, Music & Videos", "Privacy & Security", "Shopping",
                                     "Social & Communication", "Tabs", "Web Development", "Other"],
                "PERSONAS":         ["Most Popular", "Top Rated", "Newest", "Abstract", "Causes", "Fashion", "Film and TV",
                                     "Firefox", "Foxkeh", "Holiday", "Music", "Nature", "Other", "Scenery", "Seasonal", "Solid", "Sports", "Websites"],
                "THEMES":           ["Most Popular", "Top Rated", "Newest", "Animals", "Compact", "Large", "Miscellaneous", "Modern", "Nature",
                                     "OS Integration", "Retro", "Sports"],
                "COLLECTIONS":      ["Featured", "Most Followers", "Newest", "Collections I've Made", "Collections I'm Following",
                                     "My Favorite Add-ons"],
                u"MORE\u2026":      ["Add-ons for Mobile", "Dictionaries & Language Packs", "Search Tools", "Developer Hub"]
                }

    @nondestructive
    def test_that_checks_the_most_popular_section_exists(self, mozwebqa):
        """
        Litmus 25807
        https://litmus.mozilla.org/show_test.cgi?id=25807
        """
        home_page = Home(mozwebqa)
        Assert.contains('MOST POPULAR', home_page.most_popular_list_heading)
        Assert.equal(home_page.most_popular_count, 10)

    @nondestructive
    def test_that_clicking_on_addon_name_loads_details_page(self, mozwebqa):
        """ Litmus 25812
            https://litmus.mozilla.org/show_test.cgi?id=25812"""
        home_page = Home(mozwebqa)
        details_page = home_page.click_on_first_addon()
        Assert.true(details_page.is_the_current_page)

    @nondestructive
    def test_that_featured_personas_exist_on_the_home(self, mozwebqa):
        """
        Litmus29698
        https://litmus.mozilla.org/show_test.cgi?id=29698
        """
        home_page = Home(mozwebqa)
        Assert.equal(home_page.featured_personas_title, u'Featured Personas See all \xbb', 'Featured Personas region title doesn\'t match')
        Assert.equal(home_page.featured_personas_count, 6)

    @nondestructive
    def test_that_clicking_see_all_personas_link_works(self, mozwebqa):
        """
        Litmus 29699
        https://litmus.mozilla.org/show_test.cgi?id=29699
        """
        home_page = Home(mozwebqa)
        featured_persona_page = home_page.click_featured_personas_see_all_link()

        Assert.true(featured_persona_page.is_the_current_page)
        Assert.equal(featured_persona_page.persona_header, 'Personas')

    @nondestructive
    def test_that_extensions_link_loads_extensions_page(self, mozwebqa):
        """
        Litmus 25746
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=25746
        """
        home_page = Home(mozwebqa)
        extensions_page = home_page.click_extensions()
        Assert.true(extensions_page.is_the_current_page)

    @nondestructive
    def test_that_most_popular_section_is_ordered_by_users(self, mozwebqa):
        """
        Litmus 25808
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=25808
        """
        home_page = Home(mozwebqa)

        most_popular_items = home_page.most_popular_items
        Assert.is_sorted_descending([i.users_number for i in most_popular_items])

    @nondestructive
    def test_that_featured_collections_exist_on_the_home(self, mozwebqa):
        """
        Litmus 25805
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=25805
        """
        home_page = Home(mozwebqa)
        Assert.equal(home_page.featured_collections_title, u'Featured Collections See all \xbb', 'Featured Collection region title doesn\'t match')
        Assert.equal(home_page.featured_collections_count, 4)

    @nondestructive
    def test_that_clicking_see_all_collections_link_works(self, mozwebqa):
        """
        Litmus 25806
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=25806
        """
        home_page = Home(mozwebqa)
        featured_collection_page = home_page.click_featured_collections_see_all_link()
        Assert.true(featured_collection_page.is_the_current_page)
        Assert.true(featured_collection_page.get_url_current_page().endswith('/collections/?sort=featured'))

    @nondestructive
    def test_that_clicking_top_rated_shows_addons_sorted_by_rating(self, mozwebqa):
        """
        Litmus 25791
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=25791
        """
        home_page = Home(mozwebqa)
        extensions_page = home_page.click_to_explore('top_rated')

        Assert.contains('sort=rating', extensions_page.get_url_current_page())
        Assert.equal('Top Rated', extensions_page.default_selected_tab)

    @nondestructive
    def test_that_clicking_most_popular_shows_addons_sorted_by_users(self, mozwebqa):
        """
        Litmus 25790
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=25790
        """
        home_page = Home(mozwebqa)
        extensions_page = home_page.click_to_explore('popular')

        Assert.contains('sort=users', extensions_page.get_url_current_page())
        Assert.equal('Most Users', extensions_page.default_selected_tab)

    @nondestructive
    def test_that_clicking_featured_shows_addons_sorted_by_featured(self, mozwebqa):
        """
        Litmus 25790
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=25790
        """
        home_page = Home(mozwebqa)
        extensions_page = home_page.click_to_explore('featured')

        Assert.contains('sort=featured', extensions_page.get_url_current_page())
        Assert.equal('Featured', extensions_page.default_selected_tab)

    @nondestructive
    @pytest.mark.litmus([25744, 25745, 25747, 25749, 25751, 25754, 25756, 25758, 25760, 25763, 25764])
    def test_header_menus_and_items_are_correct(self, mozwebqa):
        home_page = Home(mozwebqa)
        actual_header_menus = home_page.header.site_nav
        Assert.equal(sorted(self.expected_header_menus.keys()), sorted([menu.name for menu in actual_header_menus]))

        for menu in actual_header_menus:
            Assert.equal(self.expected_header_menus[menu.name], [item.name for item in menu.items])

    @nondestructive
    @pytest.mark.litmus([25747, 25751, 25756, 25760, 25764])
    def test_top_three_menu_items_are_featured(self, mozwebqa):
        home_page = Home(mozwebqa)
        actual_header_menus = home_page.header.site_nav
        for menu in actual_header_menus:
            if menu.name == u"MORE\u2026":
                [Assert.false(item.is_featured, 'Item %s from menu %s is fetured' % (item.name, menu.name)) for item in menu.items]
            else:
                [Assert.true(item.is_featured, 'Item %s from menu %s is not fetured' % (item.name, menu.name)) for item in menu.items[:3]]
                [Assert.false(item.is_featured, 'Item %s from menu %s is fetured' % (item.name, menu.name)) for item in menu.items[3:]]

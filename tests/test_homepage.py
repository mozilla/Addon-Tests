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

nondestructive = pytest.mark.nondestructive


class TestHome:

    header_menu_values_list = {
                "Extensions":       ["Featured", "Most Popular", "Top Rated", "Alerts & Updates", "Appearance", "Bookmarks",
                                     "Download Management", "Feeds, News & Blogging", "Games & Entertainment",
                                     "Language Support", "Photos, Music & Videos", "Privacy & Security", "Shopping",
                                     "Social & Communication", "Tabs", "Web Development", "Other"],
                "Personas":         ["Most Popular", "Top Rated", "Newest", "Abstract", "Causes", "Fashion", "Film and TV",
                                     "Firefox", "Foxkeh", "Holiday", "Music", "Nature", "Other", "Scenery", "Seasonal", "Solid", "Sports", "Websites"],
                "Themes":           ["Most Popular", "Top Rated", "Newest", "Animals", "Compact", "Large", "Miscellaneous", "Modern", "Nature",
                                     "OS Integration", "Retro", "Sports"],
                "Collections":      ["Featured", "Most Followers", "Newest", "Collections I've Made", "Collections I'm Following",
                                     "My Favorite Add-ons"],
                u"More\u2026":      ["Add-ons for Mobile", "Dictionaries & Language Packs", "Plugins", "Search Tools", "Developer Hub"]
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
    def test_that_verifies_upper_menu_navigation_items(self, mozwebqa):
        """
        Litmus 25744 =>  25796
        http://bit.ly/pfDkXq
        """

        home_page = Home(mozwebqa)

        for menu in self.header_menu_values_list:
            card_items_list = self.header_menu_values_list[menu]
            menu_nav = home_page.header.site_nav(menu)
            Assert.equal(menu.upper(), menu_nav.name)
            card_items = menu_nav.menu_items
            for i in range(len(card_items_list)):
                Assert.equal(card_items_list[i], card_items[i].name, "Item '%s' is not in the %s menu" % (card_items_list[i], menu_nav.name))

                if i < 3 and menu_nav.name != u'MORE\u2026':
                    Assert.true(card_items[i].is_featured, '%s is not highlighted' % card_items[i].name)
                else:
                    Assert.false(card_items[i].is_featured, '%s is highlighted' % card_items[i].name)

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

#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from unittestzero import Assert

from pages.home import Home

xfail = pytest.mark.xfail
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
                u"More\u2026":      ["Add-ons for Mobile", "Dictionaries & Language Packs", "Search Tools", "Developer Hub"]
                }

    @nondestructive
    def test_that_checks_the_most_popular_section_exists(self, mozwebqa):
        """
        Test for Litmus 25807.
        https://litmus.mozilla.org/show_test.cgi?id=25807
        """
        home_page = Home(mozwebqa)
        Assert.contains('MOST POPULAR', home_page.most_popular_list_heading)
        Assert.equal(home_page.most_popular_count, 10)

    @nondestructive
    def test_that_clicking_on_addon_name_loads_details_page(self, mozwebqa):
        """
        Test for Litmus 25812.
        https://litmus.mozilla.org/show_test.cgi?id=25812
        """
        home_page = Home(mozwebqa)
        details_page = home_page.click_on_first_addon()
        Assert.true(details_page.is_the_current_page)

    @nondestructive
    def test_that_featured_personas_exist_on_the_home(self, mozwebqa):
        """
        Test for Litmus29698.
        https://litmus.mozilla.org/show_test.cgi?id=29698
        """
        home_page = Home(mozwebqa)
        Assert.equal(home_page.featured_personas_title, u'Featured Personas See all \xbb', 'Featured Personas region title doesn\'t match')
        Assert.less_equal(home_page.featured_personas_count, 6)

    @nondestructive
    def test_that_clicking_see_all_personas_link_works(self, mozwebqa):
        """
        Test for Litmus 29699.
        https://litmus.mozilla.org/show_test.cgi?id=29699
        """
        home_page = Home(mozwebqa)
        featured_persona_page = home_page.click_featured_personas_see_all_link()

        Assert.true(featured_persona_page.is_the_current_page)
        Assert.equal(featured_persona_page.persona_header, 'Personas')

    @nondestructive
    def test_that_extensions_link_loads_extensions_page(self, mozwebqa):
        """
        Test for Litmus 25746.
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=25746
        """
        home_page = Home(mozwebqa)
        extensions_page = home_page.header.application_masthead("Extensions").click()
        Assert.true(extensions_page.is_the_current_page)

    @nondestructive
    def test_that_most_popular_section_is_ordered_by_users(self, mozwebqa):
        """
        Test for Litmus 25808.
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=25808
        """
        home_page = Home(mozwebqa)

        most_popular_items = home_page.most_popular_items
        Assert.is_sorted_descending([i.users_number for i in most_popular_items])

    @pytest.mark.native
    @xfail(reason="pivotal tracker task to refactor this test: http://bit.ly/rXtwZk")
    @nondestructive
    def test_that_verifies_upper_menu_navigation_items(self, mozwebqa):
        """
        Test for Litmus 25744 to 25796.
        http://bit.ly/pfDkXq
        """

        home_page = Home(mozwebqa)

        for menu in self.header_menu_values_list:
            card_items_list = self.header_menu_values_list[menu]
            menu_nav = home_page.header.application_masthead(menu)
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
        Test for Litmus 25805.
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=25805
        """
        home_page = Home(mozwebqa)
        Assert.equal(home_page.featured_collections_title, u'Featured Collections See all \xbb', 'Featured Collection region title doesn\'t match')
        Assert.equal(home_page.featured_collections_count, 4)

    @nondestructive
    def test_that_featured_extensions_exist_on_the_home(self, mozwebqa):
        """
        Test for Litmus 25800.
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=25800
        """
        home_page = Home(mozwebqa)
        Assert.equal(home_page.featured_extensions_title, 'Featured Extensions', 'Featured Extensions region title doesn\'t match')
        Assert.equal(home_page.featured_extensions_see_all, u'See all \xbb', 'Featured Extensions region see all link is not correct')
        Assert.equal(home_page.featured_extensions_count, 6)

    @nondestructive
    def test_that_clicking_see_all_collections_link_works(self, mozwebqa):
        """
        Test for Litmus 25806.
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=25806
        """
        home_page = Home(mozwebqa)
        featured_collection_page = home_page.click_featured_collections_see_all_link()
        Assert.true(featured_collection_page.is_the_current_page)
        Assert.true(featured_collection_page.get_url_current_page().endswith('/collections/?sort=featured'))

    @pytest.mark.native
    @nondestructive
    def test_that_items_menu_fly_out_while_hovering(self, mozwebqa):
        """
        Test for Litmus 25754.
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=25754
        """
        #I've adapted the test to check open/closed for all menu items
        home_page = Home(mozwebqa)

        for menu in self.header_menu_values_list:
            menu_item = home_page.header.application_masthead(menu)
            menu_item.hover_over_menu_item()
            Assert.true(menu_item.is_menu_dropdown_visible)
            home_page.hover_over_addons_home_title()
            Assert.false(menu_item.is_menu_dropdown_visible)

    def test_that_clicking_top_rated_shows_addons_sorted_by_rating(self, mozwebqa):
        """
        Test for Litmus 25791.
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=25791
        """
        home_page = Home(mozwebqa)
        extensions_page = home_page.click_to_explore('top_rated')

        Assert.contains('sort=rating', extensions_page.get_url_current_page())
        Assert.equal('Top Rated', extensions_page.default_selected_tab)

    @nondestructive
    def test_that_clicking_most_popular_shows_addons_sorted_by_users(self, mozwebqa):
        """
        Test for Litmus 25790.
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=25790
        """
        home_page = Home(mozwebqa)
        extensions_page = home_page.click_to_explore('popular')

        Assert.contains('sort=users', extensions_page.get_url_current_page())
        Assert.equal('Most Users', extensions_page.default_selected_tab)

    @nondestructive
    def test_that_clicking_featured_shows_addons_sorted_by_featured(self, mozwebqa):
        """
        Test for Litmus 25790.
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=25790
        """
        home_page = Home(mozwebqa)
        extensions_page = home_page.click_to_explore('featured')

        Assert.contains('sort=featured', extensions_page.get_url_current_page())
        Assert.equal('Featured', extensions_page.default_selected_tab)

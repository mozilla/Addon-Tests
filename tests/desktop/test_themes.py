#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from unittestzero import Assert

from pages.desktop.home import Home


class TestThemes:

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_themes_can_be_sorted_by_name(self, mozwebqa):
        """Test for Litmus 11727 and 4839."""
        home_page = Home(mozwebqa)
        themes_page = home_page.header.site_navigation_menu("Themes").click()
        themes_page.click_sort_by("name")
        addons = themes_page.addon_names
        addons_set = set(addons)
        Assert.equal(len(addons), len(addons_set), "There are duplicates in the names")
        addons_orig = addons
        addons.sort()
        [Assert.equal(addons_orig[i], addons[i]) for i in xrange(len(addons))]
        themes_page.paginator.click_next_page()
        addons = themes_page.addon_names
        addons_set = set(addons)
        Assert.equal(len(addons), len(addons_set), "There are duplicates in the names")
        addons_orig = addons
        addons.sort()
        [Assert.equal(addons_orig[i], addons[i]) for i in xrange(len(addons))]

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_themes_can_be_sorted_by_updated_date(self, mozwebqa):
        """Test for Litmus 11638."""
        home_page = Home(mozwebqa)
        themes_page = home_page.header.site_navigation_menu("Themes").click()
        themes_page.click_sort_by("recently updated")
        addons = themes_page.addon_names
        addons_set = set(addons)
        Assert.equal(len(addons), len(addons_set), "There are duplicates in the names")
        updated_dates = themes_page.addon_updated_dates
        Assert.is_sorted_descending(updated_dates)
        themes_page.paginator.click_next_page()
        updated_dates.extend(themes_page.addon_updated_dates)
        Assert.is_sorted_descending(updated_dates)

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_themes_can_be_sorted_by_created_date(self, mozwebqa):
        """Test for Litmus 11638."""
        home_page = Home(mozwebqa)
        themes_page = home_page.header.site_navigation_menu("Themes").click()
        themes_page.click_sort_by("newest")
        addons = themes_page.addon_names
        addons_set = set(addons)
        Assert.equal(len(addons), len(addons_set), "There are duplicates in the names")
        created_dates = themes_page.addon_created_dates
        Assert.is_sorted_descending(created_dates)
        themes_page.paginator.click_next_page()
        created_dates.extend(themes_page.addon_created_dates)
        Assert.is_sorted_descending(created_dates)

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_themes_can_be_sorted_by_popularity(self, mozwebqa):
        """Test for Litmus 11638."""
        home_page = Home(mozwebqa)
        themes_page = home_page.header.site_navigation_menu("Themes").click()
        themes_page.click_sort_by("weekly downloads")
        addons = themes_page.addon_names
        addons_set = set(addons)
        Assert.equal(len(addons), len(addons_set), "There are duplicates in the names")
        downloads = themes_page.addon_download_number
        Assert.is_sorted_descending(downloads)
        themes_page.paginator.click_next_page()
        downloads.extend(themes_page.addon_download_number)
        Assert.is_sorted_descending(downloads)

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_themes_loads_themes_landing_page(self, mozwebqa):
        """Test for Litmus 15339."""
        home_page = Home(mozwebqa)
        themes_page = home_page.header.site_navigation_menu("Themes").click()
        url_current_page = themes_page.get_url_current_page()
        Assert.true(url_current_page.endswith("/themes/"))

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_clicking_on_theme_name_loads_its_detail_page(self, mozwebqa):
        """Test for Litmus 15363."""
        home_page = Home(mozwebqa)
        themes_page = home_page.header.site_navigation_menu("Themes").click()
        theme_name = themes_page.addon_name(1)
        theme_page = themes_page.click_on_first_addon()
        Assert.contains(theme_name, theme_page.addon_title)

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_themes_page_has_correct_title(self, mozwebqa):
        """Test for Litmus 15340."""
        home_page = Home(mozwebqa)
        themes_page = home_page.header.site_navigation_menu("Themes").click()
        expected_title = "Most Popular Themes :: Add-ons for Firefox"
        Assert.equal(expected_title, themes_page.page_title)

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_themes_page_breadcrumb(self, mozwebqa):
        """Test for Litmus 15344."""
        home_page = Home(mozwebqa)
        themes_page = home_page.header.site_navigation_menu("Themes").click()
        expected_breadcrumb = "Themes"
        Assert.equal(expected_breadcrumb, themes_page.breadcrumbs[1].text)

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_clicking_on_a_subcategory_loads_expected_page(self, mozwebqa):
        """Test for Litmus 15949."""
        home_page = Home(mozwebqa)
        themes_page = home_page.header.site_navigation_menu("Themes").click()
        selected_category = themes_page.themes_category
        amo_category_page = themes_page.click_on_first_category()
        Assert.equal(selected_category, amo_category_page.title)

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_themes_subcategory_page_breadcrumb(self, mozwebqa):
        home_page = Home(mozwebqa)
        themes_page = home_page.header.site_navigation_menu("Themes").click()
        selected_category = themes_page.themes_category
        amo_category_page = themes_page.click_on_first_category()
        expected_breadcrumbs = ['Add-ons for Firefox', 'Themes', selected_category]

        [Assert.equal(expected_breadcrumbs[i], amo_category_page.breadcrumbs[i].text) for i in range(len(amo_category_page.breadcrumbs))]

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_themes_categories_are_listed_on_left_hand_side(self, mozwebqa):
        """Test for Litmus 15342."""
        home_page = Home(mozwebqa)
        themes_page = home_page.header.site_navigation_menu("Themes").click()
        current_page_url = home_page.get_url_current_page()
        Assert.true(current_page_url.endswith("/themes/"))
        default_categories = ["Animals", "Compact", "Large", "Miscellaneous", "Modern", "Nature", "OS Integration", "Retro", "Sports"]
        Assert.equal(themes_page.categories_count, len(default_categories))
        count = 0
        for category in default_categories:
            count += 1
            current_category = themes_page.get_category(count)
            Assert.equal(category, current_category)

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_themes_categories_are_not_extensions_categories(self, mozwebqa):
        """Test for Litmus 15343."""
        home_page = Home(mozwebqa)
        themes_page = home_page.header.site_navigation_menu("Themes").click()
        themes_categories = themes_page.get_all_categories

        home_page.header.site_navigation_menu("Extensions").click()
        extensions_categories = themes_page.get_all_categories

        Assert.not_equal(len(themes_categories), len(extensions_categories))
        Assert.equal(list(set(themes_categories) & set(extensions_categories)), [])

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_last_themes_page_is_not_empty(self, mozwebqa):
        """
        Test for Litmus 15359.
        https://litmus.mozilla.org/show_test.cgi?id=15359
        """
        home_page = Home(mozwebqa)
        themes_page = home_page.header.site_navigation_menu("Themes").click()
        themes_page.paginator.click_last_page()
        Assert.greater_equal(themes_page.addon_count, 1)

    @pytest.mark.xfail(reason="https://www.pivotaltracker.com/story/show/30542103")
    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_the_displayed_message_for_incompatible_themes(self, mozwebqa):
        """
        Test for Litmus 15361
        https://litmus.mozilla.org/show_test.cgi?id=15361
        """
        home_page = Home(mozwebqa)
        themes_page = home_page.header.site_navigation_menu("Themes").click()

        themes = themes_page.themes

        for theme in themes:
            if theme.is_incompatible:
                Assert.true(theme.is_incompatible_flag_present)
                Assert.contains('Not available',
                             theme.not_compatible_flag_text)
            else:
                Assert.false(theme.is_incompatible_flag_present)

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_most_popular_link_is_default(self, mozwebqa):
        """Test for Litmus 15348"""
        home_page = Home(mozwebqa)
        themes_page = home_page.header.site_navigation_menu("Themes").click()
        url_current_page = themes_page.get_url_current_page()
        Assert.true(url_current_page.endswith("/themes/"))
        Assert.equal(themes_page.selected_explore_filter, 'Most Popular')

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_sorted_by_most_users_is_default(self, mozwebqa):
        """Test for Litmus 15346."""
        home_page = Home(mozwebqa)
        themes_page = home_page.header.site_navigation_menu("Themes").click()
        url_current_page = themes_page.get_url_current_page()
        Assert.true(url_current_page.endswith("/themes/"))
        Assert.equal(themes_page.sorted_by, 'Most Users')

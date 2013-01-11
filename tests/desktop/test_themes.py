#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import random
import pytest

from unittestzero import Assert

from pages.desktop.home import Home


class TestThemes:

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_start_exploring_link_in_the_promo_box(self, mozwebqa):
        """
        Test for Litmus 12037.
        https://litmus.mozilla.org/show_test.cgi?id=12037
        """
        home_page = Home(mozwebqa)
        themes_page = home_page.header.site_navigation_menu("Themes").click()
        Assert.true(themes_page.is_the_current_page)
        Assert.true(themes_page.is_featured_addons_present)
        browse_themes_page = themes_page.click_start_exploring()
        Assert.true(browse_themes_page.is_the_current_page)
        Assert.equal("up-and-coming", browse_themes_page.sort_key)
        Assert.equal("Up & Coming", browse_themes_page.sort_by)

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_page_title_for_themes_landing_page(self, mozwebqa):
        """
        Test for Litmus 15391.
        https://litmus.mozilla.org/show_test.cgi?id=15391
        """
        home_page = Home(mozwebqa)
        themes_page = home_page.header.site_navigation_menu("Themes").click()
        Assert.true(themes_page.is_the_current_page)

    @pytest.mark.native
    @pytest.mark.smoke
    @pytest.mark.nondestructive
    def test_the_featured_themes_section(self, mozwebqa):
        """
        Test for Litmus 15392.
        https://litmus.mozilla.org/show_test.cgi?id=15392
        """
        home_page = Home(mozwebqa)
        themes_page = home_page.header.site_navigation_menu("Themes").click()
        Assert.true(themes_page.is_the_current_page)
        Assert.less_equal(themes_page.featured_themes_count, 6)

    @pytest.mark.native
    @pytest.mark.smoke
    @pytest.mark.nondestructive
    def test_the_recently_added_section(self, mozwebqa):
        """
        Test for Litmus Litmus 15393.
        https://litmus.mozilla.org/show_test.cgi?id=15393
        """
        home_page = Home(mozwebqa)
        themes_page = home_page.header.site_navigation_menu("Themes").click()
        Assert.true(themes_page.is_the_current_page)
        Assert.equal(6, themes_page.recently_added_count)
        recently_added_dates = themes_page.recently_added_dates
        Assert.is_sorted_descending(recently_added_dates)

    @pytest.mark.native
    @pytest.mark.smoke
    @pytest.mark.nondestructive
    def test_the_most_popular_section(self, mozwebqa):
        """
        Test for Litmus 15394.
        https://litmus.mozilla.org/show_test.cgi?id=15394
        """
        home_page = Home(mozwebqa)
        themes_page = home_page.header.site_navigation_menu("Themes").click()
        Assert.true(themes_page.is_the_current_page)
        Assert.equal(6, themes_page.most_popular_count)
        downloads = themes_page.most_popular_downloads
        Assert.is_sorted_descending(downloads)

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_the_top_rated_section(self, mozwebqa):
        """
        Test for Litmus 15395.
        https://litmus.mozilla.org/show_test.cgi?id=15395
        """
        home_page = Home(mozwebqa)
        themes_page = home_page.header.site_navigation_menu("Themes").click()
        Assert.true(themes_page.is_the_current_page)
        Assert.equal(6, themes_page.top_rated_count)
        ratings = themes_page.top_rated_ratings
        Assert.is_sorted_descending(ratings)

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_breadcrumb_menu_in_theme_details_page(self, mozwebqa):
        """
        Test for Litmus Litmus 12046.
        https://litmus.mozilla.org/show_test.cgi?id=12046
        """

        # Step 1, 2: Access AMO Home, Click on theme category link.
        home_page = Home(mozwebqa)
        themes_page = home_page.header.site_navigation_menu("Themes").click()
        Assert.true(themes_page.is_the_current_page)

        # Step 3: Click on any theme.
        random_theme_index = random.randint(0, themes_page.theme_count - 1)

        themes_detail_page = themes_page.click_theme(random_theme_index)
        Assert.true(themes_detail_page.is_the_current_page)

        # Verify breadcrumb menu format, i.e. Add-ons for Firefox > themes > {theme Name}.
        theme_title = themes_detail_page.title
        Assert.equal("Add-ons for Firefox", themes_detail_page.breadcrumbs[0].text)
        Assert.equal("Themes", themes_detail_page.breadcrumbs[1].text)

        theme_breadcrumb_title = len(theme_title) > 40 and '%s...' % theme_title[:40] or theme_title

        Assert.equal(themes_detail_page.breadcrumbs[2].text, theme_breadcrumb_title)

        # Step 4: Click on the links present in the Breadcrumb menu.
        # Verify that the themes link loads the themes home page.
        themes_detail_page.breadcrumbs[1].click()
        Assert.true(themes_page.is_the_current_page)

        themes_page.return_to_previous_page()
        Assert.true(themes_detail_page.is_the_current_page)

        # Verify that the Add-ons for Firefox link loads the AMO home page.
        themes_detail_page.breadcrumbs[0].click()
        Assert.true(home_page.is_the_current_page)

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_themes_breadcrumb_format(self, mozwebqa):
        """
        Verify the breadcrumb format in themes page
        https://litmus.mozilla.org/show_test.cgi?id=12034
        """
        home_page = Home(mozwebqa)

        themes_page = home_page.header.site_navigation_menu("Themes").click()
        Assert.equal(themes_page.breadcrumbs[0].text, 'Add-ons for Firefox')
        Assert.equal(themes_page.breadcrumbs[1].text, 'Themes')

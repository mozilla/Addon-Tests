#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from unittestzero import Assert
from pages.home import Home

nondestructive = pytest.mark.nondestructive


class TestExtensions:

    @nondestructive
    def test_featured_tab_is_highlighted_by_default(self, mozwebqa):
        """
        Test for Litmus 29706.
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=29706
        """
        home_page = Home(mozwebqa)
        featured_extensions_page = home_page.header.site_navigation_menu("Extensions").click()
        Assert.equal(featured_extensions_page.default_selected_tab, "Featured")

    @pytest.mark.native
    @nondestructive
    def test_next_button_is_disabled_on_the_last_page(self, mozwebqa):
        """
        Test for Litmus 29710.
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=29710
        """
        home_page = Home(mozwebqa)
        featured_extensions_page = home_page.header.site_navigation_menu("Extensions").click()
        featured_extensions_page.sort_by('most_users')
        featured_extensions_page.paginator.click_last_page()

        Assert.true(featured_extensions_page.paginator.is_next_page_disabled, 'Next button is available')

    @pytest.mark.native
    @nondestructive
    def test_that_checks_if_the_extensions_are_sorted_by_newest(self, mozwebqa):
        """
        Test for Litmus 29719
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=29719
        """
        home_page = Home(mozwebqa)
        featured_extensions_page = home_page.header.site_navigation_menu("Extensions").click()
        featured_extensions_page.sort_by('newest')
        Assert.equal(featured_extensions_page.default_selected_tab, "Newest")
        Assert.contains("sort=created", featured_extensions_page.get_url_current_page())

        added_dates = [i.added_date for i in featured_extensions_page.extensions]
        Assert.is_sorted_descending(added_dates)
        featured_extensions_page.paginator.click_next_page()

        added_dates.extend([i.added_date for i in featured_extensions_page.extensions])
        Assert.is_sorted_descending(added_dates)

    @pytest.mark.native
    @nondestructive
    def test_that_checks_if_the_extensions_are_sorted_by_recently_updated(self, mozwebqa):
        """
        Litmus 29727
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=29727
        """
        home_page = Home(mozwebqa)
        featured_extensions_page = home_page.header.site_navigation_menu("Extensions").click()

        featured_extensions_page.sort_by('recently updated')
        Assert.equal(featured_extensions_page.default_selected_tab, "Recently Updated")
        Assert.contains("sort=updated", featured_extensions_page.get_url_current_page())

        updated_dates = [i.updated_date for i in featured_extensions_page.extensions]
        Assert.is_sorted_descending(updated_dates)
        featured_extensions_page.paginator.click_next_page()

        updated_dates.extend([i.updated_date for i in featured_extensions_page.extensions])
        Assert.is_sorted_descending(updated_dates)

#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from unittestzero import Assert
from pages.desktop.home import Home


class TestExtensions:

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_featured_tab_is_highlighted_by_default(self, mozwebqa):
        """
        Test for Litmus 29706.
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=29706
        """
        home_page = Home(mozwebqa)
        featured_extensions_page = home_page.header.site_navigation_menu("Extensions").click()
        Assert.equal(featured_extensions_page.sorter.sorted_by, "Featured")

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_pagination(self, mozwebqa):
        """
        Test for Litmus 29708
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=29708
        """
        home_page = Home(mozwebqa)
        featured_extensions_page = home_page.header.site_navigation_menu("Extensions").click()
        featured_extensions_page.sorter.sort_by('most_users')
        featured_extensions_page.paginator.click_next_page()

        Assert.contains("&page=2", featured_extensions_page.get_url_current_page())

        featured_extensions_page.paginator.click_prev_page()

        Assert.contains("&page=1", featured_extensions_page.get_url_current_page())

        featured_extensions_page.paginator.click_last_page()

        Assert.true(featured_extensions_page.paginator.is_next_page_disabled)

        featured_extensions_page.paginator.click_first_page()

        Assert.true(featured_extensions_page.paginator.is_prev_page_disabled)

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_previous_button_is_disabled_on_the_first_page(self, mozwebqa):
        """
        Test for Litmus 29709.
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=29709
        """
        home_page = Home(mozwebqa)
        featured_extensions_page = home_page.header.site_navigation_menu("Extensions").click()
        featured_extensions_page.sorter.sort_by('Most Users')

        Assert.true(featured_extensions_page.paginator.is_prev_page_disabled)

        featured_extensions_page.paginator.click_next_page()
        featured_extensions_page.paginator.click_prev_page()

        Assert.true(featured_extensions_page.paginator.is_prev_page_disabled)

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_next_button_is_disabled_on_the_last_page(self, mozwebqa):
        """
        Test for Litmus 29710.
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=29710
        """
        home_page = Home(mozwebqa)
        featured_extensions_page = home_page.header.site_navigation_menu("Extensions").click()
        featured_extensions_page.sorter.sort_by('most_users')
        featured_extensions_page.paginator.click_last_page()

        Assert.true(featured_extensions_page.paginator.is_next_page_disabled, 'Next button is available')

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_checks_if_the_extensions_are_sorted_by_featured(self, mozwebqa):
        """
        Test for Litmus 29713
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=29713
        """
        home_page = Home(mozwebqa)
        featured_extensions_page = home_page.header.site_navigation_menu("Extensions").click()
        featured_extensions_page.sorter.sort_by('most users')
        featured_extensions_page.sorter.sort_by('featured')

        Assert.contains("sort=featured", featured_extensions_page.get_url_current_page())
        for extension in featured_extensions_page.extensions:
            Assert.equal("FEATURED", extension.featured)

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_checks_if_the_extensions_are_sorted_by_top_rated(self, mozwebqa):
        """
        Test for Litmus 29717
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=29717
        """
        home_page = Home(mozwebqa)
        featured_extensions_page = home_page.header.site_navigation_menu("Extensions").click()
        featured_extensions_page.sorter.sort_by("Top Rated")
        Assert.equal(featured_extensions_page.sorter.sorted_by, "Top Rated")
        Assert.contains("sort=rating", featured_extensions_page.get_url_current_page())

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_checks_if_the_extensions_are_sorted_by_most_user(self, mozwebqa):
        """
        Test for Litmus 29715
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=29715
        """
        home_page = Home(mozwebqa)
        featured_extensions_page = home_page.header.site_navigation_menu("Extensions").click()
        featured_extensions_page.sorter.sort_by('most_users')

        Assert.contains("sort=users", featured_extensions_page.get_url_current_page())
        user_counts = [extension.user_count for extension in featured_extensions_page.extensions]
        Assert.is_sorted_descending(user_counts)

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_checks_if_the_extensions_are_sorted_by_newest(self, mozwebqa):
        """
        Test for Litmus 29719
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=29719
        """
        home_page = Home(mozwebqa)
        featured_extensions_page = home_page.header.site_navigation_menu("Extensions").click()
        featured_extensions_page.sorter.sort_by('newest')
        Assert.equal(featured_extensions_page.sorter.sorted_by, "Newest")
        Assert.contains("sort=created", featured_extensions_page.get_url_current_page())

        added_dates = [i.added_date for i in featured_extensions_page.extensions]
        Assert.is_sorted_descending(added_dates)
        featured_extensions_page.paginator.click_next_page()

        added_dates.extend([i.added_date for i in featured_extensions_page.extensions])
        Assert.is_sorted_descending(added_dates)

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_checks_the_extensions_are_sorted_by_name(self, mozwebqa):
        """
        Litmus 29723
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=29723
        """
        home_page = Home(mozwebqa)
        featured_extensions_page = home_page.header.site_navigation_menu("Extensions").click()
        featured_extensions_page.sorter.sort_by('name')

        Assert.contains("sort=name", featured_extensions_page.get_url_current_page())

        names = [i.name for i in featured_extensions_page.extensions]
        sorted_names = sorted(names, key=unicode.lower)
        Assert.true(names[:] == sorted_names[:])

        featured_extensions_page.paginator.click_next_page()

        names.extend([i.name for i in featured_extensions_page.extensions])
        sorted_names = sorted(names, key=unicode.lower)
        Assert.true(names[:] == sorted_names[:])

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_checks_if_the_extensions_are_sorted_by_recently_updated(self, mozwebqa):
        """
        Litmus 29727
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=29727
        """
        home_page = Home(mozwebqa)
        featured_extensions_page = home_page.header.site_navigation_menu("Extensions").click()

        featured_extensions_page.sorter.sort_by('recently updated')
        Assert.equal(featured_extensions_page.sorter.sorted_by, "Recently Updated")
        Assert.contains("sort=updated", featured_extensions_page.get_url_current_page())

        updated_dates = [i.updated_date for i in featured_extensions_page.extensions]
        Assert.is_sorted_descending(updated_dates)
        featured_extensions_page.paginator.click_next_page()

        updated_dates.extend([i.updated_date for i in featured_extensions_page.extensions])
        Assert.is_sorted_descending(updated_dates)

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_extensions_are_sorted_by_up_and_coming(self, mozwebqa):
        """
        Litmus 29729
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=29729
        """
        home_page = Home(mozwebqa)
        featured_extensions_page = home_page.header.site_navigation_menu("Extensions").click()

        featured_extensions_page.sorter.sort_by('up and coming')
        Assert.equal(featured_extensions_page.sorter.sorted_by, "Up & Coming")
        Assert.contains("sort=hotness", featured_extensions_page.get_url_current_page())
        Assert.greater(len(featured_extensions_page.extensions), 0)

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_extensions_page_contains_addons_and_the_pagination_works(self, mozwebqa):
        """
        Litmus 29729
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=29729
        """
        home_page = Home(mozwebqa)
        featured_extensions_page = home_page.header.site_navigation_menu("Extensions").click()

        Assert.equal(len(featured_extensions_page.extensions), 20)
        Assert.true(featured_extensions_page.paginator.is_prev_page_disabled)
        Assert.false(featured_extensions_page.paginator.is_next_page_disabled)

        featured_extensions_page.paginator.click_next_page()

        Assert.false(featured_extensions_page.paginator.is_prev_page_disabled)
        Assert.false(featured_extensions_page.paginator.is_next_page_disabled)

        Assert.equal(len(featured_extensions_page.extensions), 20)

        featured_extensions_page.paginator.click_prev_page()

        Assert.equal(len(featured_extensions_page.extensions), 20)
        Assert.true(featured_extensions_page.paginator.is_prev_page_disabled)
        Assert.false(featured_extensions_page.paginator.is_next_page_disabled)

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_breadcrumb_menu_in_extensions_page(self, mozwebqa):
        """
        Litmus 29812
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=29812
        """

        home_page = Home(mozwebqa)
        featured_extensions_page = home_page.header.site_navigation_menu("Extensions").click()

        breadcrumbs = featured_extensions_page.breadcrumbs

        Assert.equal(breadcrumbs[0].text, 'Add-ons for Firefox')
        Assert.equal(breadcrumbs[1].text, 'Extensions')

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_checks_if_the_subscribe_link_exists(self, mozwebqa):
        """
        Test for Litmus 29812
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=29812
        """
        home_page = Home(mozwebqa)
        featured_extensions_page = home_page.header.site_navigation_menu("Extensions").click()
        Assert.contains("Subscribe", featured_extensions_page.subscribe_link_text)

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_checks_featured_extensions_header(self, mozwebqa):
        """
        Test for Litmus 29812
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=29812
        """
        home_page = Home(mozwebqa)
        featured_extensions_page = home_page.header.site_navigation_menu("Extensions").click()
        Assert.equal("Featured Extensions", featured_extensions_page.featured_extensions_header_text)

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.desktop.home import Home


class TestExtensions:

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_featured_tab_is_highlighted_by_default(self, base_url, selenium):
        home_page = Home(base_url, selenium)
        featured_extensions_page = home_page.header.site_navigation_menu("Extensions").click()
        assert 'Featured' == featured_extensions_page.sorter.sorted_by

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_pagination(self, base_url, selenium):
        home_page = Home(base_url, selenium)
        featured_extensions_page = home_page.header.site_navigation_menu("Extensions").click()
        featured_extensions_page.sorter.sort_by('most_users')
        featured_extensions_page.paginator.click_next_page()
        assert '&page=2' in featured_extensions_page.get_url_current_page()
        featured_extensions_page.paginator.click_prev_page()
        assert '&page=1' in featured_extensions_page.get_url_current_page()
        featured_extensions_page.paginator.click_last_page()
        assert featured_extensions_page.paginator.is_next_page_disabled
        featured_extensions_page.paginator.click_first_page()
        assert featured_extensions_page.paginator.is_prev_page_disabled

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_previous_button_is_disabled_on_the_first_page(self, base_url, selenium):
        home_page = Home(base_url, selenium)
        featured_extensions_page = home_page.header.site_navigation_menu("Extensions").click()
        featured_extensions_page.sorter.sort_by('Most Users')
        assert featured_extensions_page.paginator.is_prev_page_disabled
        featured_extensions_page.paginator.click_next_page()
        featured_extensions_page.paginator.click_prev_page()
        assert featured_extensions_page.paginator.is_prev_page_disabled

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_next_button_is_disabled_on_the_last_page(self, base_url, selenium):
        home_page = Home(base_url, selenium)
        featured_extensions_page = home_page.header.site_navigation_menu("Extensions").click()
        featured_extensions_page.sorter.sort_by('most_users')
        featured_extensions_page.paginator.click_last_page()
        assert featured_extensions_page.paginator.is_next_page_disabled, 'Next button is available'

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_checks_if_the_extensions_are_sorted_by_top_rated(self, base_url, selenium):
        home_page = Home(base_url, selenium)
        featured_extensions_page = home_page.header.site_navigation_menu("Extensions").click()
        featured_extensions_page.sorter.sort_by("Top Rated")
        assert 'Top Rated' == featured_extensions_page.sorter.sorted_by
        assert 'sort=rating' in featured_extensions_page.get_url_current_page()

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_checks_if_the_extensions_are_sorted_by_most_user(self, base_url, selenium):
        home_page = Home(base_url, selenium)
        featured_extensions_page = home_page.header.site_navigation_menu("Extensions").click()
        featured_extensions_page.sorter.sort_by('most_users')
        assert 'sort=users' in featured_extensions_page.get_url_current_page()
        user_counts = [extension.user_count for extension in featured_extensions_page.extensions]
        assert sorted(user_counts, reverse=True) == user_counts

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_checks_if_the_extensions_are_sorted_by_newest(self, base_url, selenium):
        home_page = Home(base_url, selenium)
        featured_extensions_page = home_page.header.site_navigation_menu("Extensions").click()
        featured_extensions_page.sorter.sort_by('newest')
        assert 'Newest' == featured_extensions_page.sorter.sorted_by
        assert 'sort=created' in featured_extensions_page.get_url_current_page()

        added_dates = [i.added_date for i in featured_extensions_page.extensions]
        assert sorted(added_dates, reverse=True) == added_dates
        featured_extensions_page.paginator.click_next_page()

        added_dates.extend([i.added_date for i in featured_extensions_page.extensions])
        assert sorted(added_dates, reverse=True) == added_dates

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_checks_if_the_extensions_are_sorted_by_recently_updated(self, base_url, selenium):
        home_page = Home(base_url, selenium)
        featured_extensions_page = home_page.header.site_navigation_menu("Extensions").click()

        featured_extensions_page.sorter.sort_by('recently updated')
        assert 'Recently Updated' == featured_extensions_page.sorter.sorted_by
        assert 'sort=updated' in featured_extensions_page.get_url_current_page()

        updated_dates = [i.updated_date for i in featured_extensions_page.extensions]
        assert sorted(updated_dates, reverse=True) == updated_dates
        featured_extensions_page.paginator.click_next_page()

        updated_dates.extend([i.updated_date for i in featured_extensions_page.extensions])
        assert sorted(updated_dates, reverse=True) == updated_dates

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_extensions_are_sorted_by_up_and_coming(self, base_url, selenium):
        home_page = Home(base_url, selenium)
        featured_extensions_page = home_page.header.site_navigation_menu("Extensions").click()
        featured_extensions_page.sorter.sort_by('up and coming')
        assert 'Up & Coming' == featured_extensions_page.sorter.sorted_by
        assert 'sort=hotness' in featured_extensions_page.get_url_current_page()
        assert len(featured_extensions_page.extensions) > 0

    @pytest.mark.nondestructive
    def test_that_extensions_page_contains_addons_and_the_pagination_works(self, base_url, selenium):
        home_page = Home(base_url, selenium)
        featured_extensions_page = home_page.header.site_navigation_menu("Extensions").click()

        # Assert that at least one addon is displayed
        assert len(featured_extensions_page.extensions) > 0

        if len(featured_extensions_page.extensions) < 20:
            # Assert that the paginator is not present if fewer than 20 extensions are displayed
            assert not featured_extensions_page.is_paginator_present
        else:
            # Assert that the paginator is present if 20 extensions are displayed
            assert featured_extensions_page.is_paginator_present
            assert featured_extensions_page.paginator.is_prev_page_disabled
            assert not featured_extensions_page.paginator.is_next_page_disabled

            featured_extensions_page.paginator.click_next_page()
            assert not featured_extensions_page.paginator.is_prev_page_disabled
            assert not featured_extensions_page.paginator.is_next_page_disabled

            featured_extensions_page.paginator.click_prev_page()
            assert 20 == len(featured_extensions_page.extensions)
            assert featured_extensions_page.paginator.is_prev_page_disabled
            assert not featured_extensions_page.paginator.is_next_page_disabled

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_breadcrumb_menu_in_extensions_page(self, base_url, selenium):
        home_page = Home(base_url, selenium)
        featured_extensions_page = home_page.header.site_navigation_menu("Extensions").click()
        breadcrumbs = featured_extensions_page.breadcrumbs
        assert 'Add-ons for Firefox' == breadcrumbs[0].text
        assert 'Extensions' == breadcrumbs[1].text

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_checks_if_the_subscribe_link_exists(self, base_url, selenium):
        home_page = Home(base_url, selenium)
        featured_extensions_page = home_page.header.site_navigation_menu("Extensions").click()
        assert 'Subscribe' in featured_extensions_page.subscribe_link_text

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_checks_featured_extensions_header(self, base_url, selenium):
        home_page = Home(base_url, selenium)
        featured_extensions_page = home_page.header.site_navigation_menu("Extensions").click()
        assert 'Featured Extensions' == featured_extensions_page.featured_extensions_header_text

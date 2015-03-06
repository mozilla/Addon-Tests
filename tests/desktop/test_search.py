#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import pytest

from unittestzero import Assert

from pages.desktop.home import Home


class TestSearch:

    @pytest.mark.nondestructive
    def test_that_search_all_add_ons_results_have_pagination_that_moves_through_results(self, mozwebqa):
        """
        Open a page with search results.
        1. On the first page, check that "<<" and "previous are not active, but "next" and ">>" are active.
        2. Move forward one page by clicking next, all buttons are active
        3. Click ">>" to go to last page.  Check that "<<" and "previous" are clickable but "next" and ">>" are not.
        4. Assert the page number has incremented or decreased
        5. Click "previous", all buttons are highlighted.
        """
        home_page = Home(mozwebqa)
        search_page = home_page.search_for('addon')

        expected_page = 1

        # On the first page, "<<" and "previous" are not active, but "next" and ">>" are active.
        Assert.true(search_page.paginator.is_prev_page_disabled)
        Assert.true(search_page.paginator.is_first_page_disabled)
        Assert.false(search_page.paginator.is_next_page_disabled)
        Assert.false(search_page.paginator.is_last_page_disabled)
        Assert.equal(search_page.paginator.page_number, expected_page)

        # Move forward one page by clicking next, all buttons should be active.
        search_page.paginator.click_next_page()

        expected_page += 1

        Assert.false(search_page.paginator.is_prev_page_disabled)
        Assert.false(search_page.paginator.is_first_page_disabled)
        Assert.false(search_page.paginator.is_next_page_disabled)
        Assert.false(search_page.paginator.is_last_page_disabled)
        Assert.equal(search_page.paginator.page_number, expected_page)

        # Click ">>" to go to last page. "<<" and "previous" are active, but "next" and ">>" are not.
        search_page.paginator.click_last_page()

        expected_page = search_page.paginator.total_page_number

        Assert.false(search_page.paginator.is_prev_page_disabled)
        Assert.false(search_page.paginator.is_first_page_disabled)
        Assert.true(search_page.paginator.is_next_page_disabled)
        Assert.true(search_page.paginator.is_last_page_disabled)
        Assert.equal(search_page.paginator.page_number, expected_page)

        # Click "previous", all buttons are active.
        search_page.paginator.click_prev_page()

        expected_page -= 1

        Assert.false(search_page.paginator.is_prev_page_disabled)
        Assert.false(search_page.paginator.is_first_page_disabled)
        Assert.false(search_page.paginator.is_next_page_disabled)
        Assert.false(search_page.paginator.is_last_page_disabled)
        Assert.equal(search_page.paginator.page_number, expected_page)

    @pytest.mark.nondestructive
    @pytest.mark.parametrize('term', [
        # 9575
        u'\u0421\u043b\u043e\u0432\u0430\u0440\u0438 \u042f\u043d\u0434\u0435\u043a\u0441',
        'fox',  # 9561
        '',     # 11759
        '1',    # 17347
    ])
    def test_that_various_search_terms_return_results(self, mozwebqa, term):
        search_page = Home(mozwebqa).search_for(term)

        Assert.false(search_page.is_no_results_present)
        Assert.greater(search_page.result_count, 0)

    @pytest.mark.nondestructive
    def test_that_page_with_search_results_has_correct_title(self, mozwebqa):
        home_page = Home(mozwebqa)
        search_keyword = 'Search term'
        search_page = home_page.search_for(search_keyword)

        expected_title = '%s :: Search :: Add-ons for Firefox' % search_keyword
        Assert.equal(expected_title, search_page.page_title)

    @pytest.mark.smoke
    @pytest.mark.nondestructive
    def test_that_searching_for_firebug_returns_firebug_as_first_result(self, mozwebqa):
        home_page = Home(mozwebqa)
        search_page = home_page.search_for('firebug')
        results = [result.name for result in search_page.results]

        Assert.equal('Firebug', results[0])

    @pytest.mark.nondestructive
    def test_that_searching_for_cool_returns_results_with_cool_in_their_name_description(self, mozwebqa):
        home_page = Home(mozwebqa)
        search_term = 'cool'
        search_page = home_page.search_for(search_term)
        Assert.false(search_page.is_no_results_present)

        for i in range(0, len(search_page.results)):
            try:
                Assert.contains(search_term, search_page.results[i].text.lower())
            except:
                devs_comments = ''
                details_page = search_page.results[i].click_result()
                if details_page.is_devs_comments_section_present:
                    details_page.expand_devs_comments()
                    devs_comments = details_page.devs_comments_message
                search_range = details_page.description + devs_comments
                Assert.contains(search_term, search_range.lower())
                details_page.return_to_previous_page()

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_sorting_by_downloads(self, mozwebqa):
        search_page = Home(mozwebqa).search_for('firebug')
        search_page.click_sort_by('Weekly Downloads')
        Assert.true('sort=downloads' in search_page.get_url_current_page())
        downloads = [i.downloads for i in search_page.results]
        Assert.is_sorted_descending(downloads)
        search_page.paginator.click_next_page()

        downloads.extend([i.downloads for i in search_page.results])
        Assert.is_sorted_descending(downloads)

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_sorting_by_newest(self, mozwebqa):
        search_page = Home(mozwebqa).search_for('firebug')
        search_page.click_sort_by('Newest')
        Assert.true('sort=created' in search_page.get_url_current_page())
        Assert.is_sorted_descending([i.created_date for i in search_page.results])

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_sorting_by_most_recently_updated(self, mozwebqa):
        search_page = Home(mozwebqa).search_for('firebug')
        search_page.click_sort_by('Recently Updated')
        Assert.contains('sort=updated', search_page.get_url_current_page())
        results = [i.updated_date for i in search_page.results]
        Assert.is_sorted_descending(results)
        search_page.paginator.click_next_page()
        results.extend([i.updated_date for i in search_page.results])
        Assert.is_sorted_descending(results)

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_sorting_by_number_of_most_users(self, mozwebqa):
        search_page = Home(mozwebqa).search_for('firebug')
        search_page.click_sort_by('Most Users')
        Assert.contains('sort=users', search_page.get_url_current_page())
        Assert.is_sorted_descending([i.users for i in search_page.results])

    @pytest.mark.nondestructive
    def test_that_searching_for_a_tag_returns_results(self, mozwebqa):

        home_page = Home(mozwebqa)
        search_page = home_page.search_for('development')
        result_count = search_page.filter.results_count
        Assert.greater(result_count, 0)

        search_page.filter.tag('development').click_tag()
        Assert.greater_equal(result_count, search_page.filter.results_count)

    @pytest.mark.nondestructive
    def test_that_search_results_return_20_results_per_page(self, mozwebqa):
        home_page = Home(mozwebqa)
        search_page = home_page.search_for('deutsch')

        first_expected = 1
        second_expected = 20

        while not search_page.paginator.is_next_page_disabled:
            first_count = search_page.paginator.start_item
            second_count = search_page.paginator.end_item

            Assert.equal(first_expected, first_count)
            Assert.equal(second_expected, second_count)
            Assert.equal(search_page.result_count, 20)

            search_page.paginator.click_next_page()

            first_expected += 20
            second_expected += 20

        number = search_page.paginator.total_items % 20

        if number == 0:
            Assert.equal(search_page.result_count, 20)
        else:
            Assert.equal(search_page.result_count, number)

    @pytest.mark.native
    @pytest.mark.nondestructive
    @pytest.mark.smoke
    @pytest.mark.parametrize(('addon_type', 'term', 'breadcrumb_component'), [
        ('Complete Themes', 'nasa', 'Complete Themes'),           # 17350
        ('Extensions', 'fire', 'Extensions'),
        ('Themes', 'fox', 'Themes'),        # 17349
        ('Collections', 'web', 'Collections'),  # 17352
        # these last two depend on the More menu
        # ('Add-ons for Mobile', 'fire', 'Extensions')
        # ('Dictionaries & Language Packs', 'a', 'Dictionaries'),
    ])
    def test_searching_for_addon_type_returns_results_of_correct_type(
        self, mozwebqa, addon_type, term, breadcrumb_component
    ):
        amo_home_page = Home(mozwebqa)

        search_results = None

        if (addon_type == 'Complete Themes'):
            search_results = amo_home_page.search_for(term)

            search_results.filter.category.expand_filter_options()
            search_results.filter.category.click_filter_complete_themes()

            search_results.filter.works_with.expand_filter_options()
            search_results.filter.works_with.click_filter_all_versions_of_firefox()
            search_results.filter.works_with.click_filter_all_systems()
        else:
            amo_addon_type_page = amo_home_page.header.site_navigation_menu(addon_type).click()
            search_results = amo_addon_type_page.search_for(term)

        Assert.true(search_results.result_count > 0,
                    'Search did not return results. Search terms: %s' % search_results.selenium.current_url)

        # click through to each result and verify navigation breadcrumbs are correct
        for i in range(search_results.result_count):
            addon = search_results.result(i).click_result()
            Assert.contains(breadcrumb_component, addon.breadcrumb,
                            "Expected to find: '%s' in '%s'. url: %s" %
                            (breadcrumb_component, addon.breadcrumb, addon.selenium.current_url))
            addon.return_to_previous_page()

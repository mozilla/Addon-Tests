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
        Test for Litmus 4839 and 17339.
        https://litmus.mozilla.org/show_test.cgi?id=4839
        https://litmus.mozilla.org/show_test.cgi?id=17339
        Open a page with search results.
        1. On the first page, check that "<<" and "previous are not active, but "next" and ">>" are active.
        2. Move forward one page by clicking next, all buttons are active
        3. Click ">>" to go to last page.  Check that "<<" and "previous" are clickable but "next" and ">>" are not.
        4. Assert the page number has incremented or decreased
        5. Click "previous", all buttons are highlighted.
        """
        home_page = Home(mozwebqa)
        search_page = home_page.header.search_for('addon')

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
    def test_that_searching_with_unicode_characters_returns_results(self, mozwebqa):
        """
        Test for Litmus 9575.
        https://litmus.mozilla.org/show_test.cgi?id=9575
        """
        home_page = Home(mozwebqa)
        search_str = u'\u0421\u043b\u043e\u0432\u0430\u0440\u0438 \u042f\u043d\u0434\u0435\u043a\u0441'
        search_page = home_page.header.search_for(search_str)

        Assert.contains(search_str, search_page.search_results_title)
        Assert.false('0 matching results' in search_page.number_of_results_text)

    @pytest.mark.nondestructive
    def test_that_searching_with_substrings_returns_results(self, mozwebqa):
        """
        Test for Litmus 9561.
        https://litmus.mozilla.org/show_test.cgi?id=9561
        """
        home_page = Home(mozwebqa)
        search_page = home_page.header.search_for('fox')

        Assert.false(search_page.is_no_results_present, 'No results were found')

        results_text_summary = search_page.number_of_results_text
        Assert.not_equal(u'0 matching results', results_text_summary)

        Assert.true(int(results_text_summary.split()[0]) > 1)

    @pytest.mark.nondestructive
    def test_that_blank_search_returns_results(self, mozwebqa):
        """
        Test for Litmus 11759.
        https://litmus.mozilla.org/show_test.cgi?id=11759
        """
        home_page = Home(mozwebqa)
        search_page = home_page.header.search_for("")

        Assert.false(search_page.is_no_results_present)
        Assert.greater(search_page.result_count, 0)

    @pytest.mark.nondestructive
    def test_that_page_with_search_results_has_correct_title(self, mozwebqa):
        """
        Test for Litmus 17338.
        https://litmus.mozilla.org/show_test.cgi?id=17338
        """
        home_page = Home(mozwebqa)
        search_keyword = 'Search term'
        search_page = home_page.header.search_for(search_keyword)

        expected_title = '%s :: Search :: Add-ons for Firefox' % search_keyword
        Assert.equal(expected_title, search_page.page_title)

    @pytest.mark.smoke
    @pytest.mark.nondestructive
    def test_that_searching_for_fire_returns_firebug(self, mozwebqa):
        """
        Test for Litmus 15314.
        https://litmus.mozilla.org/show_test.cgi?id=15314
        """
        home_page = Home(mozwebqa)
        search_page = home_page.header.search_for('fire')

        results = [result.name  for result in search_page.results]

        Assert.contains('Firebug', results)

    @pytest.mark.nondestructive
    def test_that_searching_for_cool_returns_results_with_cool_in_their_name_description(self, mozwebqa):
        """
        Test for Litmus 17353.
        https://litmus.mozilla.org/show_test.cgi?id=17353
        """
        home_page = Home(mozwebqa)
        search_term = 'cool'
        search_page = home_page.header.search_for(search_term)
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

    @pytest.mark.nondestructive
    def test_that_searching_with_numerals_returns_results(self, mozwebqa):
        """
        Test for Litmus 17347.
        https://litmus.mozilla.org/show_test.cgi?id=17347
        """
        search_page = Home(mozwebqa).header.search_for('1')

        Assert.greater(search_page.result_count, 0)
        Assert.greater(int(search_page.number_of_results_text.replace(',', '').split()[0]), 0)

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_sorting_by_downloads(self, mozwebqa):
        """
        Test for Litmus 17342.
        https://litmus.mozilla.org/show_test.cgi?id=17342
        """
        search_page = Home(mozwebqa).header.search_for('firebug')
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
        """
        Test for Litmus 17343.
        https://litmus.mozilla.org/show_test.cgi?id=17343
        """
        search_page = Home(mozwebqa).header.search_for('firebug')
        search_page.click_sort_by('Newest')
        Assert.true('sort=created' in search_page.get_url_current_page())
        Assert.is_sorted_descending([i.created_date for i in search_page.results])

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_sorting_by_most_recently_updated(self, mozwebqa):
        """
        Test for Litmus 17345.
        https://litmus.mozilla.org/show_test.cgi?id=17345
        """
        search_page = Home(mozwebqa).header.search_for('firebug')
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
        """
        Test for Litmus 24867.
        https://litmus.mozilla.org/show_test.cgi?id=24867
        """
        search_page = Home(mozwebqa).header.search_for('firebug')
        search_page.click_sort_by('Most Users')
        Assert.contains('sort=users', search_page.get_url_current_page())
        Assert.is_sorted_descending([i.users for i in search_page.results])

    @pytest.mark.nondestructive
    def test_that_searching_for_a_tag_returns_results(self, mozwebqa):
        """
        Test for Litmus 7848.
        https://litmus.mozilla.org/show_test.cgi?id=7848
        """

        home_page = Home(mozwebqa)
        search_page = home_page.header.search_for('development')
        result_count = search_page.filter.results_count
        Assert.greater(result_count, 0)

        search_page.filter.tag('development').click_tag()
        Assert.greater_equal(result_count, search_page.filter.results_count)

    @pytest.mark.nondestructive
    def test_that_search_results_return_20_results_per_page(self, mozwebqa):
        """
        Test for Litmus 17346.
        https://litmus.mozilla.org/show_test.cgi?id=17346
        """
        home_page = Home(mozwebqa)
        search_page = home_page.header.search_for('deutsch')

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
    @pytest.mark.smoke
    @pytest.mark.nondestructive
    def test_searching_for_collections_returns_results(self, mozwebqa):
        """
        Test for Litmus 17352.
        https://litmus.mozilla.org/show_test.cgi?id=17352
        """
        home_page = Home(mozwebqa)
        amo_collection_page = home_page.header.site_navigation_menu("Collections").click()
        amo_search_results_page = amo_collection_page.search_for('web')

        Assert.true(amo_search_results_page.result_count > 0)

    @pytest.mark.native
    @pytest.mark.smoke
    @pytest.mark.nondestructive
    def test_searching_for_personas_returns_results(self, mozwebqa):
        """
        Test for Litmus 17349.
        https://litmus.mozilla.org/show_test.cgi?id=17349
        """
        amo_home_page = Home(mozwebqa)
        amo_personas_page = amo_home_page.header.site_navigation_menu("Personas").click()
        amo_personas_page.header.search_for('fox')

        Assert.true(amo_personas_page.persona_count > 0)

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_searching_for_theme_returns_results(self, mozwebqa):
        """
        Test for Litmus 17350
        https://litmus.mozilla.org/show_test.cgi?id=17350
        """
        amo_home_page = Home(mozwebqa)
        amo_themes_page = amo_home_page.header.site_navigation_menu("Themes").click()
        search_results = amo_themes_page.header.search_for('nasa')

        Assert.true(search_results.result_count > 0)

        for i in range(search_results.result_count):
            addon = search_results.result(i).click_result()
            Assert.contains('Themes', addon.breadcrumb)
            addon.return_to_previous_page()

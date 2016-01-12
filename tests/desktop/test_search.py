# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import pytest


from pages.desktop.home import Home
from pages.desktop.complete_themes import CompleteThemes
from pages.desktop.collections import Collections
from pages.desktop.extensions import ExtensionsHome
from pages.desktop.themes import Themes


class TestSearch:

    @pytest.mark.nondestructive
    def test_that_search_all_add_ons_results_have_pagination_that_moves_through_results(self, base_url, selenium):
        """
        Open a page with search results.
        1. On the first page, check that "<<" and "previous are not active, but "next" and ">>" are active.
        2. Move forward one page by clicking next, all buttons are active
        3. Click ">>" to go to last page.  Check that "<<" and "previous" are clickable but "next" and ">>" are not.
        4. Assert the page number has incremented or decreased
        5. Click "previous", all buttons are highlighted.
        """
        home_page = Home(base_url, selenium)
        search_page = home_page.search_for('addon')
        expected_page = 1

        # On the first page, "<<" and "previous" are not active, but "next" and ">>" are active.
        assert search_page.paginator.is_prev_page_disabled
        assert search_page.paginator.is_first_page_disabled
        assert not search_page.paginator.is_next_page_disabled
        assert not search_page.paginator.is_last_page_disabled
        assert expected_page == search_page.paginator.page_number

        # Move forward one page by clicking next, all buttons should be active.
        search_page.paginator.click_next_page()
        expected_page += 1
        assert not search_page.paginator.is_prev_page_disabled
        assert not search_page.paginator.is_first_page_disabled
        assert not search_page.paginator.is_next_page_disabled
        assert not search_page.paginator.is_last_page_disabled
        assert expected_page == search_page.paginator.page_number

        # Click ">>" to go to last page. "<<" and "previous" are active, but "next" and ">>" are not.
        search_page.paginator.click_last_page()
        expected_page = search_page.paginator.total_page_number
        assert not search_page.paginator.is_prev_page_disabled
        assert not search_page.paginator.is_first_page_disabled
        assert search_page.paginator.is_next_page_disabled
        assert search_page.paginator.is_last_page_disabled
        assert expected_page == search_page.paginator.page_number

        # Click "previous", all buttons are active.
        search_page.paginator.click_prev_page()
        expected_page -= 1
        assert not search_page.paginator.is_prev_page_disabled
        assert not search_page.paginator.is_first_page_disabled
        assert not search_page.paginator.is_next_page_disabled
        assert not search_page.paginator.is_last_page_disabled
        assert expected_page == search_page.paginator.page_number

    @pytest.mark.nondestructive
    @pytest.mark.parametrize('term', [
        # 9575
        u'\u0421\u043b\u043e\u0432\u0430\u0440\u0438 \u042f\u043d\u0434\u0435\u043a\u0441',
        'fox',  # 9561
        '',     # 11759
        '1',    # 17347
    ])
    def test_that_various_search_terms_return_results(self, base_url, selenium, term):
        search_page = Home(base_url, selenium).search_for(term)
        assert not search_page.is_no_results_present
        assert search_page.result_count > 0

    @pytest.mark.nondestructive
    def test_that_page_with_search_results_has_correct_title(self, base_url, selenium):
        home_page = Home(base_url, selenium)
        search_keyword = 'Search term'
        search_page = home_page.search_for(search_keyword)
        expected_title = '%s :: Search :: Add-ons for Firefox' % search_keyword
        assert expected_title == search_page.page_title

    @pytest.mark.smoke
    @pytest.mark.nondestructive
    def test_that_searching_for_firebug_returns_firebug_as_first_result(self, base_url, selenium):
        home_page = Home(base_url, selenium)
        search_page = home_page.search_for('firebug')
        results = [result.name for result in search_page.results]
        assert 'Firebug' == results[0]

    @pytest.mark.nondestructive
    def test_that_searching_for_cool_returns_results_with_cool_in_their_name_description(self, base_url, selenium):
        home_page = Home(base_url, selenium)
        search_term = 'cool'
        search_page = home_page.search_for(search_term)
        assert not search_page.is_no_results_present

        for i in range(0, len(search_page.results)):
            try:
                assert search_term in search_page.results[i].text.lower()
            except:
                devs_comments = ''
                details_page = search_page.results[i].click_result()
                if details_page.is_devs_comments_section_present:
                    details_page.expand_devs_comments()
                    devs_comments = details_page.devs_comments_message
                search_range = details_page.description + devs_comments
                assert search_term in search_range.lower()
                details_page.return_to_previous_page()

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_sorting_by_downloads(self, base_url, selenium):
        search_page = Home(base_url, selenium).search_for('firebug')
        search_page.click_sort_by('Weekly Downloads')
        assert 'sort=downloads' in search_page.get_url_current_page()
        downloads = [i.downloads for i in search_page.results]
        assert sorted(downloads, reverse=True) == downloads
        search_page.paginator.click_next_page()
        downloads.extend([i.downloads for i in search_page.results])
        assert sorted(downloads, reverse=True) == downloads

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_sorting_by_newest(self, base_url, selenium):
        search_page = Home(base_url, selenium).search_for('firebug')
        search_page.click_sort_by('Newest')
        assert 'sort=created' in search_page.get_url_current_page()
        results = [i.created_date for i in search_page.results]
        assert sorted(results, reverse=True) == results

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_sorting_by_most_recently_updated(self, base_url, selenium):
        search_page = Home(base_url, selenium).search_for('firebug')
        search_page.click_sort_by('Recently Updated')
        assert 'sort=updated' in search_page.get_url_current_page()
        results = [i.updated_date for i in search_page.results]
        assert sorted(results, reverse=True) == results
        search_page.paginator.click_next_page()
        results.extend([i.updated_date for i in search_page.results])
        assert sorted(results, reverse=True) == results

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_sorting_by_number_of_most_users(self, base_url, selenium):
        search_page = Home(base_url, selenium).search_for('firebug')
        search_page.click_sort_by('Most Users')
        assert 'sort=users' in search_page.get_url_current_page()
        results = [i.users for i in search_page.results]
        assert sorted(results, reverse=True) == results

    @pytest.mark.nondestructive
    def test_that_searching_for_a_tag_returns_results(self, base_url, selenium):
        home_page = Home(base_url, selenium)
        search_page = home_page.search_for('development')
        result_count = search_page.filter.results_count
        assert result_count > 0
        search_page.filter.tag('development').click_tag()
        assert search_page.filter.results_count >= result_count

    @pytest.mark.nondestructive
    def test_that_search_results_return_20_results_per_page(self, base_url, selenium):
        home_page = Home(base_url, selenium)
        search_page = home_page.search_for('deutsch')

        first_expected = 1
        second_expected = 20

        while not search_page.paginator.is_next_page_disabled:
            first_count = search_page.paginator.start_item
            second_count = search_page.paginator.end_item

            assert first_expected == first_count
            assert second_expected == second_count
            assert 20 == search_page.result_count

            search_page.paginator.click_next_page()

            first_expected += 20
            second_expected += 20

        number = search_page.paginator.total_items % 20

        if number == 0:
            assert 20 == search_page.result_count
        else:
            assert number == search_page.result_count

    @pytest.mark.nondestructive
    @pytest.mark.smoke
    def test_searching_for_extensions(self, base_url, selenium):
        page = ExtensionsHome(base_url, selenium).open()
        results_page = page.search_for('fire')
        assert len(results_page.results) > 0
        # click through to each result and verify navigation breadcrumbs
        for i in range(len(results_page.results)):
            addon = results_page.result(i).click_result()
            assert 'Extensions' in addon.breadcrumb
            selenium.back()

    @pytest.mark.nondestructive
    @pytest.mark.smoke
    def test_searching_for_themes(self, base_url, selenium):
        page = Themes(base_url, selenium).open()
        results_page = page.search_for('fox')
        assert len(results_page.results) > 0
        # click through to each result and verify navigation breadcrumbs
        for i in range(len(results_page.results)):
            addon = results_page.result(i).click_result()
            assert 'Themes' in addon.breadcrumb
            selenium.back()

    @pytest.mark.nondestructive
    @pytest.mark.smoke
    @pytest.mark.xfail(reason='https://github.com/mozilla/olympia/issues/1247')
    def test_searching_for_complete_themes(self, base_url, selenium):
        page = CompleteThemes(base_url, selenium).open()
        results_page = page.search_for('nasa')
        # show results for all firefox versions and platforms
        results_page.filter.works_with.expand_filter_options()
        results_page.filter.works_with.click_filter_all_versions_of_firefox()
        results_page.filter.works_with.click_filter_all_systems()
        assert len(results_page.results) > 0
        # click through to each result and verify navigation breadcrumbs
        for i in range(len(results_page.results)):
            addon = results_page.result(i).click_result()
            assert 'Complete Themes' in addon.breadcrumb
            selenium.back()

    @pytest.mark.nondestructive
    @pytest.mark.smoke
    def test_searching_for_collections(self, base_url, selenium):
        page = Collections(base_url, selenium).open()
        results_page = page.search_for('web')
        assert len(results_page.results) > 0
        # click through to each result and verify navigation breadcrumbs
        for i in range(len(results_page.results)):
            addon = results_page.result(i).click_result()
            assert 'Collections' in addon.breadcrumb
            selenium.back()

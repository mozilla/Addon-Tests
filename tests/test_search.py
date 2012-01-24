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
# Contributor(s): David Burns
#                 Dave Hunt <dhunt@mozilla.com>
#                 Alex Rodionov <p0deje@gmail.com>
#                 Bebe <florin.strugariu@softvision.ro>
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


import re
import pytest

from unittestzero import Assert

from pages.home import Home

xfail = pytest.mark.xfail
nondestructive = pytest.mark.nondestructive


class TestSearch:

    @nondestructive
    def test_that_search_all_add_ons_results_have_pagination_that_moves_through_results(self, mozwebqa):
        """
        Test for Litmus 4839 and 17339.
        https://litmus.mozilla.org/show_test.cgi?id=4839
        https://litmus.mozilla.org/show_test.cgi?id=17339
        """
        home_page = Home(mozwebqa)
        search_page = home_page.header.search_for('addon')
        first_expected = 1
        second_expected = 20

        # Go Forward 10 times
        for i in range(10):
            search_page.page_forward()
            results_summary = search_page.results_displayed

            results = re.split('\W+', results_summary)
            first_count = results[1]
            second_count = results[2]

            first_expected += 20
            second_expected += 20
            Assert.equal(str(first_expected), first_count)
            Assert.equal(str(second_expected), second_count)

        # Go Back 10 Times
        for i in range(10):
            search_page.page_back()
            results_summary = search_page.results_displayed

            results = re.split('\W+', results_summary)
            first_count = results[1]
            second_count = results[2]

            first_expected -= 20
            second_expected -= 20
            Assert.equal(str(first_expected), first_count)
            Assert.equal(str(second_expected), second_count)

    @nondestructive
    def test_that_entering_a_long_string_returns_no_results(self, mozwebqa):
        """
        Test for Litmus 4856.
        https://litmus.mozilla.org/show_test.cgi?id=4856
        """
        home_page = Home(mozwebqa)
        search_page = home_page.header.search_for('a' * 255)

        Assert.true(search_page.is_no_results_present)
        Assert.equal('No results found.', search_page.no_results_text)

        Assert.true('0 matching results' in search_page.number_of_results_text)

    @nondestructive
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

    @nondestructive
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

    @nondestructive
    def test_that_blank_search_returns_results(self, mozwebqa):
        """ Litmus 11759
            https://litmus.mozilla.org/show_test.cgi?id=11759 """
        home_page = Home(mozwebqa)
        search_page = home_page.header.search_for("")

        Assert.false(search_page.is_no_results_present)
        Assert.greater(search_page.result_count, 0)

    @nondestructive
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

    @nondestructive
    def test_that_searching_for_fire_returns_firebug(self, mozwebqa):
        """
        Test for Litmus 15314.
        https://litmus.mozilla.org/show_test.cgi?id=15314
        """
        home_page = Home(mozwebqa)
        search_page = home_page.header.search_for('fire')

        Assert.equal(search_page.result(0).name, 'Firebug')

    @nondestructive
    def test_that_searching_for_cool_returns_results_with_cool_in_their_name_description(self, mozwebqa):
        """
        Test for Litmus 17353.
        https://litmus.mozilla.org/show_test.cgi?id=17353
        """
        home_page = Home(mozwebqa)
        search_page = home_page.header.search_for('Cool')

        for i in range(10):
            Assert.contains('cool', search_page.result(i).text.lower())

    @nondestructive
    def test_that_searching_with_numerals_returns_results(self, mozwebqa):
        """
        Test for Litmus 17347.
        https://litmus.mozilla.org/show_test.cgi?id=17347
        """
        search_page = Home(mozwebqa).header.search_for('1')

        Assert.greater(search_page.result_count, 0)
        Assert.true(int(search_page.number_of_results_text.split()[0]) > 0)

    @nondestructive
    def test_sorting_by_downloads(self, mozwebqa):
        """
        Test for Litmus 17342.
        https://litmus.mozilla.org/show_test.cgi?id=17342
        """
        search_page = Home(mozwebqa).header.search_for('firebug')
        search_page.sort_by('Weekly Downloads')
        Assert.true('sort=downloads' in search_page.get_url_current_page())
        downloads = [i.downloads for i in search_page.results()]
        Assert.is_sorted_descending(downloads)
        search_page.page_forward()
        downloads.extend([i.downloads for i in search_page.results()])
        Assert.is_sorted_descending(downloads)

    @nondestructive
    def test_sorting_by_newest(self, mozwebqa):
        """
        Test for Litmus 17343.
        https://litmus.mozilla.org/show_test.cgi?id=17343
        """
        search_page = Home(mozwebqa).header.search_for('firebug')
        search_page.sort_by('Newest')
        Assert.true('sort=created' in search_page.get_url_current_page())
        Assert.is_sorted_descending([i.created_date for i in search_page.results()])

    @xfail(reason="Bugzilla 698165")
    @nondestructive
    def test_sorting_by_most_recently_updated(self, mozwebqa):
        """
        Test for Litmus 17345.
        https://litmus.mozilla.org/show_test.cgi?id=17345
        """
        search_page = Home(mozwebqa).header.search_for('firebug')
        search_page.sort_by('Recently Updated')
        Assert.true('sort=updated' in search_page.get_url_current_page())
        results = [i.updated_date for i in search_page.results()]
        Assert.is_sorted_descending(results)
        search_page.page_forward()
        results.extend([i.updated_date for i in search_page.results()])
        Assert.is_sorted_descending(results)

    @nondestructive
    def test_sorting_by_number_of_most_users(self, mozwebqa):
        """
        Test for Litmus 24867.
        https://litmus.mozilla.org/show_test.cgi?id=24867
        """
        search_page = Home(mozwebqa).header.search_for('firebug')
        search_page.sort_by('Most Users')
        Assert.true('sort=users' in search_page.get_url_current_page())
        Assert.is_sorted_descending([i.users for i in search_page.results()])

    @nondestructive
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

    @nondestructive
    def test_that_search_results_return_20_results_per_page(self, mozwebqa):
        """
        Test for Litmus 17346.
        https://litmus.mozilla.org/show_test.cgi?id=17346
        """
        home_page = Home(mozwebqa)
        search_page = home_page.header.search_for('deutsch')

        first_expected = 1
        second_expected = 20

        while search_page.is_next_link_enabled:
            results_summary = search_page.results_displayed
            results = re.split('\W+', results_summary)
            first_count = results[1]
            second_count = results[2]

            Assert.equal(str(first_expected), first_count)
            Assert.equal(str(second_expected), second_count)
            Assert.equal(search_page.result_count, 20)

            search_page.page_forward()
            first_expected += 20
            second_expected += 20

        number = int(re.split('\W+', results_summary)[4]) % 20

        if number == 0:
            Assert.equal(search_page.result_count, 20)
        else:
            Assert.equal(search_page.result_count, number)

    @nondestructive
    def test_searching_for_collections_returns_results(self, mozwebqa):
        """
        Test for Litmus 17352.
        https://litmus.mozilla.org/show_test.cgi?id=17352
        """
        home_page = Home(mozwebqa)
        amo_collection_page = home_page.click_collections()
        amo_search_results_page = amo_collection_page.search_for('web')

        Assert.true(amo_search_results_page.result_count > 0)

    @nondestructive
    def test_searching_for_personas_returns_results(self, mozwebqa):
        """
        Test for Litmus 17349.
        https://litmus.mozilla.org/show_test.cgi?id=17349
        """
        amo_home_page = Home(mozwebqa)
        amo_personas_page = amo_home_page.click_personas()
        amo_personas_page.header.search_for('fox')

        Assert.true(amo_personas_page.persona_count > 0)

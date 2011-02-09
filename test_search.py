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
# Portions created by the Initial Developer are Copyright (C) 2010
# the Initial Developer. All Rights Reserved.
#
# Contributor(s): David Burns
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


from selenium import selenium
from vars import ConnectionParameters
import unittest2 as unittest
import re
from addons_site import AddonsHomePage
import sys
from nose.plugins.multiprocess import MultiProcess


class SearchTests(unittest.TestCase):
    
    _count_regex = '^.* (\d+) - (\d+)'
    _total_count_regex = '^.* \d+ - \d+ of (\d+)'

    def setUp(self):
        self.selenium = selenium(ConnectionParameters.server, 
                                ConnectionParameters.port,
                                ConnectionParameters.browser, 
                                ConnectionParameters.baseurl)
        self.selenium.start()
        self.selenium.set_timeout(ConnectionParameters.page_load_timeout)

    def tearDown(self):
        self.selenium.stop()

    def test_that_search_all_add_ons_results_have_pagination_that_moves_through_results(self):
        """ Test for litmus 4839 
            https://litmus.mozilla.org/show_test.cgi?id=4839
        """
        amo_home_page = AddonsHomePage(self.selenium)
        amo_search_page = amo_home_page.search_for("addon")
        first_expected = 1
        second_expected = 20
        
        # Go Forward 10 times
        for i in range(10):
            amo_search_page.page_forward()
            results_count = amo_search_page.results_count
            
            matches = re.search(self._count_regex, results_count)
            first_count = matches.group(1)
            second_count = matches.group(2)
            
            first_expected += 20
            second_expected += 20
            self.assertEqual(str(first_expected), first_count)
            self.assertEqual(str(second_expected), second_count)

        # Go Back 10 Times
        for i in range(10):
            amo_search_page.page_back()
            results_count = amo_search_page.results_count
            
            matches = re.search(self._count_regex, results_count)
            first_count = matches.group(1)
            second_count = matches.group(2)
            
            first_expected -= 20
            second_expected -= 20
            self.assertEqual(str(first_expected), first_count)
            self.assertEqual(str(second_expected), second_count)

    def test_that_character_escaping_doesnt_go_into_the_test(self):
        """ Test for Litmus 4857
            https://litmus.mozilla.org/show_test.cgi?id=4857"""
        amo_home_page = AddonsHomePage(self.selenium)
        amo_search_page = amo_home_page.search_for("personas%20plus")
        self.assertTrue(amo_search_page.is_text_present("No results found."))
        results_count = amo_search_page.results_count
        self.assertTrue("0 - 0 of 0" in results_count)

    def test_that_entering_a_long_string_returns_no_results(self):
        """ Litmus 4856
            https://litmus.mozilla.org/show_test.cgi?id=4856 """
        amo_home_page = AddonsHomePage(self.selenium)
        amo_search_page = amo_home_page.search_for("a" * 255)
        self.assertTrue(amo_search_page.is_text_present("No results found."))
        results_count = amo_search_page.results_count
        self.assertTrue("0 - 0 of 0" in results_count)

    def test_that_searching_with_unicode_characters_returns_results(self):
        """ Litmus 9575
            https://litmus.mozilla.org/show_test.cgi?id=9575 """
        amo_home_page = AddonsHomePage(self.selenium)
        search_str = u'\u0421\u043b\u043e\u0432\u0430\u0440\u0438 \u042f\u043d\u0434\u0435\u043a\u0441'
        amo_search_page = amo_home_page.search_for(search_str)
        self.assertTrue(amo_search_page.is_text_present(search_str)) 
        results_count = amo_search_page.results_count
        self.assertFalse("0 - 0 of 0" in results_count)

    def test_that_searching_with_substrings_returns_results(self):
        """ Litmus 9561
            https://litmus.mozilla.org/show_test.cgi?id=9561 """
        amo_home_page = AddonsHomePage(self.selenium)
        amo_search_page = amo_home_page.search_for("fox")
        self.assertFalse(amo_search_page.is_text_present("No results found."))
        results_count = amo_search_page.results_count
        self.assertFalse("0 - 0 of 0" in results_count)
        matches = re.search(self._total_count_regex, results_count)
        self.assertTrue(int(matches.group(1)) > 1)

if __name__ == "__main__":
    unittest.main()

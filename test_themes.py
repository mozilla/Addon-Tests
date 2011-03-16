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
# Contributor(s): David Burns, Marc George
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


class ThemeTests(unittest.TestCase):
    
    def setUp(self):
        self.selenium = selenium(ConnectionParameters.server, 
                                ConnectionParameters.port,
                                ConnectionParameters.browser, 
                                ConnectionParameters.baseurl)
        self.selenium.start()
        self.selenium.set_timeout(ConnectionParameters.page_load_timeout)

    def tearDown(self):
        self.selenium.stop()
        
    def test_that_themes_is_listed_as_a_category(self):
        """ Test for litmus 4839 
            https://litmus.mozilla.org/show_test.cgi?id=4839
        """
        amo_home_page = AddonsHomePage(self.selenium)
        self.assertTrue(amo_home_page.has_category("themes"))
        amo_home_page.click_category("themes")
        self.assertTrue(amo_home_page.current_page_is("themes"))

    def test_that_themes_can_be_sorted_by_name(self):
        """ Test for Litmus 11727 """
        amo_home_page = AddonsHomePage(self.selenium)
        amo_themes_page = amo_home_page.click_themes()
        amo_themes_page.click_sort_by("name")
        addons = amo_themes_page.addon_names
        addons_set = set(addons)
        self.assertEquals(len(addons), len(addons_set), "There are duplicates in the names")
        addons_orig = addons
        addons.sort()
        [self.assertEqual(addons_orig[i], addons[i]) for i in xrange(len(addons))]
        amo_themes_page.page_forward()
        addons = amo_themes_page.addon_names
        addons_set = set(addons)
        self.assertEquals(len(addons), len(addons_set), "There are duplicates in the names")
        addons_orig = addons
        addons.sort()
        [self.assertEqual(addons_orig[i], addons[i]) for i in xrange(len(addons))]



if __name__ == "__main__":
    unittest.main()

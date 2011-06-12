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
#                 Marc George
#                 Dave Hunt <dhunt@mozilla.com>
#                 Joel Andersson <janderssn@gmail.com>
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


from unittestzero import Assert

from addons_site import AddonsHomePage
import pytest
xfail = pytest.mark.xfail


class TestThemes:

    @xfail(reason="Test disabled due to bug 659290")
    def test_that_themes_can_be_sorted_by_name(self, testsetup):
        """ Test for Litmus 11727, 4839 """
        amo_home_page = AddonsHomePage(testsetup)
        amo_themes_page = amo_home_page.click_themes()
        amo_themes_page.click_sort_by("name")
        addons = amo_themes_page.addon_names
        addons_set = set(addons)
        Assert.equal(len(addons), len(addons_set), "There are duplicates in the names")
        addons_orig = addons
        addons.sort()
        [Assert.equal(addons_orig[i], addons[i]) for i in xrange(len(addons))]
        amo_themes_page.page_forward()
        addons = amo_themes_page.addon_names
        addons_set = set(addons)
        Assert.equal(len(addons), len(addons_set), "There are duplicates in the names")
        addons_orig = addons
        addons.sort()
        [Assert.equal(addons_orig[i], addons[i]) for i in xrange(len(addons))]

    def test_that_themes_can_be_sorted_by_updated_date(self, testsetup):
        """ test for litmus 11638 """
        amo_home_page = AddonsHomePage(testsetup)
        amo_themes_page = amo_home_page.click_themes()
        amo_themes_page.click_sort_by("updated")
        addons = amo_themes_page.addon_names
        addons_set = set(addons)
        Assert.equal(len(addons), len(addons_set), "There are duplicates in the names")
        updated_dates = amo_themes_page.addon_updated_dates
        Assert.is_sorted_descending(updated_dates)
        amo_themes_page.page_forward()
        updated_dates.extend(amo_themes_page.addon_updated_dates)
        Assert.is_sorted_descending(updated_dates)

    def test_that_themes_can_be_sorted_by_created_date(self, testsetup):
        """ test for litmus 11638 """
        amo_home_page = AddonsHomePage(testsetup)
        amo_themes_page = amo_home_page.click_themes()
        amo_themes_page.click_sort_by("created")
        addons = amo_themes_page.addon_names
        addons_set = set(addons)
        Assert.equal(len(addons), len(addons_set), "There are duplicates in the names")
        created_dates = amo_themes_page.addon_created_dates
        Assert.is_sorted_descending(created_dates)
        amo_themes_page.page_forward()
        created_dates.extend(amo_themes_page.addon_created_dates)
        Assert.is_sorted_descending(created_dates)

    def test_that_themes_can_be_sorted_by_popularity(self, testsetup):
        """ test for litmus 11638 """
        amo_home_page = AddonsHomePage(testsetup)
        amo_themes_page = amo_home_page.click_themes()
        amo_themes_page.click_sort_by("popular")
        addons = amo_themes_page.addon_names
        addons_set = set(addons)
        Assert.equal(len(addons), len(addons_set), "There are duplicates in the names")
        downloads = amo_themes_page.addon_download_number
        Assert.is_sorted_descending(downloads)
        amo_themes_page.page_forward()
        downloads.extend(amo_themes_page.addon_download_number)
        Assert.is_sorted_descending(downloads)

    @xfail(reason="Test disabled due to bug 663710")
    def test_that_themes_can_be_sorted_by_rating(self, testsetup):
        """ test for litmus 11638 """
        amo_home_page = AddonsHomePage(testsetup)
        amo_themes_page = amo_home_page.click_themes()
        amo_themes_page.click_sort_by("rating")
        addons = amo_themes_page.addon_names
        addons_set = set(addons)
        Assert.equal(len(addons), len(addons_set), "There are duplicates in the names")
        ratings = amo_themes_page.addon_rating
        Assert.is_sorted_descending(ratings)
        # find a page where not all themes have the same number of stars
        while (all([ratings[i] == ratings[i + 1] for i in xrange(len(ratings) - 1)])):
            amo_themes_page.page_forward()
            ratings.extend(amo_themes_page.addon_rating)
        # try one page more for good measure
        amo_themes_page.page_forward()
        ratings.extend(amo_themes_page.addon_rating)
        Assert.is_sorted_descending(ratings)

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
# Contributor(s): Teodosia Pop <teodosia.pop@softvision.ro>
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

from unittestzero import Assert
from addons_site import AddonsDetailsPage


class TestDetailsPage:

    def test_that_register_link_is_present_in_addon_details_page(self, testsetup):
        """ Test for Litmus 9890"""
        amo_details_page = AddonsDetailsPage(testsetup, "Firebug")
        Assert.true(amo_details_page.is_register_visible())
        Assert.equal(amo_details_page.register_link, "Register")

    def test_that_login_link_is_present_in_addon_details_page(self, testsetup):
        amo_details_page = AddonsDetailsPage(testsetup, "Firebug")
        Assert.true(amo_details_page.is_login_visible())
        Assert.equal(amo_details_page.login_link, "Log in")

    def test_that_dropdown_menu_is_present_after_click_on_other_apps(self, testsetup):
        amo_details_page = AddonsDetailsPage(testsetup, "Firebug")
        Assert.true(amo_details_page.is_other_apps_link_visible())
        Assert.equal(amo_details_page.other_apps, "Other Applications")
        Assert.true(amo_details_page.is_other_apps_dropdown_menu_visible())

    def test_that_addon_name_is_displayed(self, testsetup):
        amo_details_page = AddonsDetailsPage(testsetup, "Firebug")
        Assert.true(amo_details_page.is_addon_name_visible())
        # check that the name is not empty
        Assert.not_equal(amo_details_page.name, "")

    def test_that_summary_is_displayed(self, testsetup):
        amo_details_page = AddonsDetailsPage(testsetup, "Firebug")
        Assert.true(amo_details_page.is_summary_visible())
        # check that the summary is not empty
        Assert.not_none(re.match('(\w+\s*){3,}', amo_details_page.summary))

    def test_that_more_about_this_addon_is_displayed(self, testsetup):
        amo_details_page = AddonsDetailsPage(testsetup, "Firebug")
        Assert.true(amo_details_page.is_more_about_addon_visible())
        Assert.equal(amo_details_page.more_about_addon, "More about this add-on")
        Assert.not_none(re.match('(\w+\s*){3,}', amo_details_page.description))

    def test_that_release_notes_are_displayed(self, testsetup):
        amo_details_page = AddonsDetailsPage(testsetup, "Firebug")
        Assert.true(amo_details_page.are_release_notes_visible())
        Assert.equal(amo_details_page.release_notes, "Release Notes")
        Assert.not_none(re.match('\w+', amo_details_page.version_number))

    def test_that_reviews_are_displayed(self, testsetup):
        amo_details_page = AddonsDetailsPage(testsetup, "Firebug")
        Assert.true(amo_details_page.is_review_title_visible())
        Assert.equal(amo_details_page.review_title, "Reviews")
        Assert.not_none(re.match('(\w+\s*){3,}', amo_details_page.review_details))

    def test_that_other_addons_are_displayed(self, testsetup):
        amo_details_page = AddonsDetailsPage(testsetup, "Firebug")
        Assert.true(amo_details_page.are_other_addons_visible())

    def test_that_tags_are_displayed(self, testsetup):
        amo_details_page = AddonsDetailsPage(testsetup, "Firebug")
        Assert.true(amo_details_page.are_tags_visible())

    def test_other_collections_are_displayed(self, testsetup):
        amo_details_page = AddonsDetailsPage(testsetup, "Firebug")
        Assert.true(amo_details_page.are_other_collections_visible())

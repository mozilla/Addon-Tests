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
# Contributor(s): Bebe <florin.strugariu@softvision.ro>
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
from addons_site import AddonsDetailsPage


class TestAddonDetails:

    def test_other_addons_label_when_there_are_multiple_authors(self, testsetup):
        """
        Litmus 11926
        https://litmus.mozilla.org/show_test.cgi?id=11926
        """
        addon_with_multiple_authors = 'firebug'
        amo_detail_page = AddonsDetailsPage(testsetup, addon_with_multiple_authors)

        Assert.true(len(amo_detail_page.authors) > 1)
        Assert.equal(amo_detail_page.other_addons_by_authors_text, 'Other add-ons by these authors')

    def test_other_addons_label_when_there_is_only_one_author(self, testsetup):
        """
        Litmus 11926
        https://litmus.mozilla.org/show_test.cgi?id=11926
        """
        addon_with_one_authors = 'adblock-plus'
        amo_detail_page = AddonsDetailsPage(testsetup, addon_with_one_authors)

        Assert.equal(len(amo_detail_page.authors), 1)
        Assert.equal(amo_detail_page.other_addons_by_authors_text, "Other add-ons by %s" % amo_detail_page.authors[0])

    def test_navigating_to_other_addons_by_the_same_author_when_there_are_less_than_five_other_addons(self, testsetup):
        """
        Litmus 11926
        https://litmus.mozilla.org/show_test.cgi?id=1192"""
        addon_with_less_than_five_addons_by_the_same_author = 'adblock-plus'
        amo_detail_page = AddonsDetailsPage(testsetup, addon_with_less_than_five_addons_by_the_same_author)

        Assert.false(amo_detail_page.is_other_addons_dropdown_present)

        addons = amo_detail_page.other_addons_link_list()
        for i in range(amo_detail_page.other_addons_link_list_count):
            amo_detail_page.click_other_addon_by_this_author(addons[i])
            print addons[i]
            Assert.true(amo_detail_page.name.startswith(addons[i].rstrip('.')))
            AddonsDetailsPage(testsetup, addon_with_less_than_five_addons_by_the_same_author)

    def test_navigating_to_other_addons_by_the_same_author_when_there_are_more_than_five_other_addons(self, testsetup):
        """
        Litmus 11926
        https://litmus.mozilla.org/show_test.cgi?id=1192"""
        addon_with_more_than_five_addons_by_the_same_author = 'firebug'
        amo_detail_page = AddonsDetailsPage(testsetup, addon_with_more_than_five_addons_by_the_same_author)

        addons = amo_detail_page.other_addons_dropdown_values
        for i in range(len(addons) - 1, 0, -1):  # Not checking the first item in the drop-down https://bugzilla.mozilla.org/show_bug.cgi?id=660706
            amo_detail_page.select_other_addons_dropdown_value(addons[i])
            print addons[i]
            Assert.true(amo_detail_page.name.startswith(addons[i].rstrip('.')))
            AddonsDetailsPage(testsetup, addon_with_more_than_five_addons_by_the_same_author)

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
# Contributor(s): Marlena Compton <mcompton@mozilla.com>
#                 Bebe
#                 Geo Mealer <gmealer@mozilla.com>
#                 Teodosia Pop <teodosia.pop@softvision.ro>
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

import pytest

from unittestzero import Assert

from pages.home import Home


nondestructive = pytest.mark.nondestructive


class TestCategory:

    @nondestructive
    def test_that_all_category_links_work(self, mozwebqa):
        "Test for Litmus 25796"
        home_page = Home(mozwebqa)

        for i in range(len(home_page.categories)):
            category = home_page.categories[i]
            category_name = category.name
            category_page = category.click_link()
            Assert.contains(category_name, category_page.page_title)
            Assert.equal(category_name, category_page.category_header_title)
            home_page = Home(mozwebqa)

    @nondestructive
    def test_that_category_names_are_correct(self, mozwebqa):
        """Test for Litmus 25795"""

        expected_categories = [
            "Alerts & Updates",
            "Appearance",
            "Bookmarks",
            "Download Management",
            "Feeds, News & Blogging",
            "Games & Entertainment",
            "Language Support",
            "Photos, Music & Videos",
            "Privacy & Security",
            "Shopping",
            "Social & Communication",
            "Tabs",
            "Web Development",
            "Other"]

        # Get actual categories
        home_page = Home(mozwebqa)
        categories = home_page.categories

        # Catch extra/missing categories with a simple count check
        Assert.equal(len(categories), len(expected_categories))

        # Check the categories that are there against the expected list
        for category in categories:
            Assert.contains(category.name, expected_categories)

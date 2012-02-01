#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from unittestzero import Assert

from pages.home import Home


nondestructive = pytest.mark.nondestructive


class TestCategory:

    @nondestructive
    def test_that_all_category_links_work(self, mozwebqa):
        """Test for Litmus 25796."""
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
        """Test for Litmus 25795."""

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

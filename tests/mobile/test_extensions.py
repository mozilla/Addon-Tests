#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from unittestzero import Assert
from pages.mobile.home import Home


class TestExtensions:

    sort_options = ['Featured', 'Most Users', 'Top Rated', 'Newest', 'Name', 'Weekly Downloads', 'Recently Updated', 'Up & Coming']

    @pytest.mark.nondestructive
    def test_sort_by_region(self, mozwebqa):

        home = Home(mozwebqa)
        extensions_page = home.click_all_featured_addons_link()
        sort_menu = extensions_page.click_sort_by()
        Assert.true(sort_menu.is_extensions_dropdown_visible)

        actual_options = sort_menu.options
        expected_options = self.sort_options
        Assert.equal(len(actual_options), len(expected_options))

        for i in range(len(actual_options)):
            Assert.equal(actual_options[i].name, expected_options[i])
            Assert.true(actual_options[i].is_option_visible)

#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from unittestzero import Assert
from pages.home import Home

nondestructive = pytest.mark.nondestructive


class TestExtensions:

    @nondestructive
    def test_featured_tab_is_highlighted_by_default(self, mozwebqa):
        """
        Test for Litmus 29706.
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=29706
        """
        home_page = Home(mozwebqa)
        featured_extensions_page = home_page.header.application_masthead("Extensions").click()
        Assert.equal(featured_extensions_page.default_selected_tab, "Featured")

    @nondestructive
    def test_next_button_is_disabled_on_the_last_page(self, mozwebqa):
        """
        Test for Litmus 29710.
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=29710
        """
        home_page = Home(mozwebqa)
        featured_extensions_page = home_page.header.application_masthead("Extensions").click()
        featured_extensions_page.sort_by('most_users')
        featured_extensions_page.paginator.click_last_page()

        Assert.true(featured_extensions_page.paginator.is_next_page_disabled, 'Next button is available')

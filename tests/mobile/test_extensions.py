# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from pages.mobile.home import Home


class TestExtensions:

    sort_options = ['Featured', 'Most Users', 'Top Rated', 'Newest', 'Name', 'Weekly Downloads', 'Recently Updated', 'Up & Coming']

    @pytest.mark.nondestructive
    def test_sort_by_region(self, base_url, selenium):

        home = Home(base_url, selenium)
        extensions_page = home.click_all_featured_addons_link()
        sort_menu = extensions_page.click_sort_by()
        assert sort_menu.is_extensions_dropdown_visible

        actual_options = sort_menu.options
        expected_options = self.sort_options
        assert len(expected_options) == len(actual_options)

        for i in range(len(actual_options)):
            assert expected_options[i] == actual_options[i].name
            assert actual_options[i].is_option_visible

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.mobile.home import Home


class TestSearch:

    positive_search_term = "firefox"

    @pytest.mark.nondestructive
    def test_that_search_returns_results(self, base_url, selenium):
        home = Home(base_url, selenium)
        search_page = home.search_for(self.positive_search_term)
        assert len(search_page.results) > 0

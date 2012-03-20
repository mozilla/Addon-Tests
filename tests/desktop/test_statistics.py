#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from unittestzero import Assert
from pages.desktop.details import Details


class TestStatistics:

    @pytest.mark.nondestructive
    def test_that_verifies_the_url_of_the_statistics_page(self, mozwebqa):
        """ Test for Litmus 25710
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=25710
        """

        details_page = Details(mozwebqa, "Firebug")
        statistics_page = details_page.click_view_statistics()

        Assert.true(statistics_page.is_the_current_page)
        Assert.contains("/statistics", statistics_page.get_url_current_page())

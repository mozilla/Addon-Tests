#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import pytest

from unittestzero import Assert

from pages.desktop.home import Home


class TestInstalls:

    @pytest.mark.native
    @pytest.mark.nondestructive
    @pytest.mark.litmus(15115)
    def test_could_install_theme(self, mozwebqa):
        """note that this test does not actually *install* the theme"""

        home_page = Home(mozwebqa)
        complete_themes_page = home_page.header.click_complete_themes()
        complete_theme_page = complete_themes_page.click_on_first_addon()
        Assert.true(complete_theme_page.install_button_exists)

    @pytest.mark.nondestructive
    @pytest.mark.litmus(17355)
    def test_could_install_jetpack(self, mozwebqa):
        """note that this test does not actually *install* the jetpack"""

        home_page = Home(mozwebqa)
        search_page = home_page.search_for("jetpack")
        details_page = search_page.results.pop().click_result()
        Assert.true(details_page.is_version_information_install_button_visible)

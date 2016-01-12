# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import pytest


from pages.desktop.home import Home


class TestInstalls:

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_could_install_theme(self, base_url, selenium):
        """note that this test does not actually *install* the theme"""

        home_page = Home(base_url, selenium)
        complete_themes_page = home_page.header.click_complete_themes()
        complete_theme_page = complete_themes_page.click_on_first_addon()
        assert complete_theme_page.is_install_button_visible

    @pytest.mark.nondestructive
    def test_could_install_jetpack(self, base_url, selenium):
        """note that this test does not actually *install* the jetpack"""

        home_page = Home(base_url, selenium)
        search_page = home_page.search_for("jetpack")
        for result in search_page.results:
            # click on the first compatible result
            if result.is_compatible:
                details_page = result.click_result()
                break

        assert details_page.is_version_information_install_button_visible

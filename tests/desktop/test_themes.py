# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import pytest

from pages.desktop.home import Home
from pages.desktop.themes import Themes


class TestThemes:

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_page_title_for_themes_landing_page(self, base_url, selenium):
        home_page = Home(base_url, selenium)
        themes_page = home_page.header.site_navigation_menu('Themes').click()
        assert themes_page.is_the_current_page

    @pytest.mark.smoke
    @pytest.mark.nondestructive
    def test_the_featured_themes_section(self, base_url, selenium):
        page = Themes(base_url, selenium).open()
        assert 0 < len(page.featured_themes) <= 6

    @pytest.mark.smoke
    @pytest.mark.nondestructive
    def test_the_recently_added_section(self, base_url, selenium):
        page = Themes(base_url, selenium).open()
        assert 6 == len(page.recently_added_themes)

    @pytest.mark.smoke
    @pytest.mark.nondestructive
    def test_the_most_popular_section(self, base_url, selenium):
        page = Themes(base_url, selenium).open()
        assert 6 == len(page.most_popular_themes)

    @pytest.mark.nondestructive
    def test_the_top_rated_section(self, base_url, selenium):
        page = Themes(base_url, selenium).open()
        assert 6 == len(page.top_rated_themes)

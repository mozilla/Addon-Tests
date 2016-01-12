# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import random
import pytest


from pages.desktop.home import Home


class TestThemes:

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_start_exploring_link_in_the_promo_box(self, base_url, selenium):
        home_page = Home(base_url, selenium)
        themes_page = home_page.header.site_navigation_menu("Themes").click()
        assert themes_page.is_the_current_page
        assert themes_page.is_featured_addons_present
        browse_themes_page = themes_page.click_start_exploring()
        assert browse_themes_page.is_the_current_page
        assert 'up-and-coming' == browse_themes_page.sort_key
        assert 'Up & Coming' == browse_themes_page.sort_by

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_page_title_for_themes_landing_page(self, base_url, selenium):
        home_page = Home(base_url, selenium)
        themes_page = home_page.header.site_navigation_menu("Themes").click()
        assert themes_page.is_the_current_page

    @pytest.mark.native
    @pytest.mark.smoke
    @pytest.mark.nondestructive
    def test_the_featured_themes_section(self, base_url, selenium):
        home_page = Home(base_url, selenium)
        themes_page = home_page.header.site_navigation_menu("Themes").click()
        assert themes_page.is_the_current_page
        assert 0 < len(themes_page.featured_themes) <= 6

    @pytest.mark.native
    @pytest.mark.smoke
    @pytest.mark.nondestructive
    def test_the_recently_added_section(self, base_url, selenium):
        home_page = Home(base_url, selenium)
        themes_page = home_page.header.site_navigation_menu("Themes").click()
        assert themes_page.is_the_current_page
        assert 6 == themes_page.recently_added_count
        recently_added_dates = themes_page.recently_added_dates
        assert sorted(recently_added_dates, reverse=True) == recently_added_dates

    @pytest.mark.native
    @pytest.mark.smoke
    @pytest.mark.nondestructive
    def test_the_most_popular_section(self, base_url, selenium):
        home_page = Home(base_url, selenium)
        themes_page = home_page.header.site_navigation_menu("Themes").click()
        assert themes_page.is_the_current_page
        assert 6 == themes_page.most_popular_count
        downloads = themes_page.most_popular_downloads
        assert sorted(downloads, reverse=True) == downloads

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_the_top_rated_section(self, base_url, selenium):
        home_page = Home(base_url, selenium)
        themes_page = home_page.header.site_navigation_menu("Themes").click()
        assert themes_page.is_the_current_page
        assert 6 == themes_page.top_rated_count
        ratings = themes_page.top_rated_ratings
        assert sorted(ratings, reverse=True) == ratings

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_breadcrumb_menu_in_theme_details_page(self, base_url, selenium):

        # Step 1, 2: Access AMO Home, Click on theme category link.
        home_page = Home(base_url, selenium)
        themes_page = home_page.header.site_navigation_menu("Themes").click()
        assert themes_page.is_the_current_page

        # Step 3: Click on any featured theme.
        theme = random.choice(themes_page.featured_themes)
        themes_detail_page = theme.click()
        assert themes_detail_page.is_the_current_page

        # Verify breadcrumb menu format, i.e. Add-ons for Firefox > themes > {theme Name}.
        theme_title = themes_detail_page.title
        assert 'Add-ons for Firefox' == themes_detail_page.breadcrumbs[0].text
        assert 'Themes' == themes_detail_page.breadcrumbs[1].text

        theme_breadcrumb_title = len(theme_title) > 40 and '%s...' % theme_title[:40] or theme_title

        assert theme_breadcrumb_title == themes_detail_page.breadcrumbs[2].text

        # Step 4: Click on the links present in the Breadcrumb menu.
        # Verify that the themes link loads the themes home page.
        themes_detail_page.breadcrumbs[1].click()
        assert themes_page.is_the_current_page

        themes_page.return_to_previous_page()
        assert themes_detail_page.is_the_current_page

        # Verify that the Add-ons for Firefox link loads the AMO home page.
        themes_detail_page.breadcrumbs[0].click()
        assert home_page.is_the_current_page

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_themes_breadcrumb_format(self, base_url, selenium):
        home_page = Home(base_url, selenium)
        themes_page = home_page.header.site_navigation_menu("Themes").click()
        assert 'Add-ons for Firefox' == themes_page.breadcrumbs[0].text
        assert 'Themes' == themes_page.breadcrumbs[1].text

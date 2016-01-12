# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest


from pages.desktop.home import Home


class TestAmoLayout:

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_other_applications_thunderbird(self, base_url, selenium):
        app_under_test = "Thunderbird"
        home_page = Home(base_url, selenium)
        home_page.header.click_other_application(app_under_test)
        assert app_under_test.lower() in home_page.get_url_current_page()
        assert not home_page.header.is_other_application_visible(app_under_test)

    @pytest.mark.nondestructive
    def test_that_checks_amo_logo_text_layout_and_title(self, base_url, selenium):
        home_page = Home(base_url, selenium)
        assert 'ADD-ONS' == home_page.amo_logo_text
        assert 'Return to the Firefox Add-ons homepage' == home_page.amo_logo_title
        assert '/img/app-icons/med/firefox.png' in home_page.amo_logo_image_source

    @pytest.mark.nondestructive
    def test_that_clicking_the_amo_logo_loads_home_page(self, base_url, selenium):
        home_page = Home(base_url, selenium)
        assert home_page.is_amo_logo_visible
        home_page = home_page.click_amo_logo()
        assert home_page.is_the_current_page
        assert home_page.is_amo_logo_visible
        assert'%s/en-US/firefox/' % home_page.base_url == home_page.get_url_current_page()

    @pytest.mark.nondestructive
    def test_that_other_applications_link_has_tooltip(self, base_url, selenium):
        home_page = Home(base_url, selenium)
        tooltip = home_page.get_title_of_link('Other applications')
        assert 'Find add-ons for other applications' == tooltip

    @pytest.mark.action_chains
    @pytest.mark.nondestructive
    @pytest.mark.parametrize('expected_app', ["Thunderbird", "Android", "SeaMonkey"])
    def test_the_applications_listed_in_other_applications(self, base_url, selenium, expected_app):
        home_page = Home(base_url, selenium)
        assert home_page.header.is_other_application_visible(expected_app), '%s link not found in the Other Applications menu' % expected_app

    @pytest.mark.nondestructive
    def test_the_search_field_placeholder_and_search_button(self, base_url, selenium):
        home_page = Home(base_url, selenium)
        assert 'search for add-ons' == home_page.header.search_field_placeholder
        assert home_page.header.is_search_button_visible
        assert 'Search' == home_page.header.search_button_title

    @pytest.mark.nondestructive
    def test_the_search_box_exist(self, base_url, selenium):
        home_page = Home(base_url, selenium)
        assert home_page.header.is_search_textbox_visible

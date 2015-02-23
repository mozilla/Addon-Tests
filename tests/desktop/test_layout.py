#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from unittestzero import Assert

from pages.desktop.home import Home


class TestAmoLayout:

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_other_applications_thunderbird(self, mozwebqa):
        app_under_test = "Thunderbird"
        home_page = Home(mozwebqa)

        home_page.header.click_other_application(app_under_test)
        Assert.contains(app_under_test.lower(), home_page.get_url_current_page())

        Assert.false(home_page.header.is_other_application_visible(app_under_test))

    @pytest.mark.nondestructive
    def test_that_checks_amo_logo_text_layout_and_title(self, mozwebqa):
        home_page = Home(mozwebqa)
        Assert.equal(home_page.amo_logo_text, "ADD-ONS")
        Assert.equal(home_page.amo_logo_title, "Return to the Firefox Add-ons homepage")
        Assert.contains("/img/app-icons/med/firefox.png", home_page.amo_logo_image_source)

    @pytest.mark.nondestructive
    def test_that_clicking_the_amo_logo_loads_home_page(self, mozwebqa):
        home_page = Home(mozwebqa)

        Assert.true(home_page.is_amo_logo_visible)
        home_page = home_page.click_amo_logo()
        Assert.true(home_page.is_the_current_page)
        Assert.true(home_page.is_amo_logo_visible)
        Assert.equal(home_page.get_url_current_page(), '%s/en-US/firefox/' % home_page.base_url)

    @pytest.mark.nondestructive
    def test_that_other_applications_link_has_tooltip(self, mozwebqa):
        home_page = Home(mozwebqa)
        tooltip = home_page.get_title_of_link('Other applications')
        Assert.equal(tooltip, 'Find add-ons for other applications')

    @pytest.mark.action_chains
    @pytest.mark.nondestructive
    @pytest.mark.parametrize('expected_app', ["Thunderbird", "Android", "SeaMonkey"])
    def test_the_applications_listed_in_other_applications(self, mozwebqa, expected_app):
        home_page = Home(mozwebqa)

        Assert.true(home_page.header.is_other_application_visible(expected_app),
                    "%s link not found in the Other Applications menu" % expected_app)

    @pytest.mark.nondestructive
    def test_the_search_field_placeholder_and_search_button(self, mozwebqa):
        home_page = Home(mozwebqa)
        Assert.equal(home_page.header.search_field_placeholder, 'search for add-ons')
        Assert.true(home_page.header.is_search_button_visible)
        Assert.equal(home_page.header.search_button_title, 'Search')

    @pytest.mark.nondestructive
    def test_the_search_box_exist(self, mozwebqa):
        home_page = Home(mozwebqa)
        Assert.true(home_page.header.is_search_textbox_visible)

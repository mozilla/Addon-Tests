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
    @pytest.mark.xfail(reason="Fails sporadically; see https://www.pivotaltracker.com/story/show/23906697")
    def test_other_applications_thunderbird(self, mozwebqa):
        """
        Test for Litmus 5037.
        https://litmus.mozilla.org/show_test.cgi?id=5037
        """
        app_under_test = "Thunderbird"
        home_page = Home(mozwebqa)

        home_page.header.click_other_application(app_under_test)
        Assert.contains(app_under_test.lower(), home_page.get_url_current_page())

        Assert.false(home_page.header.is_other_application_visible(app_under_test))

    @pytest.mark.nondestructive
    def test_that_checks_amo_logo_text_layout_and_title(self, mozwebqa):
        """
        Test for Litmus 22924 and 25742.
        https://litmus.mozilla.org/show_test.cgi?id=22924
        https://litmus.mozilla.org/show_test.cgi?id=25742
        """
        home_page = Home(mozwebqa)
        Assert.equal(home_page.amo_logo_text, "ADD-ONS")
        Assert.equal(home_page.amo_logo_title, "Return to the Firefox Add-ons homepage")
        Assert.contains("-cdn.allizom.org/media/img/app-icons/med/firefox.png", home_page.amo_logo_image_source)

    @pytest.mark.nondestructive
    def test_that_clicking_the_amo_logo_loads_home_page(self, mozwebqa):
        """
        Test for Litmus 25743.
        https://litmus.mozilla.org/show_test.cgi?id=25743
        """
        home_page = Home(mozwebqa)

        Assert.true(home_page.is_amo_logo_visible)
        home_page = home_page.click_amo_logo()
        Assert.true(home_page.is_the_current_page)
        Assert.true(home_page.is_amo_logo_visible)
        Assert.equal(home_page.get_url_current_page(), '%s/en-US/firefox/' % home_page.base_url)

    @pytest.mark.nondestructive
    def test_that_clicking_mozilla_logo_loads_mozilla_dot_org(self, mozwebqa):
        """
        Test for Litmus 22922.
        https://litmus.mozilla.org/show_test.cgi?id=22922
        """
        home_page = Home(mozwebqa)
        Assert.true(home_page.is_mozilla_logo_visible)
        home_page.click_mozilla_logo()
        Assert.equal(home_page.get_url_current_page(), "http://www.mozilla.org/en-US/")

    @pytest.mark.nondestructive
    def test_that_other_applications_link_has_tooltip(self, mozwebqa):
        """
        Test for Litmus 22925.
        https://litmus.mozilla.org/show_test.cgi?id=29698
        """
        home_page = Home(mozwebqa)
        tooltip = home_page.get_title_of_link('Other applications')
        Assert.equal(tooltip, 'Find add-ons for other applications')

    @pytest.mark.native
    @pytest.mark.nondestructive
    @pytest.mark.xfail(reason="Fails sporadically, due to action chains; see https://www.pivotaltracker.com/projects/310523?story_id=27171441")
    @pytest.mark.parametrize('expected_app', ["Thunderbird", "Mobile", "SeaMonkey"])
    def test_the_applications_listed_in_other_applications(self, mozwebqa, expected_app):
        """
        Test for Litmus 25740.
        https://litmus.mozilla.org/show_test.cgi?id=25740
        """
        home_page = Home(mozwebqa)

        Assert.true(home_page.header.is_other_application_visible(expected_app), 
                "%s link not found in the Other Applications menu" % expected_app)

    @pytest.mark.nondestructive
    def test_the_search_field_placeholder_and_serch_button(self, mozwebqa):
        """
        Test for Litmus 4826 and 25767.
        https://litmus.mozilla.org/show_test.cgi?id=4826
        https://litmus.mozilla.org/show_test.cgi?id=25767
        """
        home_page = Home(mozwebqa)
        Assert.equal(home_page.header.search_field_placeholder, 'search for add-ons')
        Assert.true(home_page.header.is_search_button_visible)
        Assert.equal(home_page.header.search_button_title, 'Search')

    @pytest.mark.nondestructive
    def test_the_search_box_exist(self, mozwebqa):
        """
        Test for Litmus 25766
        https://litmus.mozilla.org/show_test.cgi?id=25766
        """
        home_page = Home(mozwebqa)
        Assert.true(home_page.header.is_search_textbox_visible)

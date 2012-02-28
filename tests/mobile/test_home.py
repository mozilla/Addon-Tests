#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from unittestzero import Assert
from pages.mobile.home import Home


class TestHome:

    expected_menu_items = ['MOZILLA FIREFOX', 'FEATURES', 'DESKTOP', 'ADD-ONS', 'SUPPORT', 'VISIT MOZILLA']

    @pytest.mark.nondestructive
    def test_that_checks_the_desktop_version_link(self, mozwebqa):
        home = Home(mozwebqa)
        Assert.true(home.is_the_current_page)

        Assert.equal('VIEW FULL SITE', home.footer.desktop_version_text)

        home_desktop = home.footer.click_desktop_version()
        Assert.true(home_desktop.is_the_current_page)

    @pytest.mark.nondestructive
    def test_that_checks_the_header_menu(self, mozwebqa):
        home = Home(mozwebqa)
        Assert.true(home.is_the_current_page)

        Assert.equal('FIREFOX ADD-ONS', home.header_text)
        Assert.equal('Return to the Firefox Add-ons homepage', home.header_title)
        Assert.equal('Easy ways to personalize.', home.header_statement_text)

        Assert.equal(u'Learn More\xbb', home.learn_more_text)
        home.click_learn_more()

        Assert.true(home.is_learn_more_msg_visible)
        Assert.equal("Add-ons are applications that let you personalize Firefox with extra functionality and style. Whether you mistype the name of a website or can't read a busy page, there's an add-on to improve your on-the-go browsing.",
                     home.learn_more_msg_text)

    @pytest.mark.nondestructive
    def test_that_checks_the_footer_items(self, mozwebqa):
        home = Home(mozwebqa)
        Assert.true(home.is_the_current_page)

        Assert.true(home.footer.is_other_language_dropdown_visible)
        Assert.equal('Other languages', home.footer.other_language_text)
        Assert.equal('Privacy Policy', home.footer.privacy_text)
        Assert.equal('Legal Notices', home.footer.legal_text)

    @pytest.mark.nondestructive
    def test_that_checks_the_search_box_and_button(self, mozwebqa):
        """
        Test for Litmus 15128.
        https://litmus.mozilla.org/show_test.cgi?id=15128
        """
        home = Home(mozwebqa)
        Assert.true(home.is_the_current_page)

        Assert.true(home.is_search_box_visible)
        Assert.equal('search for add-ons', home.search_box_placeholder)
        Assert.true(home.is_search_button_visible)

    @pytest.mark.nondestructive
    def test_expandable_header(self, mozwebqa):
        """
        Litmus 15128
        https://litmus.mozilla.org/show_test.cgi?id=15128
        """
        home = Home(mozwebqa)
        home.header.click()
        Assert.true(home.is_dropdown_menu_visible)

        menu_names = [str(menu.name) for menu in home.header.dropdown_menu_items]
        Assert.equal(menu_names, self.expected_menu_items)

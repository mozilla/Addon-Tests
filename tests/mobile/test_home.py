#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from unittestzero import Assert
from pages.mobile.home import Home


class TestHome:

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
    def test_all_featured_extensions_link(self, mozwebqa):
        """
        litmus 15136
        https://litmus.mozilla.org/show_test.cgi?id=15136
        """

        home = Home(mozwebqa)
        Assert.true(home.is_the_current_page)
        featured_extensions = home.click_all_featured_addons_link()

        Assert.equal(featured_extensions.page_header, 'Featured Extensions')
        Assert.contains('sort=featured', featured_extensions.get_url_current_page())

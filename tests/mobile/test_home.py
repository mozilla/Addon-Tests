#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from unittestzero import Assert
from pages.mobile.home import Home


class TestHome:

    expected_menu_items = ['MOZILLA FIREFOX', 'FEATURES', 'DESKTOP', 'ADD-ONS', 'SUPPORT', 'VISIT MOZILLA']

    expected_tabs = ['Featured', 'Categories', 'Personas']

    expected_category_items = ['Alerts & Updates', 'Appearance', 'Bookmarks', 'Download Management',
                               'Feeds, News & Blogging', 'Games & Entertainment', 'Language Support',
                               'Photos, Music & Videos', 'Privacy & Security', 'Shopping', 'Social & Communication',
                               'Tabs', 'Web Development', 'Other']

    @pytest.mark.xfail(reason='Bug 788152 - View mobile site\View full site links are not working as expected')
    @pytest.mark.nondestructive
    def test_that_checks_the_desktop_version_link(self, mozwebqa):
        home = Home(mozwebqa)
        Assert.true(home.is_the_current_page)

        Assert.equal('VIEW FULL SITE', home.footer.desktop_version_text)

        home_desktop = home.footer.click_desktop_version()
        Assert.true(home_desktop.is_the_current_page)

    @pytest.mark.nondestructive
    def test_that_checks_header_text_and_page_title(self, mozwebqa):
        """
        litmus 15128
        https://litmus.mozilla.org/show_test.cgi?id=15128
        """
        home = Home(mozwebqa)
        Assert.true(home.is_the_current_page)

        Assert.equal('FIREFOX ADD-ONS', home.header_text)
        Assert.equal('Return to the Firefox Add-ons homepage', home.header_title)
        Assert.equal('Easy ways to personalize.', home.header_statement_text)

    @pytest.mark.nondestructive
    def test_that_checks_learn_more_link(self, mozwebqa):
        home = Home(mozwebqa)
        Assert.true(home.is_the_current_page)

        Assert.equal(u'Learn More\xbb', home.learn_more_text)
        home.click_learn_more()

        Assert.true(home.is_learn_more_msg_visible)
        Assert.equal("Add-ons are applications that let you personalize Firefox with extra functionality and style. Whether you mistype the name of a website or can't read a busy page, there's an add-on to improve your on-the-go browsing.",
                     home.learn_more_msg_text)

    @pytest.mark.nondestructive
    def test_that_checks_the_firefox_logo(self, mozwebqa):
        """
        litmus 15128
        https://litmus.mozilla.org/show_test.cgi?id=15128
        """

        home = Home(mozwebqa)
        Assert.true(home.is_the_current_page)

        Assert.true(home.is_header_firefox_logo_visible)
        Assert.contains('firefox.png', home.firefox_header_logo_src)

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
        Assert.equal(home.default_selected_tab_text, 'Featured')

        home.scroll_down  # workaround for selenium scroll issue

        featured_extensions = home.click_all_featured_addons_link()

        Assert.equal(featured_extensions.title, 'ADD-ONS')
        Assert.equal(featured_extensions.page_header, 'Featured Extensions')
        Assert.contains('sort=featured', featured_extensions.get_url_current_page())

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
        home.header.click_header_menu()
        Assert.true(home.header.is_dropdown_menu_visible)

        menu_names = [menu.name for menu in home.header.dropdown_menu_items]
        Assert.equal(menu_names, self.expected_menu_items)

    @pytest.mark.xfail(reason='Bug 824471 - New Personas tab on mobile site not working as expected')
    # https://bugzilla.mozilla.org/show_bug.cgi?id=824471
    def test_that_checks_the_tabs(self, mozwebqa):
        """
        Test for Litmus 15128.
        https://litmus.mozilla.org/show_test.cgi?id=15128
        """
        home = Home(mozwebqa)
        Assert.true(home.is_the_current_page)

        Assert.equal(3, len(home.tabs))

        for tab in reversed(range(len(home.tabs))):
            Assert.equal(self.expected_tabs[tab], home.tabs[tab].name)
            home.tabs[tab].click()
            Assert.true(home.tabs[tab].is_tab_selected, "The tab '%s' is not selected." % home.tabs[tab].name)
            Assert.true(home.tabs[tab].is_tab_content_visible,
                        "The content of tab '%s' is not visible." % home.tabs[tab].name)

    @pytest.mark.nondestructive
    def test_the_amo_logo_text_and_title(self, mozwebqa):
        """
        Test for Litmus 15128.
        https://litmus.mozilla.org/show_test.cgi?id=15128
        """
        home = Home(mozwebqa)
        Assert.true(home.is_the_current_page)

        Assert.equal('Return to the Firefox Add-ons homepage', home.logo_title)
        Assert.equal('FIREFOX ADD-ONS', home.logo_text)
        Assert.contains('/media/img/zamboni/app_icons/firefox.png', home.logo_image_src)
        Assert.equal('Easy ways to personalize.', home.subtitle)

    @pytest.mark.nondestructive
    def test_category_items(self, mozwebqa):
        """
        https://www.pivotaltracker.com/story/show/26074381
        """
        home = Home(mozwebqa)
        home.tab('Categories').click()
        Assert.true(home.is_categories_region_visible)

        for i in range(len(home.categories)):
            Assert.equal(home.categories[i].name, self.expected_category_items[i])

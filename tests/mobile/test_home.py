# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from pages.mobile.home import Home
from pages.mobile.themes import Themes


class TestHome:

    expected_menu_items = ['MOZILLA FIREFOX', 'FEATURES', 'DESKTOP', 'ADD-ONS', 'SUPPORT', 'VISIT MOZILLA']

    expected_tabs = ['Featured', 'Categories', 'Themes']

    expected_category_items = ['Alerts & Updates', 'Appearance', 'Bookmarks', 'Download Management',
                               'Feeds, News & Blogging', 'Games & Entertainment', 'Language Support',
                               'Photos, Music & Videos', 'Privacy & Security', 'Search Tools', 'Shopping',
                               'Social & Communication', 'Tabs', 'Web Development', 'Other']

    @pytest.mark.nondestructive
    def test_that_checks_the_desktop_version_link(self, base_url, selenium):
        home = Home(base_url, selenium)
        assert home.is_the_current_page
        assert 'VIEW FULL SITE' == home.footer.desktop_version_text

        home_desktop = home.footer.click_desktop_version()
        assert home_desktop.is_the_current_page

    @pytest.mark.nondestructive
    def test_that_checks_header_text_and_page_title(self, base_url, selenium):
        home = Home(base_url, selenium)
        assert home.is_the_current_page
        assert 'ADD-ONS' == home.header_text
        assert 'Return to the Firefox Add-ons homepage' == home.header_title
        assert 'Easy ways to personalize.' == home.header_statement_text

    @pytest.mark.nondestructive
    def test_that_checks_learn_more_link(self, base_url, selenium):
        home = Home(base_url, selenium)
        assert home.is_the_current_page
        assert u'Learn More\xbb' == home.learn_more_text

        home.click_learn_more()
        assert home.is_learn_more_msg_visible
        assert ('Add-ons are applications that let you personalize Firefox '
                'with extra functionality and style. Whether you mistype the '
                'name of a website or can\'t read a busy page, there\'s an '
                'add-on to improve your on-the-go browsing.' == home.learn_more_msg_text)

    @pytest.mark.nondestructive
    def test_that_checks_the_firefox_logo(self, base_url, selenium):
        home = Home(base_url, selenium)
        assert home.is_the_current_page
        assert home.is_header_firefox_logo_visible
        assert 'firefox.png' in home.firefox_header_logo_src

    @pytest.mark.nondestructive
    def test_that_checks_the_footer_items(self, base_url, selenium):
        home = Home(base_url, selenium)
        assert home.is_the_current_page
        assert home.footer.is_other_language_dropdown_visible
        assert 'Other languages' == home.footer.other_language_text
        assert 'Privacy Policy' == home.footer.privacy_text
        assert 'Legal Notices' == home.footer.legal_text

    @pytest.mark.nondestructive
    def test_all_featured_extensions_link(self, base_url, selenium):
        home = Home(base_url, selenium)
        assert home.is_the_current_page
        assert 'Featured' == home.default_selected_tab_text

        featured_extensions = home.click_all_featured_addons_link()
        assert 'ADD-ONS' == featured_extensions.title
        assert 'Featured Extensions' == featured_extensions.page_header
        assert 'sort=featured' in featured_extensions.get_url_current_page()

    @pytest.mark.nondestructive
    def test_that_checks_the_search_box_and_button(self, base_url, selenium):
        home = Home(base_url, selenium)
        assert home.is_the_current_page
        assert home.is_search_box_visible
        assert 'search for add-ons' == home.search_box_placeholder
        assert home.is_search_button_visible

    @pytest.mark.nondestructive
    def test_expandable_header(self, base_url, selenium):
        home = Home(base_url, selenium)
        home.header.click_header_menu()
        assert home.header.is_dropdown_menu_visible
        menu_names = [menu.name for menu in home.header.dropdown_menu_items]
        assert self.expected_menu_items == menu_names

    def test_that_checks_the_tabs(self, base_url, selenium):
        home = Home(base_url, selenium)
        assert home.is_the_current_page
        assert 3 == len(home.tabs)

        # Ignore the last tab "Themes" because it redirects to another page
        for tab in reversed(range(len(home.tabs[:-1]))):
            assert self.expected_tabs[tab] == home.tabs[tab].name
            home.tabs[tab].click()
            assert home.tabs[tab].is_tab_selected, "The tab '%s' is not selected." % home.tabs[tab].name
            assert home.tabs[tab].is_tab_content_visible, "The content of tab '%s' is not visible." % home.tabs[tab].name

        # Click on the themes tab separately
        home.tabs[-1].click()
        themes = Themes(base_url, selenium)
        themes.is_the_current_page

    @pytest.mark.nondestructive
    def test_the_amo_logo_text_and_title(self, base_url, selenium):
        home = Home(base_url, selenium)
        assert home.is_the_current_page
        assert 'Return to the Firefox Add-ons homepage', home.logo_title
        assert 'ADD-ONS', home.logo_text
        assert '/img/zamboni/app_icons/firefox.png' in home.logo_image_src
        assert 'Easy ways to personalize.' == home.subtitle

    @pytest.mark.nondestructive
    def test_category_items(self, base_url, selenium):
        home = Home(base_url, selenium)
        home.tab('Categories').click()
        assert home.is_categories_region_visible
        for i in range(len(home.categories)):
            assert self.expected_category_items[i] == home.categories[i].name

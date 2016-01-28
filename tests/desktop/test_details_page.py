# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import re
import pytest

from pages.desktop.details import Details
from pages.desktop.extensions import ExtensionsHome
from pages.desktop.home import Home


class TestDetails:

    @pytest.mark.login
    @pytest.mark.nondestructive
    def test_that_register_login_link_is_present_in_addon_details_page(self, base_url, selenium):
        details_page = Details(base_url, selenium, "Firebug")
        assert details_page.header.is_register_link_visible, 'Register link is not visible'
        assert details_page.header.is_login_link_visible, 'Login links is not visible'

    @pytest.mark.action_chains
    @pytest.mark.nondestructive
    def test_that_dropdown_menu_is_present_after_click_on_other_apps(self, base_url, selenium):
        details_page = Details(base_url, selenium, "Firebug")
        assert 'Other Applications' == details_page.header.menu_name
        details_page.header.hover_over_other_apps_menu()
        assert details_page.header.is_other_apps_dropdown_menu_visible

    @pytest.mark.nondestructive
    def test_that_addon_name_is_displayed(self, base_url, selenium):
        details_page = Details(base_url, selenium, "Firebug")
        # check that the name is not empty
        assert not details_page.title == ''

    @pytest.mark.nondestructive
    def test_that_summary_is_displayed(self, base_url, selenium):
        details_page = Details(base_url, selenium, "Firebug")
        # check that the summary is not empty
        assert re.match('(\w+\s*){3,}', details_page.summary) is not None

    @pytest.mark.nondestructive
    def test_that_about_this_addon_is_displayed(self, base_url, selenium):
        details_page = Details(base_url, selenium, "Firebug")
        assert 'About this Add-on' == details_page.about_addon
        assert re.match('(\w+\s*){3,}', details_page.description) is not None

    @pytest.mark.action_chains
    @pytest.mark.nondestructive
    def test_that_version_information_is_displayed(self, base_url, selenium):
        details_page = Details(base_url, selenium, 'Firebug')
        assert 'Version Information' == details_page.version_information_heading

        details_page.expand_version_information()
        assert details_page.is_version_information_section_expanded
        assert details_page.is_source_code_license_information_visible
        assert details_page.is_whats_this_license_visible
        assert details_page.is_view_the_source_link_visible
        assert details_page.is_complete_version_history_visible
        assert details_page.is_version_information_install_button_visible
        # check that the release number matches the version number at the top of the page
        assert 'Version %s' % details_page.version_number == details_page.release_version

    @pytest.mark.smoke
    @pytest.mark.nondestructive
    def test_that_reviews_are_displayed(self, base_url, selenium):
        details_page = Details(base_url, selenium, "Firebug")
        assert 'Reviews' == details_page.review_title
        assert details_page.has_reviews
        for review in details_page.review_details:
            assert review is not None

    @pytest.mark.nondestructive
    def test_that_tags_are_displayed(self, base_url, selenium):
        details_page = Details(base_url, selenium, "Firebug")
        assert details_page.are_tags_visible

    @pytest.mark.nondestructive
    def test_part_of_collections_are_displayed(self, base_url, selenium):
        details_page = Details(base_url, selenium, "Firebug")
        assert 'Part of these Collections' == details_page.part_of_collections_header
        assert len(details_page.part_of_collections) > 0

    @pytest.mark.nondestructive
    def test_that_external_link_leads_to_addon_website(self, base_url, selenium):
        # Step 1 - Open AMO Home
        # Step 2 - Open MemChaser Plus details page
        details_page = Details(base_url, selenium, 'MemChaser')
        website_link = details_page.website
        assert not website_link == ''
        # Step 3 - Follow external website link
        details_page.click_website_link()
        assert details_page.get_url_current_page() in website_link

    @pytest.mark.nondestructive
    def test_that_whats_this_link_for_source_license_links_to_an_answer_in_faq(self, base_url, selenium):
        details_page = Details(base_url, selenium, "Firebug")
        details_page.expand_version_information()
        user_faq_page = details_page.click_whats_this_license()
        assert re.match('(\w+\s*){3,}', user_faq_page.license_question) is not None
        assert re.match('(\w+\s*){3,}', user_faq_page.license_answer) is not None

    @pytest.mark.nondestructive
    def test_other_addons_label_when_there_are_multiple_authors(self, base_url, selenium):
        addon_with_multiple_authors = 'firebug'
        detail_page = Details(base_url, selenium, addon_with_multiple_authors)
        assert len(detail_page.authors) > 1
        assert 'Other add-ons by these authors' == detail_page.other_addons_by_authors_text

    @pytest.mark.nondestructive
    def test_other_addons_label_when_there_is_only_one_author(self, base_url, selenium):
        addon_with_one_author = 'MemChaser'
        detail_page = Details(base_url, selenium, addon_with_one_author)
        assert len(detail_page.authors) == 1
        assert 'Other add-ons by %s' % detail_page.authors[0] == detail_page.other_addons_by_authors_text

    @pytest.mark.nondestructive
    def test_navigating_to_other_addons(self, base_url, selenium):
        detail_page = Details(base_url, selenium, 'firebug')
        for i in range(0, len(detail_page.other_addons)):
            name = detail_page.other_addons[i].name
            detail_page.other_addons[i].click_addon_link()
            assert name in detail_page.title
            Details(base_url, selenium, 'firebug')

    @pytest.mark.nondestructive
    def test_open_close_functionality_for_image_viewer(self, base_url, selenium):
        detail_page = Details(base_url, selenium, 'firebug')
        image_viewer = detail_page.previewer.click_image()
        assert image_viewer.is_visible
        image_viewer.close()
        assert not image_viewer.is_visible

    @pytest.mark.nondestructive
    def test_navigation_buttons_for_image_viewer(self, base_url, selenium):
        detail_page = Details(base_url, selenium, 'firebug')
        images_count = detail_page.previewer.image_count
        image_set_count = detail_page.previewer.image_set_count
        images_title = []
        image_link = []
        for img_set in range(image_set_count):
            for img_no in range(3):
                if img_set * 3 + img_no != images_count:
                    images_title.append(detail_page.previewer.image_title(img_set * 3 + img_no))
                    image_link.append(detail_page.previewer.image_link(img_set * 3 + img_no))

            detail_page.previewer.next_set()

        for img_set in range(image_set_count):
            detail_page.previewer.prev_set()

        image_viewer = detail_page.previewer.click_image()
        assert image_viewer.is_visible
        assert images_count == image_viewer.images_count
        for i in range(image_viewer.images_count):
            assert image_viewer.is_visible
            assert images_title[i] == image_viewer.caption
            assert image_link[i].split('/')[-1] == image_viewer.image_link.split('/')[-1]

            if not i == 0:
                assert image_viewer.is_previous_present
            else:
                assert not image_viewer.is_previous_present

            if not i == image_viewer.images_count - 1:
                assert image_viewer.is_next_present
                image_viewer.click_next()
            else:
                assert not image_viewer.is_next_present

        for i in range(image_viewer.images_count - 1, -1, -1):
            assert image_viewer.is_visible
            assert images_title[i] == image_viewer.caption
            assert image_link[i].split('/')[-1] == image_viewer.image_link.split('/')[-1]

            if not i == image_viewer.images_count - 1:
                assert image_viewer.is_next_present
            else:
                assert not image_viewer.is_next_present

            if not i == 0:
                assert image_viewer.is_previous_present
                image_viewer.click_previous()
            else:
                assert not image_viewer.is_previous_present

    @pytest.mark.nondestructive
    def test_that_review_usernames_are_clickable(self, base_url, selenium):
        addon_name = 'firebug'
        detail_page = Details(base_url, selenium, addon_name)

        for i in range(0, len(detail_page.reviews)):
            username = detail_page.reviews[i].username
            amo_user_page = detail_page.reviews[i].click_username()
            assert username == amo_user_page.username
            Details(base_url, selenium, addon_name)

    @pytest.mark.nondestructive
    def test_that_details_page_has_breadcrumb(self, base_url, selenium):
        detail_page = Details(base_url, selenium, 'firebug')
        assert 'Add-ons for Firefox' == detail_page.breadcrumbs[0].text
        assert 'Extensions' == detail_page.breadcrumbs[1].text
        assert 'Firebug' == detail_page.breadcrumbs[2].text

    @pytest.mark.nondestructive
    def test_that_clicking_info_link_slides_down_page_to_version_info(self, base_url, selenium):
        details_page = Details(base_url, selenium, 'firebug')
        details_page.click_version_info_link()
        assert details_page.version_info_link == details_page.version_information_href
        assert details_page.is_version_information_section_expanded
        assert details_page.is_version_information_section_in_view

    @pytest.mark.nondestructive
    def test_that_breadcrumb_links_in_details_page_work(self, base_url, selenium):
        home_page = Home(base_url, selenium)
        detail_page = Details(base_url, selenium, 'firebug')

        assert 'Add-ons for Firefox' == detail_page.breadcrumbs[0].text
        link = detail_page.breadcrumbs[0].href_value
        detail_page.breadcrumbs[0].click()

        assert home_page.is_the_current_page
        assert home_page.get_url_current_page().endswith(link)

        home_page.return_to_previous_page()

        assert 'Extensions' == detail_page.breadcrumbs[1].text
        link = detail_page.breadcrumbs[1].href_value
        detail_page.breadcrumbs[1].click()

        amo_extensions_page = ExtensionsHome(base_url, selenium)
        assert amo_extensions_page.is_the_current_page
        assert amo_extensions_page.get_url_current_page().endswith(link)

        home_page.return_to_previous_page()
        assert 'Firebug' == detail_page.breadcrumbs[2].text

    @pytest.mark.nondestructive
    @pytest.mark.login
    def test_that_add_a_review_button_works(self, base_url, selenium, existing_user):
        # Step 1: Addons Home Page loads and Addons Details loads
        home_page = Home(base_url, selenium)

        # Step 2:user logs in to submit a review
        home_page.login(existing_user['email'], existing_user['password'])
        assert home_page.header.is_user_logged_in

        # Step 3: user loads an addon details page and clicks write a review button
        details_page = Details(base_url, selenium, 'Firebug')
        review_box = details_page.click_to_write_review()
        assert review_box.is_review_box_visible

    @pytest.mark.nondestructive
    def test_the_developers_comments_section(self, base_url, selenium):
        details_page = Details(base_url, selenium, 'Firebug')
        assert u'Developer\u2019s Comments' == details_page.devs_comments_title
        details_page.expand_devs_comments()
        assert details_page.is_devs_comments_section_expanded
        assert re.match('(\w+\s*){3,}', details_page.devs_comments_message) is not None

    @pytest.mark.smoke
    @pytest.mark.nondestructive
    def test_that_add_to_collection_flyout_for_anonymous_users(self, base_url, selenium):
        details_page = Details(base_url, selenium, 'Firebug')
        details_page.click_add_to_collection_widget()
        assert 'Create an Add-ons Account' == details_page.collection_widget_button
        assert 'log in to your current account' == details_page.collection_widget_login_link

    @pytest.mark.nondestructive
    def test_that_the_development_channel_expands(self, base_url, selenium):
        details_page = Details(base_url, selenium, 'Firebug')
        assert 'Development Channel' == details_page.development_channel_text
        assert '' == details_page.development_channel_content
        details_page.click_development_channel()
        assert details_page.development_channel_content is not None
        details_page.click_development_channel()
        assert '' == details_page.development_channel_content

    @pytest.mark.nondestructive
    def test_click_on_other_collections(self, base_url, selenium):
        details_pg = Details(base_url, selenium, 'Firebug')
        for i in range(0, len(details_pg.part_of_collections)):
            name = details_pg.part_of_collections[i].name
            collection_pg = details_pg.part_of_collections[i].click_collection()
            assert name == collection_pg.collection_name, 'Expected collection name does not match the page header'
            details_pg = Details(base_url, selenium, 'Firebug')

    @pytest.mark.nondestructive
    def test_the_development_channel_section(self, base_url, selenium):
        details_page = Details(base_url, selenium, 'Firebug')
        assert 'Development Channel' == details_page.development_channel_text
        details_page.click_development_channel()

        # Verify if description present
        assert details_page.development_channel_content is not None
        assert details_page.is_development_channel_install_button_visible

        # Verify experimental version (beta or pre)
        assert re.match('Version\s\d+\.\d+\.\d+[a|b|rc]\d+\:', details_page.beta_version) is not None

    @pytest.mark.nondestructive
    def test_that_license_link_works(self, base_url, selenium):
        addon_name = 'Firebug'
        details_page = Details(base_url, selenium, addon_name)
        assert 'BSD License' == details_page.license_link_text
        license_link = details_page.license_site
        assert license_link is not None

    @pytest.mark.nondestructive
    def test_that_clicking_user_reviews_slides_down_page_to_reviews_section(self, base_url, selenium):
        details_page = Details(base_url, selenium, 'firebug')
        details_page.click_user_reviews_link()
        assert details_page.is_reviews_section_visible
        assert details_page.is_reviews_section_in_view

    @pytest.mark.action_chains
    @pytest.mark.nondestructive
    def test_that_install_button_is_clickable(self, base_url, selenium):
        details_page = Details(base_url, selenium, 'firebug')
        assert 'active' in details_page.click_and_hold_install_button_returns_class_value()

    @pytest.mark.nondestructive
    def test_what_is_this_in_the_version_information(self, base_url, selenium):
        details_page = Details(base_url, selenium, "Firebug")
        assert 'Version Information' == details_page.version_information_heading
        details_page.expand_version_information()
        assert 'What\'s this?' == details_page.license_faq_text
        license_faq = details_page.click_whats_this_license()
        assert 'Frequently Asked Questions' == license_faq.header_text

    @pytest.mark.nondestructive
    def test_view_the_source_in_the_version_information(self, base_url, selenium):
        details_page = Details(base_url, selenium, "Firebug")
        assert 'Version Information' == details_page.version_information_heading
        details_page.expand_version_information()
        assert 'View the source' == details_page.view_source_code_text
        view_source = details_page.click_view_source_code()
        assert '/files/browse/' in view_source.get_url_current_page()

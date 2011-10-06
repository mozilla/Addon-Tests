#!/usr/bin/env python

# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is Mozilla WebQA Selenium Tests.
#
# The Initial Developer of the Original Code is
# Mozilla.
# Portions created by the Initial Developer are Copyright (C) 2011
# the Initial Developer. All Rights Reserved.
#
# Contributor(s): Teodosia Pop <teodosia.pop@softvision.ro>
#                 Bebe <florin.strugariu@softvision.ro>
#                 Alex Rodionov <p0deje@gmail.com>
#                 Alin Trif <alin.trif@softvision.ro>
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
#
# ***** END LICENSE BLOCK *****


import re
import pytest
xfail = pytest.mark.xfail

from unittestzero import Assert
from addons_site import UserFAQPage
from details_page import DetailsPage
from user_page import LoginPage
from extensions_homepage import ExtensionsHomePage
from homepage import HomePage



class TestDetailsPage:

    def test_that_register_link_is_present_in_addon_details_page(self, mozwebqa):
        """ Test for Litmus 9890"""
        details_page = DetailsPage(mozwebqa, "Firebug")
        Assert.true(details_page.is_register_visible)
        Assert.equal(details_page.register_link, "Register")

    def test_that_login_link_is_present_in_addon_details_page(self, mozwebqa):
        """ Test for Litmus 9890"""
        details_page = DetailsPage(mozwebqa, "Firebug")
        Assert.true(details_page.is_login_visible)
        Assert.equal(details_page.login_link, "Log in")

    def test_that_dropdown_menu_is_present_after_click_on_other_apps(self, mozwebqa):
        """ Test for Litmus 9890"""
        details_page = DetailsPage(mozwebqa, "Firebug")
        Assert.true(details_page.is_other_apps_link_visible)
        Assert.equal(details_page.other_apps, "Other Applications")
        #TODO: Fix when the hover event works
        #Assert.true(details_page.is_other_apps_dropdown_menu_visible

    def test_that_addon_name_is_displayed(self, mozwebqa):
        """ Test for Litmus 9890"""
        details_page = DetailsPage(mozwebqa, "Firebug")
        Assert.true(details_page.is_addon_name_visible)
        # check that the name is not empty
        Assert.not_equal(details_page.name, "")

    def test_that_summary_is_displayed(self, mozwebqa):
        """ Test for Litmus 9890"""
        details_page = DetailsPage(mozwebqa, "Firebug")
        Assert.true(details_page.is_summary_visible)
        # check that the summary is not empty
        Assert.not_none(re.match('(\w+\s*){3,}', details_page.summary))

    def test_that_about_this_addon_is_displayed(self, mozwebqa):
        """ Test for Litmus 9890"""
        details_page = DetailsPage(mozwebqa, "Firebug")
        Assert.true(details_page.is_about_addon_visible)
        Assert.equal(details_page.about_addon, "About this Add-on")
        Assert.not_none(re.match('(\w+\s*){3,}', details_page.description))

    # TODO expand the Version Information section and check that the required details are present/visible/correct
    def test_that_version_information_is_displayed(self, mozwebqa):
        """ Test for Litmus 9890"""
        details_page = DetailsPage(mozwebqa, "Firebug")
        Assert.true(details_page.is_version_information_heading_visible)
        Assert.equal(details_page.version_information_heading, "Version Information")
        Assert.not_none(re.search('\w+', details_page.release_version))
        Assert.not_none(re.search('\w+', details_page.source_code_license_information))
        # check that the release number matches the the version number at the top of the page
        Assert.not_none(re.search(details_page.version_number, details_page.release_version))

    def test_that_reviews_are_displayed(self, mozwebqa):
        """ Test for Litmus 9890"""
        details_page = DetailsPage(mozwebqa, "Firebug")
        Assert.true(details_page.is_review_title_visible)
        Assert.equal(details_page.review_title, "Reviews")
        Assert.true(details_page.has_reviews)
        Assert.not_none(re.search('(\w+\s*){1,}', details_page.review_details))

    def test_that_in_often_used_with_addons_are_displayed(self, mozwebqa):
        """ Test for Litmus 9890"""
        details_page = DetailsPage(mozwebqa, "Firebug")
        Assert.true(details_page.is_often_used_with_header_visible)
        Assert.equal(details_page.often_used_with_header, u"Often used with\u2026")
        Assert.true(details_page.is_often_used_with_list_visible)

    def test_that_tags_are_displayed(self, mozwebqa):
        """ Test for Litmus 9890"""
        details_page = DetailsPage(mozwebqa, "Firebug")
        Assert.true(details_page.are_tags_visible)

    def test_part_of_collections_are_displayed(self, mozwebqa):
        """ Test for Litmus 9890"""
        details_page = DetailsPage(mozwebqa, "Firebug")
        Assert.true(details_page.is_part_of_collections_header_visible)
        Assert.true(details_page.is_part_of_collections_list_visible)
        Assert.equal(details_page.part_of_collections_header, 'Part of these Collections')

    def test_that_external_link_leads_to_addon_website(self, mozwebqa):
        """ Litmus 11809
            https://litmus.mozilla.org/show_test.cgi?id=11809 """
        # Step 1 - Open AMO homepage
        # Step 2 - Open Adblock Plus details page
        details_page = DetailsPage(mozwebqa, 'Adblock Plus')
        website_link = details_page.website
        Assert.true(website_link != '')
        # Step 3 - Follow external website link
        details_page.click_website_link()
        Assert.true(website_link in details_page.get_url_current_page())

    def test_that_whats_this_link_for_source_license_links_to_an_answer_in_faq(self, mozwebqa):
        """ Test for Litmus 11530"""
        details_page = DetailsPage(mozwebqa, "Firebug")
        user_faq_page = details_page.click_whats_this_license()
        Assert.not_none(re.match('(\w+\s*){3,}', user_faq_page.license_question))
        Assert.not_none(re.match('(\w+\s*){3,}', user_faq_page.license_answer))

    def test_other_addons_label_when_there_are_multiple_authors(self, mozwebqa):
        """
        Litmus 11926
        https://litmus.mozilla.org/show_test.cgi?id=11926
        """
        addon_with_multiple_authors = 'firebug'
        detail_page = DetailsPage(mozwebqa, addon_with_multiple_authors)

        Assert.true(len(detail_page.authors) > 1)
        Assert.equal(detail_page.other_addons_by_authors_text, 'Other add-ons by these authors')

    def test_other_addons_label_when_there_is_only_one_author(self, mozwebqa):
        """
        Litmus 11926
        https://litmus.mozilla.org/show_test.cgi?id=11926
        """
        addon_with_one_authors = 'adblock-plus'
        detail_page = DetailsPage(mozwebqa, addon_with_one_authors)

        Assert.equal(len(detail_page.authors), 1)
        Assert.equal(detail_page.other_addons_by_authors_text, "Other add-ons by %s" % detail_page.authors[0])

    def test_navigating_to_other_addons(self, mozwebqa):
        """
        Litmus 11926
        https://litmus.mozilla.org/show_test.cgi?id=11926"""
        addon_name = 'firebug'
        detail_page = DetailsPage(mozwebqa, addon_name)

        addons = detail_page.other_addons()
        for addon in addons:
            name = addon.name
            addon.click_addon_link()
            Assert.contains(name, detail_page.name)
            detail_page = DetailsPage(mozwebqa, addon_name)

    def test_details_more_images(self, mozwebqa):
        """
        Litmus 4846
        https://litmus.mozilla.org/show_test.cgi?id=4846
        """
        detail_page = DetailsPage(mozwebqa, 'firebug')

        image_viewer = detail_page.previewer.click_image()
        Assert.true(image_viewer.is_visible)
        image_viewer.close()
        Assert.false(image_viewer.is_visible)

        images_count = detail_page.previewer.image_count
        image_set_count = detail_page.previewer.image_set_count
        images_title = []
        image_link = []
        for img_set in range(image_set_count):
            for img_no in range(3):
                if img_set * 3 + img_no != images_count:
                    images_title.append(detail_page.previewer.image_title(img_set * 3 + img_no))
                    image_link.append(detail_page.previewer.image_link(img_set * 3 + img_no))

            image_viewer = detail_page.previewer.next_set()

        image_viewer = detail_page.previewer.click_image()
        Assert.true(image_viewer.is_visible)
        Assert.equal(images_count, image_viewer.images_count)
        for i in range(image_viewer.images_count):
            Assert.true(image_viewer.is_visible)

            Assert.equal(image_viewer.caption, images_title[i])
            Assert.equal(image_viewer.image_link.split('/')[8], image_link[i].split('/')[8])

            if not i == 0:
                Assert.true(image_viewer.is_previous_present)
            else:
                Assert.false(image_viewer.is_previous_present)

            if not i == image_viewer.images_count - 1:
                Assert.true(image_viewer.is_next_present)
                image_viewer.click_next()
            else:
                Assert.false(image_viewer.is_next_present)

        for i in range(image_viewer.images_count - 1, -1, -1):
            Assert.true(image_viewer.is_visible)

            Assert.equal(image_viewer.caption, images_title[i])
            Assert.equal(image_viewer.image_link.split('/')[8], image_link[i].split('/')[8])

            if not i == image_viewer.images_count - 1:
                Assert.true(image_viewer.is_next_present)
            else:
                Assert.false(image_viewer.is_next_present)

            if not i == 0:
                Assert.true(image_viewer.is_previous_present)
                image_viewer.click_previous()
            else:
                Assert.false(image_viewer.is_previous_present)

        image_viewer.close()
        Assert.false(image_viewer.is_visible)

    @xfail(reason="Flaky test")
    def test_that_review_usernames_are_clickable(self, mozwebqa):
        """
        Litmus 4842
        https://litmus.mozilla.org/show_test.cgi?id=4842
        """
        addon_name = 'firebug'
        detail_page = DetailsPage(mozwebqa, addon_name)

        for review in detail_page.reviews():
            username = review.username
            amo_user_page = review.click_username()
            Assert.equal(username, amo_user_page.username)
            DetailsPage(mozwebqa, addon_name)

    def test_that_details_page_has_breadcrumb(self, mozwebqa):
        """
        Litmus 11922
        https://litmus.mozilla.org/show_test.cgi?id=11922
        """
        detail_page = DetailsPage(mozwebqa, 'firebug')

        Assert.equal(detail_page.breadcrumb, 'Add-ons for Firefox Extensions Firebug')

    def test_that_clicking_info_link_slides_down_page_to_version_info(self, mozwebqa):
        """ Test for Litmus 25725
            https://litmus.mozilla.org/show_test.cgi?id=25725 """
        details_page = DetailsPage(mozwebqa, 'firebug')
        Assert.true(details_page.is_version_info_link_visible)
        details_page.click_version_info_link()
        Assert.equal(details_page.version_info_link, details_page.version_information)
        Assert.true(details_page.is_version_information_section_expanded)
        Assert.true(details_page.does_page_scroll_to_version_information_section)

    def test_that_breadcrumb_links_in_details_page_work(self, mozwebqa):
        """
        Litmus 11923
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=11923
        """
        home_page = HomePage(mozwebqa)
        detail_page = DetailsPage(mozwebqa, 'firebug')

        Assert.true(detail_page.is_breadcrumb_menu_visible)

        Assert.equal(detail_page.breadcrumbs[0].name, 'Add-ons for Firefox')
        link = detail_page.breadcrumbs[0].link_value
        detail_page.breadcrumbs[0].click()

        Assert.true(home_page.is_the_current_page)
        Assert.true(home_page.get_url_current_page().endswith(link))

        home_page.return_to_previous_page()

        Assert.equal(detail_page.breadcrumbs[1].name, 'Extensions')
        link = detail_page.breadcrumbs[1].link_value
        detail_page.breadcrumbs[1].click()

        amo_extenstions_page = ExtensionsHomePage(mozwebqa)
        Assert.true(amo_extenstions_page.is_the_current_page)
        Assert.true(amo_extenstions_page.get_url_current_page().endswith(link))

        home_page.return_to_previous_page()

        Assert.equal(detail_page.breadcrumbs[2].name, 'Firebug')

    def test_that_add_a_review_button_works(self, mozwebqa):
        """
        Litmus 25729
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=25729
        """
        #Step 1: Addons Home Page loads and Addons Details loads
        home_page = HomePage(mozwebqa)

        #Step 2:user logs in to submit a review
        home_page.login()
        Assert.true(home_page.header.is_user_logged_in)

        #Step 3: user loads an addon details page and clicks write a review button
        details_page = DetailsPage(mozwebqa, 'Firebug')
        review_box = details_page.click_to_write_review()
        Assert.true(review_box.is_review_box_visible)

    def test_the_developers_comments_section(self, mozwebqa):
        """ 
        Test for Litmus 25724
        https://litmus.mozilla.org/show_test.cgi?id=25724 
        """
        details_page = DetailsPage(mozwebqa, 'Firebug')
        Assert.true(details_page.is_devs_comments_section_visible)
        Assert.equal(details_page.devs_comments_title, u"Developer\u2019s Comments")
        details_page.click_devs_comments_title()
        Assert.true(details_page.is_devs_comments_section_expanded())
        Assert.not_none(details_page.devs_comments_message)

    def test_that_add_to_collection_flyout_for_anonymous_users(self, mozwebqa):
        """
        Litmus 25711
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=25711
        """
        details_page = DetailsPage(mozwebqa, 'Firebug')
        details_page.click_add_to_collection_widget()
        Assert.true(details_page.is_collection_widget_visible)
        Assert.true(details_page.is_collection_widget_button_visible)
        Assert.equal(details_page.collection_widget_button, 'Create an Add-ons Account')
        Assert.true(details_page.is_collection_widget_login_link_visible)
        Assert.equal(details_page.collection_widget_login_link, 'log in to your current account')

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
from addons_details_page import AddonsDetailsPage
from addons_user_page import AddonsLoginPage
from addons_site import ExtensionsHomePage
from addons_homepage import AddonsHomePage


class TestDetailsPage:

    def test_that_register_link_is_present_in_addon_details_page(self, mozwebqa):
        """ Test for Litmus 9890"""
        amo_details_page = AddonsDetailsPage(mozwebqa, "Firebug")
        Assert.true(amo_details_page.is_register_visible)
        Assert.equal(amo_details_page.register_link, "Register")

    def test_that_login_link_is_present_in_addon_details_page(self, mozwebqa):
        """ Test for Litmus 9890"""
        amo_details_page = AddonsDetailsPage(mozwebqa, "Firebug")
        Assert.true(amo_details_page.is_login_visible)
        Assert.equal(amo_details_page.login_link, "Log in")

    def test_that_dropdown_menu_is_present_after_click_on_other_apps(self, mozwebqa):
        """ Test for Litmus 9890"""
        amo_details_page = AddonsDetailsPage(mozwebqa, "Firebug")
        Assert.true(amo_details_page.is_other_apps_link_visible)
        Assert.equal(amo_details_page.other_apps, "Other Applications")
        #TODO: Fix when the hover event works
        #Assert.true(amo_details_page.is_other_apps_dropdown_menu_visible

    def test_that_addon_name_is_displayed(self, mozwebqa):
        """ Test for Litmus 9890"""
        amo_details_page = AddonsDetailsPage(mozwebqa, "Firebug")
        Assert.true(amo_details_page.is_addon_name_visible)
        # check that the name is not empty
        Assert.not_equal(amo_details_page.name, "")

    def test_that_summary_is_displayed(self, mozwebqa):
        """ Test for Litmus 9890"""
        amo_details_page = AddonsDetailsPage(mozwebqa, "Firebug")
        Assert.true(amo_details_page.is_summary_visible)
        # check that the summary is not empty
        Assert.not_none(re.match('(\w+\s*){3,}', amo_details_page.summary))

    def test_that_about_this_addon_is_displayed(self, mozwebqa):
        """ Test for Litmus 9890"""
        amo_details_page = AddonsDetailsPage(mozwebqa, "Firebug")
        Assert.true(amo_details_page.is_about_addon_visible)
        Assert.equal(amo_details_page.about_addon, "About this Add-on")
        Assert.not_none(re.match('(\w+\s*){3,}', amo_details_page.description))

    @xfail(reason="bugzilla 688917")
    # TODO expand the Version Information section and check that the required details are present/visible/correct
    def test_that_version_information_is_displayed(self, mozwebqa):
        """ Test for Litmus 9890"""
        amo_details_page = AddonsDetailsPage(mozwebqa, "Firebug")
        Assert.true(amo_details_page.is_version_information_heading_visible)
        Assert.equal(amo_details_page.version_information_heading, "Version Information")
        Assert.not_none(re.search('\w+', amo_details_page.release_version))

        # check that the release number matches the the version number at the top of the page
        Assert.not_none(re.search(amo_details_page.version_number, amo_details_page.release_version))

    def test_that_reviews_are_displayed(self, mozwebqa):
        """ Test for Litmus 9890"""
        amo_details_page = AddonsDetailsPage(mozwebqa, "Firebug")
        Assert.true(amo_details_page.is_review_title_visible)
        Assert.equal(amo_details_page.review_title, "Reviews")
        Assert.true(amo_details_page.has_reviews)
        Assert.not_none(re.search('(\w+\s*){1,}', amo_details_page.review_details))

    def test_that_in_often_used_with_addons_are_displayed(self, mozwebqa):
        """ Test for Litmus 9890"""
        amo_details_page = AddonsDetailsPage(mozwebqa, "Firebug")
        Assert.true(amo_details_page.is_often_used_with_header_visible)
        Assert.equal(amo_details_page.often_used_with_header, u"Often used with\u2026")
        Assert.true(amo_details_page.is_often_used_with_list_visible)

    def test_that_tags_are_displayed(self, mozwebqa):
        """ Test for Litmus 9890"""
        amo_details_page = AddonsDetailsPage(mozwebqa, "Firebug")
        Assert.true(amo_details_page.are_tags_visible)

    def test_part_of_collections_are_displayed(self, mozwebqa):
        """ Test for Litmus 9890"""
        amo_details_page = AddonsDetailsPage(mozwebqa, "Firebug")
        Assert.true(amo_details_page.is_part_of_collections_header_visible)
        Assert.true(amo_details_page.is_part_of_collections_list_visible)
        Assert.equal(amo_details_page.part_of_collections_header, 'Part of these Collections')

    def test_that_external_link_leads_to_addon_website(self, mozwebqa):
        """ Litmus 11809
            https://litmus.mozilla.org/show_test.cgi?id=11809 """
        # Step 1 - Open AMO homepage
        # Step 2 - Open Adblock Plus details page
        details_page = AddonsDetailsPage(mozwebqa, 'Adblock Plus')
        website_link = details_page.website
        Assert.true(website_link != '')
        # Step 3 - Follow external website link
        details_page.click_website_link()
        Assert.true(website_link in details_page.get_url_current_page())

    @xfail(reason="bugzilla 688910")
    def test_that_whats_this_link_for_source_license_links_to_an_answer_in_faq(self, mozwebqa):
        """ Test for Litmus 11530"""
        amo_details_page = AddonsDetailsPage(mozwebqa, "Firebug")
        user_faq_page = amo_details_page.click_whats_this_license()
        Assert.not_none(re.match('(\w+\s*){3,}', user_faq_page.license_question))
        Assert.not_none(re.match('(\w+\s*){3,}', user_faq_page.license_answer))

    def test_other_addons_label_when_there_are_multiple_authors(self, mozwebqa):
        """
        Litmus 11926
        https://litmus.mozilla.org/show_test.cgi?id=11926
        """
        addon_with_multiple_authors = 'firebug'
        amo_detail_page = AddonsDetailsPage(mozwebqa, addon_with_multiple_authors)

        Assert.true(len(amo_detail_page.authors) > 1)
        Assert.equal(amo_detail_page.other_addons_by_authors_text, 'Other add-ons by these authors')

    def test_other_addons_label_when_there_is_only_one_author(self, mozwebqa):
        """
        Litmus 11926
        https://litmus.mozilla.org/show_test.cgi?id=11926
        """
        addon_with_one_authors = 'adblock-plus'
        amo_detail_page = AddonsDetailsPage(mozwebqa, addon_with_one_authors)

        Assert.equal(len(amo_detail_page.authors), 1)
        Assert.equal(amo_detail_page.other_addons_by_authors_text, "Other add-ons by %s" % amo_detail_page.authors[0])

    def test_navigating_to_other_addons(self, mozwebqa):
        """
        Litmus 11926
        https://litmus.mozilla.org/show_test.cgi?id=11926"""
        addon_name = 'firebug'
        amo_detail_page = AddonsDetailsPage(mozwebqa, addon_name)

        addons = amo_detail_page.other_addons()
        for addon in addons:
            name = addon.name
            addon.click_addon_link()
            Assert.contains(name, amo_detail_page.name)
            amo_detail_page = AddonsDetailsPage(mozwebqa, addon_name)

    def test_details_more_images(self, mozwebqa):
        """
        Litmus 4846
        https://litmus.mozilla.org/show_test.cgi?id=4846
        """
        amo_detail_page = AddonsDetailsPage(mozwebqa, 'firebug')

        image_viewer = amo_detail_page.previewer.click_image()
        Assert.true(image_viewer.is_visible)
        image_viewer.close()
        Assert.false(image_viewer.is_visible)

        images_count = amo_detail_page.previewer.image_count
        image_set_count = amo_detail_page.previewer.image_set_count
        images_title = []
        image_link = []
        for img_set in range(image_set_count):
            for img_no in range(3):
                if img_set * 3 + img_no != images_count:
                    images_title.append(amo_detail_page.previewer.image_title(img_set * 3 + img_no))
                    image_link.append(amo_detail_page.previewer.image_link(img_set * 3 + img_no))

            image_viewer = amo_detail_page.previewer.next_set()

        image_viewer = amo_detail_page.previewer.click_image()
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
        amo_detail_page = AddonsDetailsPage(mozwebqa, addon_name)

        for review in amo_detail_page.reviews():
            username = review.username
            amo_user_page = review.click_username()
            Assert.equal(username, amo_user_page.username)
            AddonsDetailsPage(mozwebqa, addon_name)

    def test_that_details_page_has_breadcrumb(self, mozwebqa):
        """
        Litmus 11922
        https://litmus.mozilla.org/show_test.cgi?id=11922
        """
        amo_detail_page = AddonsDetailsPage(mozwebqa, 'firebug')

        Assert.equal(amo_detail_page.breadcrumb, 'Add-ons for Firefox Extensions Firebug')

    def test_that_clicking_info_link_slides_down_page_to_version_info(self, mozwebqa):
        """ Test for Litmus 25725
            https://litmus.mozilla.org/show_test.cgi?id=25725 """
        amo_details_page = AddonsDetailsPage(mozwebqa, 'firebug')
        Assert.true(amo_details_page.is_version_info_link_visible)
        amo_details_page.click_version_info_link()
        Assert.equal(amo_details_page.version_info_link, amo_details_page.version_information)
        Assert.true(amo_details_page.is_version_information_section_expanded)
        Assert.true(amo_details_page.does_page_scroll_to_version_information_section)

    def test_that_breadcrumb_links_in_addons_details_page_work(self, mozwebqa):
        """
        Litmus 11923
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=11923
        """
        amo_home_page = AddonsHomePage(mozwebqa)
        amo_detail_page = AddonsDetailsPage(mozwebqa, 'firebug')

        Assert.true(amo_detail_page.is_breadcrumb_menu_visible)

        Assert.equal(amo_detail_page.breadcrumbs[0].name, 'Add-ons for Firefox')
        link = amo_detail_page.breadcrumbs[0].link_value
        amo_detail_page.breadcrumbs[0].click()

        Assert.true(amo_home_page.is_the_current_page)
        Assert.true(amo_home_page.get_url_current_page().endswith(link))

        amo_home_page.return_to_previous_page()

        Assert.equal(amo_detail_page.breadcrumbs[1].name, 'Extensions')
        link = amo_detail_page.breadcrumbs[1].link_value
        amo_detail_page.breadcrumbs[1].click()

        amo_extenstions_page = ExtensionsHomePage(mozwebqa)
        Assert.true(amo_extenstions_page.is_the_current_page)
        Assert.true(amo_extenstions_page.get_url_current_page().endswith(link))

        amo_home_page.return_to_previous_page()

        Assert.equal(amo_detail_page.breadcrumbs[2].name, 'Firebug')

    def test_that_add_a_review_button_works(self, mozwebqa):
        """
        Litmus 25729
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=25729
        """
        #Step 1: Addons Home Page loads and Addons Details loads
        amo_home_page = AddonsHomePage(mozwebqa)

        #Step 2:user logs in to submit a review
        amo_home_page.login()
        Assert.true(amo_home_page.header.is_user_logged_in)

        #Step 3: user loads an addon details page and clicks write a review button
        amo_details_page = AddonsDetailsPage(mozwebqa, 'Firebug')
        addon_review_box = amo_details_page.click_to_write_review()
        Assert.true(addon_review_box.is_review_box_visible)

    def test_that_add_to_collection_flyout_for_anonymous_users(self, mozwebqa):
        """
        Litmus 25711
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=25711
        """
        amo_details_page = AddonsDetailsPage(mozwebqa, 'Firebug')
        amo_details_page.click_add_to_collection_widget()
        Assert.true(amo_details_page.is_collection_widget_visible)
        Assert.true(amo_details_page.is_collection_widget_button_visible)
        Assert.equal(amo_details_page.collection_widget_button, 'Create an Add-ons Account')
        Assert.true(amo_details_page.is_collection_widget_login_link_visible)
        Assert.equal(amo_details_page.collection_widget_login_link, 'log in to your current account')

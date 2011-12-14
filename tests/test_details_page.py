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

from unittestzero import Assert

from pages.details import Details
from pages.extensions import ExtensionsHome
from pages.home import Home

nondestructive = pytest.mark.nondestructive


class TestDetails:

    @nondestructive
    def test_that_register_login_link_is_present_in_addon_details_page(self, mozwebqa):
        """ Test for Litmus 9890"""
        details_page = Details(mozwebqa, "Firebug")
        Assert.equal(details_page.register_link, "Log in / Register", "Login / Register text does not match the expected one")

    @nondestructive
    def test_that_dropdown_menu_is_present_after_click_on_other_apps(self, mozwebqa):
        """ Test for Litmus 9890"""
        details_page = Details(mozwebqa, "Firebug")
        Assert.equal(details_page.other_apps, "Other Applications")
        #TODO: Fix when the hover event works
        #Assert.true(details_page.is_other_apps_dropdown_menu_visible

    @nondestructive
    def test_that_addon_name_is_displayed(self, mozwebqa):
        """ Test for Litmus 9890"""
        details_page = Details(mozwebqa, "Firebug")
        # check that the name is not empty
        Assert.not_none(details_page.title, "")

    @nondestructive
    def test_that_summary_is_displayed(self, mozwebqa):
        """ Test for Litmus 9890"""
        details_page = Details(mozwebqa, "Firebug")
        # check that the summary is not empty
        Assert.not_none(re.match('(\w+\s*){3,}', details_page.summary))

    @nondestructive
    def test_that_about_this_addon_is_displayed(self, mozwebqa):
        """ Test for Litmus 9890"""
        details_page = Details(mozwebqa, "Firebug")
        Assert.equal(details_page.about_addon, "About this Add-on")
        Assert.not_none(re.match('(\w+\s*){3,}', details_page.description))

    @nondestructive
    def test_that_version_information_is_displayed(self, mozwebqa):
        """ Test for Litmus 9890"""
        details_page = Details(mozwebqa, 'Firebug')
        Assert.equal(details_page.version_information_heading, 'Version Information')
        """
        Updated for Litmus 25721
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=25721
        """

        details_page.click_version_information_header()
        Assert.true(details_page.is_version_information_section_expanded)
        Assert.true(details_page.is_source_code_license_information_visible)
        Assert.true(details_page.is_whats_this_license_visible)
        Assert.true(details_page.is_view_the_source_link_visible)
        Assert.true(details_page.is_complete_version_history_visible)
        Assert.true(details_page.is_version_information_install_button_visible)
        # check that the release number matches the version number at the top of the page
        Assert.equal('Version %s' % details_page.version_number, details_page.release_version)

    @nondestructive
    def test_that_reviews_are_displayed(self, mozwebqa):
        """ Test for Litmus 9890"""
        details_page = Details(mozwebqa, "Firebug")
        Assert.equal(details_page.review_title, "Reviews")
        Assert.true(details_page.has_reviews)
        Assert.not_none(re.search('(\w+\s*){1,}', details_page.review_details))

    @nondestructive
    def test_that_in_often_used_with_addons_are_displayed(self, mozwebqa):
        """ Test for Litmus 9890"""
        details_page = Details(mozwebqa, "Firebug")
        Assert.equal(details_page.often_used_with_header, u"Often used with\u2026")
        Assert.true(details_page.is_often_used_with_list_visible)

    @nondestructive
    def test_that_tags_are_displayed(self, mozwebqa):
        """ Test for Litmus 9890"""
        details_page = Details(mozwebqa, "Firebug")
        Assert.true(details_page.are_tags_visible)

    @nondestructive
    def test_part_of_collections_are_displayed(self, mozwebqa):
        """ Test for Litmus 9890"""
        details_page = Details(mozwebqa, "Firebug")
        Assert.equal(details_page.part_of_collections_header, 'Part of these Collections')
        Assert.true(len(details_page.part_of_collections) > 0)

    @nondestructive
    def test_that_external_link_leads_to_addon_website(self, mozwebqa):
        """ Litmus 11809
            https://litmus.mozilla.org/show_test.cgi?id=11809 """
        # Step 1 - Open AMO Home
        # Step 2 - Open Adblock Plus details page
        details_page = Details(mozwebqa, 'Adblock Plus')
        website_link = details_page.website
        Assert.true(website_link != '')
        # Step 3 - Follow external website link
        details_page.click_website_link()
        Assert.true(website_link in details_page.get_url_current_page())

    @nondestructive
    def test_that_whats_this_link_for_source_license_links_to_an_answer_in_faq(self, mozwebqa):
        """ Test for Litmus 11530"""
        details_page = Details(mozwebqa, "Firebug")
        details_page.click_version_information_heading()
        user_faq_page = details_page.click_whats_this_license()
        Assert.not_none(re.match('(\w+\s*){3,}', user_faq_page.license_question))
        Assert.not_none(re.match('(\w+\s*){3,}', user_faq_page.license_answer))

    @nondestructive
    def test_other_addons_label_when_there_are_multiple_authors(self, mozwebqa):
        """
        Litmus 11926
        https://litmus.mozilla.org/show_test.cgi?id=11926
        """
        addon_with_multiple_authors = 'firebug'
        detail_page = Details(mozwebqa, addon_with_multiple_authors)

        Assert.true(len(detail_page.authors) > 1)
        Assert.equal(detail_page.other_addons_by_authors_text, 'Other add-ons by these authors')

    @nondestructive
    def test_other_addons_label_when_there_is_only_one_author(self, mozwebqa):
        """
        Litmus 11926
        https://litmus.mozilla.org/show_test.cgi?id=11926
        """
        addon_with_one_authors = 'F1 by Mozilla Labs'
        detail_page = Details(mozwebqa, addon_with_one_authors)

        Assert.equal(len(detail_page.authors), 1)
        Assert.equal(detail_page.other_addons_by_authors_text, "Other add-ons by %s" % detail_page.authors[0])

    @nondestructive
    def test_navigating_to_other_addons(self, mozwebqa):
        """
        Litmus 11926
        https://litmus.mozilla.org/show_test.cgi?id=11926"""
        detail_page = Details(mozwebqa, 'firebug')

        for i in range(0, len(detail_page.other_addons)):
            name = detail_page.other_addons[i].name
            detail_page.other_addons[i].click_addon_link()
            Assert.contains(name, detail_page.title)
            Details(mozwebqa, 'firebug')

    @nondestructive
    def test_details_more_images(self, mozwebqa):
        """
        Litmus 4846
        https://litmus.mozilla.org/show_test.cgi?id=4846
        """
        detail_page = Details(mozwebqa, 'firebug')

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

        for img_set in range(image_set_count):
            image_viewer = detail_page.previewer.prev_set()

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

    @nondestructive
    def test_that_review_usernames_are_clickable(self, mozwebqa):
        """
        Litmus 4842
        https://litmus.mozilla.org/show_test.cgi?id=4842
        """
        addon_name = 'firebug'
        detail_page = Details(mozwebqa, addon_name)

        for i in range(0, len(detail_page.reviews)):
            username = detail_page.reviews[i].username
            amo_user_page = detail_page.reviews[i].click_username()
            Assert.equal(username, amo_user_page.username)
            Details(mozwebqa, addon_name)

    @nondestructive
    def test_that_details_page_has_breadcrumb(self, mozwebqa):
        """
        Litmus 11922
        https://litmus.mozilla.org/show_test.cgi?id=11922
        """
        detail_page = Details(mozwebqa, 'firebug')
        Assert.equal(detail_page.breadcrumb, 'Add-ons for Firefox\nExtensions Firebug')

    @nondestructive
    def test_that_clicking_info_link_slides_down_page_to_version_info(self, mozwebqa):
        """ Test for Litmus 25725
            https://litmus.mozilla.org/show_test.cgi?id=25725 """
        details_page = Details(mozwebqa, 'firebug')
        details_page.click_version_info_link()
        Assert.equal(details_page.version_info_link, details_page.version_information_href)
        Assert.true(details_page.is_version_information_section_expanded)
        Assert.true(details_page.is_version_information_section_in_view)

    @nondestructive
    def test_that_breadcrumb_links_in_details_page_work(self, mozwebqa):
        """
        Litmus 11923
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=11923
        """
        home_page = Home(mozwebqa)
        detail_page = Details(mozwebqa, 'firebug')

        Assert.equal(detail_page.breadcrumbs[0].name, 'Add-ons for Firefox')
        link = detail_page.breadcrumbs[0].link_value
        detail_page.breadcrumbs[0].click_breadcrumb()

        Assert.true(home_page.is_the_current_page)
        Assert.true(home_page.get_url_current_page().endswith(link))

        home_page.return_to_previous_page()

        Assert.equal(detail_page.breadcrumbs[1].name, 'Extensions')
        link = detail_page.breadcrumbs[1].link_value
        detail_page.breadcrumbs[1].click_breadcrumb()

        amo_extenstions_page = ExtensionsHome(mozwebqa)
        Assert.true(amo_extenstions_page.is_the_current_page)
        Assert.true(amo_extenstions_page.get_url_current_page().endswith(link))

        home_page.return_to_previous_page()

        Assert.equal(detail_page.breadcrumbs[2].name, 'Firebug')

    @nondestructive
    def test_that_add_a_review_button_works(self, mozwebqa):
        """
        Litmus 25729
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=25729
        """
        #Step 1: Addons Home Page loads and Addons Details loads
        home_page = Home(mozwebqa)

        #Step 2:user logs in to submit a review
        home_page.login("browserID")
        Assert.true(home_page.header.is_user_logged_in)

        #Step 3: user loads an addon details page and clicks write a review button
        details_page = Details(mozwebqa, 'Firebug')
        review_box = details_page.click_to_write_review()
        Assert.true(review_box.is_review_box_visible)

    @nondestructive
    def test_the_developers_comments_section(self, mozwebqa):
        """
        Test for Litmus 25724
        https://litmus.mozilla.org/show_test.cgi?id=25724
        """
        details_page = Details(mozwebqa, 'Firebug')
        Assert.equal(details_page.devs_comments_title, u"Developer\u2019s Comments")
        details_page.click_devs_comments()
        Assert.true(details_page.is_devs_comments_section_expanded())
        Assert.not_none(re.match('(\w+\s*){3,}', details_page.devs_comments_message))

    @nondestructive
    def test_that_add_to_collection_flyout_for_anonymous_users(self, mozwebqa):
        """
        Litmus 25711
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=25711
        """
        details_page = Details(mozwebqa, 'Firebug')
        details_page.click_add_to_collection_widget()
        Assert.equal(details_page.collection_widget_button, 'Create an Add-ons Account')
        Assert.equal(details_page.collection_widget_login_link, 'log in to your current account')

    @nondestructive
    def test_that_the_development_channel_expands(self, mozwebqa):
        """
        Litmus 25711
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=25711
        """
        details_page = Details(mozwebqa, 'Firebug')
        Assert.equal("Development Channel", details_page.development_channel_text)

        Assert.equal('', details_page.development_channel_content)
        details_page.click_development_channel()
        Assert.not_none(details_page.development_channel_content)
        details_page.click_development_channel()
        Assert.equal('', details_page.development_channel_content)

    @nondestructive
    def test_click_on_other_collections(self, mozwebqa):
        """
        Litmus 25722
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=25722
        """
        details_pg = Details(mozwebqa, 'Firebug')

        for i in range(0, len(details_pg.part_of_collections)):
            name = details_pg.part_of_collections[i].name
            collection_pg = details_pg.part_of_collections[i].click_collection()
            Assert.equal(name, collection_pg.collection_name, "Expected collection name does not match the page header")
            details_pg = Details(mozwebqa, 'Firebug')

    @nondestructive
    def test_the_development_channel_section(self, mozwebqa):
        """
        Test for Litmus 25732
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=25732
        """
        details_page = Details(mozwebqa, 'Firebug')

        Assert.equal('Development Channel', details_page.development_channel_text)
        details_page.click_development_channel()

        # Verify if description present
        Assert.not_none(details_page.development_channel_content)
        Assert.true(details_page.is_development_channel_install_button_visible)

        # Verify experimental version (beta or pre)
        Assert.not_none(re.match('Version \d\.\d.\d(b|a|rc)[0-9]:', details_page.beta_version))

    def test_that_license_link_works(self, mozwebqa):
        """
        Litmus 25726
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=25726
        """
        addon_name = 'Firebug'
        details_page = Details(mozwebqa, addon_name)
        Assert.equal(details_page.license_link_text, 'BSD License')
        license_link = details_page.license_site
        Assert.not_none(license_link)

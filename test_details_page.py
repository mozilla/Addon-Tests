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
from addons_site import AddonsDetailsPage


class TestDetailsPage:

    def test_that_register_link_is_present_in_addon_details_page(self, mozwebqa):
        """ Test for Litmus 9890"""
        amo_details_page = AddonsDetailsPage(mozwebqa, "Firebug")
        Assert.true(amo_details_page.is_register_visible())
        Assert.equal(amo_details_page.register_link, "Register")

    def test_that_login_link_is_present_in_addon_details_page(self, mozwebqa):
        """ Test for Litmus 9890"""
        amo_details_page = AddonsDetailsPage(mozwebqa, "Firebug")
        Assert.true(amo_details_page.is_login_visible())
        Assert.equal(amo_details_page.login_link, "Log in")

    def test_that_dropdown_menu_is_present_after_click_on_other_apps(self, mozwebqa):
        """ Test for Litmus 9890"""
        amo_details_page = AddonsDetailsPage(mozwebqa, "Firebug")
        Assert.true(amo_details_page.is_other_apps_link_visible())
        Assert.equal(amo_details_page.other_apps, "Other Applications")
        #TODO: Fix when the hover event works
        #Assert.true(amo_details_page.is_other_apps_dropdown_menu_visible())

    def test_that_addon_name_is_displayed(self, mozwebqa):
        """ Test for Litmus 9890"""
        amo_details_page = AddonsDetailsPage(mozwebqa, "Firebug")
        Assert.true(amo_details_page.is_addon_name_visible())
        # check that the name is not empty
        Assert.not_equal(amo_details_page.name, "")

    def test_that_summary_is_displayed(self, mozwebqa):
        """ Test for Litmus 9890"""
        amo_details_page = AddonsDetailsPage(mozwebqa, "Firebug")
        Assert.true(amo_details_page.is_summary_visible())
        # check that the summary is not empty
        Assert.not_none(re.match('(\w+\s*){3,}', amo_details_page.summary))

    def test_that_about_this_addon_is_displayed(self, mozwebqa):
        """ Test for Litmus 9890"""
        amo_details_page = AddonsDetailsPage(mozwebqa, "Firebug")
        Assert.true(amo_details_page.is_about_addon_visible())
        Assert.equal(amo_details_page.about_addon, "About this Add-on")
        Assert.not_none(re.match('(\w+\s*){3,}', amo_details_page.description))

    # TODO expand the Version Information section and check that the required details are present/visible/correct
    def test_that_version_information_is_displayed(self, mozwebqa):
        """ Test for Litmus 9890"""
        amo_details_page = AddonsDetailsPage(mozwebqa, "Firebug")
        Assert.true(amo_details_page.is_version_information_heading_visible())
        Assert.equal(amo_details_page.version_information_heading, "Version Information")
        Assert.not_none(re.search('\w+', amo_details_page.release_version))

        # check that the release number matches the the version number at the top of the page
        Assert.not_none(re.search(amo_details_page.version_number, amo_details_page.release_version))

    def test_that_reviews_are_displayed(self, mozwebqa):
        """ Test for Litmus 9890"""
        amo_details_page = AddonsDetailsPage(mozwebqa, "Firebug")
        Assert.true(amo_details_page.is_review_title_visible())
        Assert.equal(amo_details_page.review_title, "Reviews")
        Assert.true(amo_details_page.has_reviews)
        Assert.not_none(re.search('(\w+\s*){1,}', amo_details_page.review_details))

    def test_that_in_often_used_with_addons_are_displayed(self, mozwebqa):
        """ Test for Litmus 9890"""
        amo_details_page = AddonsDetailsPage(mozwebqa, "Firebug")
        Assert.true(amo_details_page.is_often_used_with_header_visible())
        Assert.equal(amo_details_page.often_used_with_header, u"Often used with\u2026")
        Assert.true(amo_details_page.is_often_used_with_list_visible())

    def test_that_tags_are_displayed(self, mozwebqa):
        """ Test for Litmus 9890"""
        amo_details_page = AddonsDetailsPage(mozwebqa, "Firebug")
        Assert.true(amo_details_page.are_tags_visible())

    def test_part_of_collections_are_displayed(self, mozwebqa):
        """ Test for Litmus 9890"""
        amo_details_page = AddonsDetailsPage(mozwebqa, "Firebug")
        Assert.true(amo_details_page.is_part_of_collections_header_visible())
        Assert.true(amo_details_page.is_part_of_collections_list_visible())
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

    def test_navigating_to_other_addons_by_the_same_author_when_there_are_less_than_five_other_addons(self, mozwebqa):
        """
        Litmus 11926
        https://litmus.mozilla.org/show_test.cgi?id=1192"""
        addon_with_less_than_five_addons_by_the_same_author = 'adblock-plus'
        amo_detail_page = AddonsDetailsPage(mozwebqa, addon_with_less_than_five_addons_by_the_same_author)

        addons = amo_detail_page.other_addons_link_list()
        Assert.true(len(addons) < 5)
        for i in range(amo_detail_page.other_addons_link_list_count):
            amo_detail_page.click_other_addon_by_this_author(addons[i])
            print addons[i]
            Assert.true(amo_detail_page.name.startswith(addons[i].rstrip('.')))
            AddonsDetailsPage(mozwebqa, addon_with_less_than_five_addons_by_the_same_author)

    def test_navigating_to_other_addons_by_the_same_author_when_there_are_more_than_four_other_addons(self, mozwebqa):
        """
        Litmus 11926
        https://litmus.mozilla.org/show_test.cgi?id=1192"""
        addon_with_more_than_four_addons_by_the_same_author = 'firebug'
        amo_detail_page = AddonsDetailsPage(mozwebqa, addon_with_more_than_four_addons_by_the_same_author)

        addons = amo_detail_page.other_addons_dropdown_values
        Assert.true(len(addons) > 4)
        for i in range(len(addons) - 1, 0, -1):  # Not checking the first item in the drop-down https://bugzilla.mozilla.org/show_bug.cgi?id=660706
            amo_detail_page.select_other_addons_dropdown_value(addons[i])
            print addons[i]
            Assert.true(amo_detail_page.name.startswith(addons[i].rstrip('.')))
            AddonsDetailsPage(mozwebqa, addon_with_more_than_four_addons_by_the_same_author)

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

        _images_count = amo_detail_page.previewer.image_count
        _image_set_count = amo_detail_page.previewer.image_set_count
        _images_title = []
        _image_link = []
        for img_set in range(_image_set_count):
            for img_no in range(3):
                if img_set * 3 + img_no != _images_count:
                    _images_title.append(amo_detail_page.previewer.image_title(img_set * 3 + img_no))
                    _image_link.append(amo_detail_page.previewer.image_link(img_set * 3 + img_no))

            image_viewer = amo_detail_page.previewer.next_set()

        image_viewer = amo_detail_page.previewer.click_image()
        Assert.true(image_viewer.is_visible)
        Assert.equal(_images_count, image_viewer.images_count)
        for i in range(image_viewer.images_count):
            Assert.true(image_viewer.is_visible)

            Assert.equal(image_viewer.caption, _images_title[i])
            Assert.equal(image_viewer.image_link.split('/')[8], _image_link[i].split('/')[8])

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

            Assert.equal(image_viewer.caption, _images_title[i])
            Assert.equal(image_viewer.image_link.split('/')[8], _image_link[i].split('/')[8])

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

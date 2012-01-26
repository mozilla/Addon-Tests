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
# Contributor(s): Marlena Compton <mcompton@mozilla.com>
#                 Teodosia Pop <teodosia.pop@softvision.ro>
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
from urllib2 import urlparse

from pages.details import Details
from pages.addons_api import AddOnsAPI

xfail = pytest.mark.xfail
nondestructive = pytest.mark.nondestructive


class TestDetailsAgainstXML:

    firebug = "Firebug"

    @nondestructive
    def test_that_firebug_page_title_is_correct(self, mozwebqa):
        firebug_page = Details(mozwebqa, self.firebug)
        Assert.true(re.search(self.firebug, firebug_page.page_title) is not None)

    @nondestructive
    def test_that_firebug_version_number_is_correct(self, mozwebqa):
        firebug_page = Details(mozwebqa, self.firebug)
        Assert.true(len(str(firebug_page.version_number)) > 0)

    @nondestructive
    def test_that_firebug_authors_is_correct(self, mozwebqa):
        """Test for Litmus 15319."""

        #get authors from browser
        firebug_page = Details(mozwebqa, self.firebug)
        browser_authors = firebug_page.authors

        #get authors from xml
        addons_xml = AddOnsAPI(mozwebqa)
        xml_authors = addons_xml.get_list_of_addon_author_names(self.firebug)

        #check that both lists have the same number of authors
        Assert.equal(len(browser_authors), len(xml_authors))

        #cross check both lists with each other
        for i in range(len(xml_authors)):
            Assert.equal(xml_authors[i], browser_authors[i])

    @nondestructive
    def test_that_firebug_images_is_correct(self, mozwebqa):
        """Test for Litmus 15324."""

        #get images links from browser
        firebug_page = Details(mozwebqa, self.firebug)
        images_count = firebug_page.previewer.image_count
        browser_images = []
        for i in range(images_count):
            browser_images.append(firebug_page.previewer.image_link(i))

        #get images links from xml
        addons_xml = AddOnsAPI(mozwebqa)
        xml_images = addons_xml.get_list_of_addon_images_links(self.firebug)

        #check that both lists have the same number of images
        Assert.equal(len(browser_images), len(xml_images))

        #cross check both lists with each other
        for i in range(len(xml_images)):
            Assert.equal(xml_images[i].replace('src=api&amp;', ''), browser_images[i])

    @nondestructive
    def test_that_firebug_summary_is_correct(self, mozwebqa):
        """Test for Litmus 15320."""

        #browser
        firebug_page = Details(mozwebqa, self.firebug)
        browser_summary = firebug_page.summary

        #api
        addons_xml = AddOnsAPI(mozwebqa)
        xml_summary = addons_xml.get_addon_summary(self.firebug)

        Assert.equal(xml_summary, browser_summary)

    @nondestructive
    def test_that_firebug_rating_is_correct(self, mozwebqa):
        firebug_page = Details(mozwebqa, self.firebug)
        Assert.equal("5", firebug_page.rating)

    @nondestructive
    def test_that_description_text_is_correct(self, mozwebqa):
        """Test for Litmus 15321."""
        #browser
        firebug_page = Details(mozwebqa, self.firebug)
        browser_description = firebug_page.description

        #api
        addons_xml = AddOnsAPI(mozwebqa)
        xml_description = addons_xml.get_addon_description(self.firebug)

        Assert.equal(browser_description.replace('\n', ''), xml_description.replace('\n', ''))

    @xfail(reason="https://www.pivotaltracker.com/story/show/17471931")
    def test_that_icon_is_correct(self, mozwebqa):
        """Test for Litmus 15322."""

        #browser
        firebug_page = Details(mozwebqa, self.firebug)
        browser_icon = firebug_page.icon_url

        #api
        addons_xml = AddOnsAPI(mozwebqa)

        xml_icon = addons_xml.get_icon_url(self.firebug)

        Assert.equal(browser_icon, xml_icon)

    @nondestructive
    def test_that_support_url_is_correct(self, mozwebqa):
        """Test for Litmus 15337."""

        #browser
        firebug_page = Details(mozwebqa, self.firebug)
        browser_support_url = firebug_page.support_url

        #api
        addons_xml = AddOnsAPI(mozwebqa)
        xml_support_url = addons_xml.get_support_url("firebug")

        Assert.equal(browser_support_url, xml_support_url)

    @nondestructive
    def test_that_rating_in_api_equals_rating_in_details_page(self, mozwebqa):
        """Test for Litmus 15325."""

        #browser
        firebug_page = Details(mozwebqa, self.firebug)
        browser_rating = firebug_page.rating

        #api
        addons_xml = AddOnsAPI(mozwebqa)
        xml_rating = addons_xml.get_rating("firebug")

        Assert.equal(browser_rating, xml_rating)

    @nondestructive
    def test_that_compatible_applications_equal(self, mozwebqa):
        """Test for Litmus 15323."""

        #browser
        firebug_page = Details(mozwebqa, self.firebug)
        firebug_page.click_version_information_header()
        browser_compatible_applications = firebug_page.compatible_applications

        #api
        addons_xml = AddOnsAPI(mozwebqa)
        xml_compatible_applications = addons_xml.get_compatible_applications("firebug")
        name = xml_compatible_applications[0]
        min_version = xml_compatible_applications[1]
        max_version = xml_compatible_applications[2]
        Assert.equal(browser_compatible_applications, 'Works with %s %s - %s' % (name, min_version, max_version))

    @nondestructive
    def test_that_addon_number_of_total_downloads_is_correct(self, mozwebqa):
        """Test for Litmus 15331."""

        #browser
        firebug_page = Details(mozwebqa, self.firebug)
        statistics_page = firebug_page.click_view_statistics()
        browser_downloads = statistics_page.total_downloads_number

        #api
        addons_xml = AddOnsAPI(mozwebqa)
        xml_downloads = addons_xml.get_total_downloads("firebug")

        Assert.equal(browser_downloads, xml_downloads)

    @nondestructive
    def test_that_learn_more_link_is_correct(self, mozwebqa):
        """Test for Litmus 15326."""

        #browser
        initial_page = Details(mozwebqa, 'Adblock Plus')

        #api
        addons_xml = AddOnsAPI(mozwebqa)
        learn_more_url = addons_xml.get_learn_more_url(self.firebug)
        addons_xml.goto_url_from_xml(learn_more_url)

        Assert.not_none(re.search(self.firebug, initial_page.page_title))

    @nondestructive
    def test_that_firebug_devs_comments_is_correct(self, mozwebqa):
        """Test for Litmus 15329."""

        #browser
        firebug_page = Details(mozwebqa, self.firebug)
        firebug_page.click_devs_comments()
        browser_devs_comments = firebug_page.devs_comments_message

        #api
        addons_xml = AddOnsAPI(mozwebqa)
        xml_devs_comments = addons_xml.get_devs_comments(self.firebug)

        Assert.equal(xml_devs_comments, browser_devs_comments)

    @nondestructive
    def test_that_home_page_in_api_equals_home_page_in_details_page(self, mozwebqa):
        """Test for Litmus 15336."""

        #browser
        firebug_page = Details(mozwebqa, self.firebug)
        browser_home_page = urlparse.unquote(firebug_page.website)

        #api
        addons_xml = AddOnsAPI(mozwebqa)
        xml_home_page = addons_xml.get_home_page("firebug")

        Assert.contains(xml_home_page, browser_home_page)

    @nondestructive
    def test_that_reviews_in_api_equals_reviews_in_details_page(self, mozwebqa):
        """Test for Litmus 15330."""

        #browser
        firebug_page = Details(mozwebqa, self.firebug)
        browser_reviews = firebug_page.total_reviews_count

        #api
        addons_xml = AddOnsAPI(mozwebqa)
        xml_reviews = addons_xml.get_reviews_count("firebug")

        Assert.equal(browser_reviews, xml_reviews)

    @nondestructive
    def test_that_daily_users_in_api_equals_daily_users_in_details_page(self, mozwebqa):
        """Test for Litmus 15333."""

        #browser
        firebug_page = Details(mozwebqa, self.firebug)
        browser_daily_users = firebug_page.daily_users_number

        #api
        addons_xml = AddOnsAPI(mozwebqa)
        xml_daily_users = addons_xml.get_daily_users("firebug")

        Assert.equal(browser_daily_users, xml_daily_users)

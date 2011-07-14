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


from selenium import selenium
from addons_site import AddonsHomePage
from addons_site import AddonsDetailsPage
from addons_search_home_page import AddonsSearchHomePage
from addons_api import AddOnsAPI
import pytest
from unittestzero import Assert
import re


class TestDetailsPageAgainstXML:

    firebug = "Firebug"

    def test_that_firebug_page_title_is_correct(self, testsetup):
        firebug_page = AddonsDetailsPage(testsetup, self.firebug)
        Assert.true(re.search(self.firebug, firebug_page.page_title) is not None)

    def test_that_firebug_version_number_is_correct(self, testsetup):
        firebug_page = AddonsDetailsPage(testsetup, self.firebug)
        Assert.true(len(str(firebug_page.version_number)) > 0)

    def test_that_firebug_authors_is_correct(self, testsetup):
        """litmus 15319"""

        #get authors from browser
        firebug_page = AddonsDetailsPage(testsetup, self.firebug)
        browser_authors = firebug_page.authors

        #get authors from xml
        addons_xml = AddOnsAPI(testsetup)
        xml_authors = addons_xml.get_list_of_addon_author_names(self.firebug)

        #check that both lists have the same number of authors
        Assert.equal(len(browser_authors), len(xml_authors))

        #cross check both lists with each other
        for i in range(len(xml_authors)):
            Assert.equal(xml_authors[i], browser_authors[i])

    def test_that_firebug_summary_is_correct(self, testsetup):
        """litmus 15320"""

        #browser
        firebug_page = AddonsDetailsPage(testsetup, self.firebug)
        browser_summary = firebug_page.summary

        #api
        addons_xml = AddOnsAPI(testsetup)
        xml_summary = addons_xml.get_addon_summary(self.firebug)

        Assert.equal(xml_summary, browser_summary)

    def test_that_firebug_rating_is_correct(self, testsetup):
        firebug_page = AddonsDetailsPage(testsetup, self.firebug)
        Assert.equal("5", firebug_page.rating)

    def test_that_description_text_is_correct(self, testsetup):
        """litmus 15321"""
        #browser
        firebug_page = AddonsDetailsPage(testsetup, self.firebug)
        browser_description = firebug_page.description

        #api
        addons_xml = AddOnsAPI(testsetup)
        xml_description = addons_xml.get_addon_description(self.firebug)

        Assert.equal(browser_description, xml_description)

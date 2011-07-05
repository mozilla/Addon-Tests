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

        #xml
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

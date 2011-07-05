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
        firebug_page = AddonsDetailsPage(testsetup, self.firebug)
        summary = "Firebug integrates with Firefox to put a wealth of development tools at your fingertips while you browse. You can edit, debug, and monitor CSS, HTML, and JavaScript live in any web page"
        summary += "...\n\nThis is our production release. For Firefox 4.0b, see below."
        Assert.equal(summary, firebug_page.summary)

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
        
    def test_that_icon_is_correct(self, testsetup):
        """litmus """
        
        #browser
        firebug_page = AddonsDetailsPage(testsetup, self.firebug)
        Assert.true(firebug_page.is_element_present("css=img[class='icon']"))
        
        
        
        #try get_attribute(locator) to see if that will return the html string for icon locator
        #javadoc:
        #http://release.seleniumhq.org/selenium-remote-control/0.9.2/doc/java/com/thoughtworks/selenium/Selenium.html
        
        #xml
        addons_xml = AddOnsAPI(testsetup)
        xml_icon_url = addons_xml.get_icon_url(self.firebug)
        
        Assert.equal( firebug_page.selenium.get_attribute("css=img[class='icon']@src"), xml_icon_url )
        
        the_url = 'https://gs1.adn.edgecastcdn.net/801237/addons-cdn.allizom.org/images/addon_icon/1843-32.png?modified=1308640553'
        Assert.equal('https://gs1.adn.edgecastcdn.net/801237/addons-cdn.allizom.org/images/addon_icon/1843-32.png?modified=1308640553', xml_icon_url)
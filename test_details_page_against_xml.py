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
    
    #The asserts in these tests will be using values from the xml api for comparison 
    #and not hardcoded values once the api class is merged.
    def test_that_firebug_page_title_is_correct(self, testsetup):
        firebug_page = AddonsDetailsPage(testsetup, self.firebug)
        Assert.true(re.search(self.firebug, firebug_page.page_title) is not None)          

    def test_that_firebug_version_number_is_correct(self, testsetup):
        firebug_page = AddonsDetailsPage(testsetup, self.firebug)
        Assert.true(len (str(firebug_page.version_number)) > 0)

    def test_that_firebug_authors_is_correct(self, testsetup):
        """litmus 15319"""
        
        #get authors from browser
        firebug_page = AddonsDetailsPage(testsetup, self.firebug)
        browser_authors = firebug_page.authors
        
        #get authors from xml
        addons_xml = AddOnsAPI(testsetup)
        xml_authors = addons_xml.get_list_of_addon_author_names("Firebug")
        
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
    
        
if __name__ == "__main__":
    unittest.main()
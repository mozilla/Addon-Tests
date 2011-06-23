from selenium import selenium
from addons_site import AddonsHomePage
from addons_site import AddonsDetailsPage
from addons_search_home_page import AddonsSearchHomePage
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
        firebug_page = AddonsDetailsPage(testsetup, self.firebug)
        authors = firebug_page.authors
        Assert.equal("Joe Hewitt", authors[0])
        Assert.equal("johnjbarton", authors[1])
        Assert.equal("robcee", authors[2])
        Assert.equal("FirebugWorkingGroup", authors[3])
        Assert.equal("Jan Odvarko", authors[4])
        
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
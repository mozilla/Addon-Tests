#!/usr/bin/env python

# https://addons.allizom.org/en-us/firefox/api/1.5/search/fire
# https://addons.allizom.org/en-us/firefox/api/1.5/search/firebug 

from BeautifulSoup import BeautifulStoneSoup
#from selenium import selenium
#from vars import ConnectionParameters
import unittest
import urllib2
#import pytest
#xfail = pytest.mark.xfail



class APITests(unittest.TestCase):


	

		
	def test_api(self):  #test_that_firebug_is_listed_first_in_api_search_results_for_fire(self):
		""" TestCase for Litmus 15314 """
		xml_soup = BeautifulStoneSoup(urllib2.urlopen('https://addons.allizom.org/en-us/firefox/api/1.5/search/fire'))
		name_of_first_addon_listed = xml_soup.searchresults.addon.nameTag.contents[0]
		self.assertEquals("Firebug", name_of_first_addon_listed)
		
		
if __name__ == "__main__":
	unittest.main()

			
		
		
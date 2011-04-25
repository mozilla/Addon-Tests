#!/usr/bin/env python

# https://addons.allizom.org/en-us/firefox/api/1.5/search/fire
# https://addons.allizom.org/en-us/firefox/api/1.5/search/firebug 

from BeautifulSoup import BeautifulStoneSoup
#from selenium import selenium
from vars import ConnectionParameters
import unittest
import urllib2
#import pytest
#xfail = pytest.mark.xfail



class AddOnsAPI(object):
	
	
	_api_base_url = ConnectionParameters.baseurl + '/en-us/firefox/api/1.5/search'	
	
	_firebug_url = _api_base_url + '/firebug'		
		
	def __init__(self,api_search_term):
		pass
			
class APITests(unittest.TestCase):		

	def test_check_that_firebug_is_listed_first_on_searching_for_fire(self):  
		""" TestCase for Litmus 15314 """
		url = urllib2.urlopen(AddOnsAPI._api_base_url + '/fire')
		xml_soup = BeautifulStoneSoup(url)
		name_of_first_addon_listed = xml_soup.searchresults.addon.nameTag.contents[0]
		self.assertEquals("Firebug", name_of_first_addon_listed)		
					
if __name__ == "__main__":
	unittest.main()

			
		
		
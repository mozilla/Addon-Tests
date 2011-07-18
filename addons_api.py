#!/usr/bin/env python

from BeautifulSoup import BeautifulStoneSoup
import urllib2
import pytest
import py
import re


class AddOnsAPI(object):

    def __init__(self, testsetup, search_extension='firebug'):

        self.api_base_url = testsetup.base_url + '/en-us/firefox/api/1.5/search/'
        self.search_url = self.api_base_url + search_extension
        self.parsed_xml = BeautifulStoneSoup(urllib2.urlopen(self.search_url))

    def get_xml_for_single_addon(self, addon_name):
        try:
            addon_xml = self.parsed_xml.find(text=addon_name).findParent().findParent()
            return addon_xml
        except AttributeError:
            self._print_search_error()

    def get_name_of_first_addon(self):
        try:
            name_of_first_addon_listed = self.parsed_xml.searchresults.addon.nameTag.contents[0]
            return name_of_first_addon_listed
        except:
            print 'Check that searchresults returned valid xml'

    def get_addon_type_name(self, addon_name):
        try:
            addon_xml = self.get_xml_for_single_addon(addon_name)
            return addon_xml.type.string
        except:
            self._print_search_error()

    def get_addon_type_id(self, addon_name):
        try:
            addon_xml = self.get_xml_for_single_addon(addon_name)
            return addon_xml.type["id"]
        except AttributeError:
            self._print_search_error()

    def get_addon_version_number(self, addon_name):
        try:
            addon_xml = self.get_xml_for_single_addon(addon_name)
            return addon_xml.version.string
        except AttributeError:
            self._print_search_error()

    def get_addon_description(self, addon_name):
        try:
            addon_xml = self.get_xml_for_single_addon(addon_name)
            description = addon_xml.description.string
            return self._strip_links_from_text(description)
        except AttributeError:
            self._print_search_error()

    def get_addon_summary(self, addon_name):
        try:
            addon_xml = self.get_xml_for_single_addon(addon_name)
            summary = addon_xml.summary.string
            return self._strip_links_from_text(summary)
        except AttributeError:
            self._print_search_error()

    def get_list_of_addon_author_names(self, addon_name):
        try:
            addon_xml = self.get_xml_for_single_addon(addon_name)
            name_tags = addon_xml.authors.findAll('name')
2
            return [BeautifulStoneSoup(str(name_tags[i])).find('name').string
                for i in range(len(name_tags))]

        except AttributeError:
            self._print_search_error()

    def get_icon_url(self, addon_name):
        try:
            addon_xml = self.get_xml_for_single_addon(addon_name)
            return addon_xml.icon.string
        except:
            self._print_search_error()

    def _strip_links_from_text(self, text):
        for i in re.findall("&lt;.+?&gt;", text, re.MULTILINE):
            text = text.replace(i, "")
        return text

    def _print_search_error(self):
        print('The addon is not in the search results.')

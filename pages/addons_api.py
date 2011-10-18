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
# Contributor(s):
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

import py
import re
import pytest
import urllib2

from BeautifulSoup import BeautifulStoneSoup


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

    def get_support_url(self, addon_name):
        try:
            addon_xml = self.get_xml_for_single_addon(addon_name)
            return addon_xml.support.string
        except:
            self._print_search_error()

    def get_rating(self, addon_name):
        try:
            addon_xml = self.get_xml_for_single_addon(addon_name)
            return addon_xml.rating.string
        except:
            self._print_search_error()

    def _strip_links_from_text(self, text):
        for i in re.findall("&lt;.+?&gt;", text, re.MULTILINE):
            text = text.replace(i, "")
        return text

    def _print_search_error(self):
        print('The addon is not in the search results.')

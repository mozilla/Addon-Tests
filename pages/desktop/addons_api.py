#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import xml.etree.ElementTree as ET
import urllib2


class AddonsAPI:

    def __init__(self, testsetup, search_query):
        """
        This class checks the XML response returned by
        the AddonsAPI on addons.mozilla.org.  The search_query
        parameter is the name of the add-on to search for.
        """
        self.search_query = search_query
        self.api_url = '%s/en-us/firefox/api/1.5/search/%s' % (testsetup.base_url, search_query)
        self.xml_response = ET.parse(urllib2.urlopen(self.api_url))

    def get_addon_name(self):
        """
        returns the value of the name element
        of the first add-on from the xml response.
        """
        try:
            name = self.xml_response.getroot().find('./addon/name')
            return name.text.lower()
        except AttributeError:
            print 'Could not find the element [name] for the [%s] add-on.' % self.search_query

    def get_addon_type(self):
        """
        returns the value of the type element
        of the first add-on from the xml response.
        """
        try:
            addon_type = self.xml_response.getroot().find('./addon/type')
            return addon_type.text.lower()
        except AttributeError:
            print 'Could not find the element [type] for the [%s] add-on.' % self.search_query

    def get_addon_type_id(self):
        """
        returns the id attribute of the type
        element of the the first add-on from
        the xml response.
        """
        try:
            addon_type = self.xml_response.getroot().find('./addon/type')
            return int(addon_type.attrib['id'])
        except AttributeError:
            print 'Could not find the attribute [id] of element [type] for [%s] add-on.' % self.search_query

    def get_install_link(self):
        """
        returns the url value of the link element
        of the first add-on from the xml response.
        """
        try:
            link = self.xml_response.getroot().find('./addon/install')
            return link.text.lower()
        except AttributeError:
            print 'Could not find element [install] for the [%s] add-on.' % self.search_query

    def get_daily_users(self):
        """
        returns the value of the daily_users element
        of the first add-on from the xml response
        """
        try:
            daily_users = self.xml_response.getroot().find('./addon/daily_users')
            return daily_users.text.lower()
        except AttributeError:
            print 'Could not find the element [daily_users] for the [%s] add-on.' % self.search_query

    def get_addon_status_id(self):
        """
        returns the id attribute of the status element
        of the first add-on from the xml response.
        """
        try:
            status_id = self.xml_response.getroot().find('./addon/status')
            return int(status_id.attrib['id'])
        except AttributeError:
            print 'Could not find the attribute [id] of element [status] for [%s] add-on.' % self.search_query

    def get_addon_status(self):
        """
        returns the status element
        of the first add-on from the xml response.
        """
        try:
            status_id = self.xml_response.getroot().find('./addon/status')
            return status_id.text.lower()
        except AttributeError:
            print 'Could not find the element [status] for [%s] add-on. %s' % (self.search_query, self.api_url)

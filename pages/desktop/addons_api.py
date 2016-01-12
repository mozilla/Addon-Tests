# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re
import urllib2

import xml.etree.ElementTree as ET


class AddonsAPI:

    def __init__(self, base_url, search_query):
        """
        This class checks the XML response returned by
        the AddonsAPI on addons.mozilla.org.  The search_query
        parameter is the name of the add-on to search for.
        """
        self.search_query = search_query
        self.api_url = '%s/en-us/firefox/api/1.5/search/%s' % (base_url, search_query)
        self.xml_response = ET.parse(urllib2.urlopen(self.api_url))

    def get_addon_name(self):
        """
        returns the value of the name element
        of the first add-on from the xml response.
        """
        name = self._parse_response('name')
        return name.lower()

    def get_addon_type(self):
        """
        returns the value of the type element
        of the first add-on from the xml response.
        """
        addon_type = self._parse_response(relpath='type')
        return addon_type.lower()

    def get_addon_type_id(self):
        """
        returns the id attribute of the type
        element of the the first add-on from
        the xml response.
        """
        addon_type = self._parse_response(relpath='type', attr='id')
        return int(addon_type)

    def get_install_link(self):
        """
        returns the url value of the link element
        of the first add-on from the xml response.
        """
        link = self._parse_response(relpath='install')
        return link.lower()

    def get_daily_users(self):
        """
        returns the value of the daily_users element
        of the first add-on from the xml response
        """
        daily_users = self._parse_response(relpath='daily_users')
        return int(daily_users)

    def get_addon_status_id(self):
        """
        returns the id attribute of the status element
        of the first add-on from the xml response.
        """
        status_id = self._parse_response(relpath='status', attr='id')
        return int(status_id)

    def get_addon_status(self):
        """
        returns the status element
        of the first add-on from the xml response.
        """
        status = self._parse_response(relpath='status')
        return status.lower()

    def get_reviews_count(self):
        """
        returns the num attribute of reviews element
        of the first add-on from the xml response.
        """
        count = self._parse_response(relpath='reviews', attr='num')
        return int(count)

    def get_home_page(self):
        """
        returns text of the homepage element
        of the first add-on from the xml response.
        """
        homepage = self._parse_response(relpath='homepage')
        return homepage.lower()

    def get_devs_comments(self):
        """
        returns text of the developer_comments element
        of the first add-on from the xml response.
        all HTML tags are stripped.
        """
        devs_comments = self._parse_response(relpath='developer_comments')
        return self._remove_html_tags(devs_comments)

    def get_learn_more_url(self):
        """
        returns text of the learnmore element
        of the first add-on from the xml response.
        """
        return self._parse_response(relpath='learnmore')

    def get_total_downloads(self):
        """
        returns the total_downloads element
        of the first add-on from the xml response.
        """
        downloads = self._parse_response(relpath='total_downloads')
        return int(downloads)

    def get_compatible_applications(self):
        """
        returns name, min version and max version of
        compatible application of the first add-on from the xml response.
        """
        xpath = 'compatible_applications/application/'
        name_path = xpath + 'name'
        min_ver_path = xpath + 'min_version'
        max_ver_path = xpath + 'max_version'

        return map(self._parse_response,
                   [name_path, min_ver_path, max_ver_path])

    def get_rating(self):
        """
        returns text of the rating element
        of the first add-on from the xml response.
        """
        return self._parse_response(relpath='rating')

    def get_support_url(self):
        """
        returns text of the support element
        of the first add-on from the xml response.
        """
        return self._parse_response(relpath='support')

    def get_icon_url(self):
        """
        returns text of the first icon element
        of the first add-on from the xml response.
        """
        return self._parse_response(relpath='icon')

    def get_addon_description(self):
        """
        returns text of the description element
        of the first add-on from the xml response.
        all HTML tags are stripped.
        """
        desc = self._parse_response(relpath='description')
        return self._remove_html_tags(desc)

    def get_addon_summary(self):
        """
        returns text of the summary element
        of the first add-on from the xml response.
        """
        return self._parse_response(relpath='summary')

    def get_list_of_addon_author_names(self):
        """
        returns list of author names of the first add-on
        from the xml response
        """
        authors_el = self._get_element(relpath='authors')
        authors_list = []
        for child in authors_el:
            authors_list.append(child.find('name').text)
        return authors_list

    def get_list_of_addon_images_links(self):
        """
        returns list of thumbnail image links
        of the first add-on from xml response
        """
        preview_el = self._get_element(relpath='previews')
        link_list = []
        for child in preview_el:
            link = child.find('thumbnail').text
            link_list.append(link.strip())
        return link_list

    def _parse_response(self, relpath, attr=None):
        """
        returns text node of element or attribute of element
        of the first add-on from xml response.
        """
        try:
            el = self.xml_response.getroot().find('./addon/%s' % relpath)
            return attr and el.attrib[attr] or el.text
        except (AttributeError, KeyError):
            raise ET.ParseError(self._error_message(relpath, attr))

    def _get_element(self, relpath):
        """returns element of the first add-on from xml response."""
        try:
            return self.xml_response.getroot().find('./addon/%s' % relpath)
        except AttributeError:
            raise ET.ParseError(self._error_message(relpath))

    def _remove_html_tags(self, text):
        """removes all HTML tags from given string"""
        return re.sub(r'<.*?>', '', text)

    def _error_message(self, relpath, attr=None):
        """generates error message text"""
        if attr:
            err_msg = 'Could not find the attribute [%s] of element [%s]' % (attr, relpath)
        else:
            err_msg = 'Could not find the element [%s]' % relpath

        return err_msg + ' for [%s] add-on. %s' % (self.search_query, self.api_url)

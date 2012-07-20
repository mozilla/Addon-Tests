#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re
import urllib2

from BeautifulSoup import BeautifulStoneSoup


class AddOnsAPI:

    def __init__(self, testsetup, search_extension='firebug'):
        self.search_url = '%s/en-us/firefox/api/1.5/search/%s' % (testsetup.api_base_url, search_extension)
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
            print 'Check that search results returned valid xml'

    def get_name_of_top_addons(self, count=5):
        try:
            c = 0
            for addon in filter(lambda s: not isinstance(s, (str, unicode)),
                                self.parsed_xml.searchresults.contents):
                yield addon.nameTag.contents[0]
                c += 1
                if c == count:
                    return
        except:
            print 'Check that search results returned valid xml'

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

    def get_addon_status(self, addon_name):
        try:
            addon_xml = self.get_xml_for_single_addon(addon_name)
            return addon_xml.status['id'], addon_xml.status.string
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

    def get_list_of_addon_images_links(self, addon_name):
        try:
            addon_xml = self.get_xml_for_single_addon(addon_name)
            name_tags = addon_xml.previews.findAll('thumbnail')

            return [BeautifulStoneSoup(str(name_tags[i])).find('thumbnail').string.strip('\n ')
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

    def get_learn_more_url(self, addon_name):
        try:
            addon_xml = self.get_xml_for_single_addon(addon_name)
            return addon_xml.learnmore.string
        except:
            self._print_search_error()

    def get_rating(self, addon_name):
        try:
            addon_xml = self.get_xml_for_single_addon(addon_name)
            return addon_xml.rating.string
        except:
            self._print_search_error()

    def get_compatible_applications(self, addon_name):
        try:
            addon_xml = self.get_xml_for_single_addon(addon_name)
            return (addon_xml.application.find('name').string,
                    addon_xml.min_version.string, addon_xml.max_version.string)
        except AttributeError:
            self._print_search_error()

    def get_total_downloads(self, addon_name):
        try:
            addon_xml = self.get_xml_for_single_addon(addon_name)
            return int(addon_xml.total_downloads.string)
        except AttributeError:
            self._print_search_error()

    def get_devs_comments(self, addon_name):
        try:
            addon_xml = self.get_xml_for_single_addon(addon_name)
            developer_comments = addon_xml.developer_comments.string.rstrip("\n")
            return self._strip_links_from_text(developer_comments)
        except AttributeError:
            self._print_search_error()

    def get_home_page(self, addon_name):
        try:
            addon_xml = self.get_xml_for_single_addon(addon_name)
            return addon_xml.homepage.string
        except:
            self._print_search_error()

    def get_reviews_count(self, addon_name):
        try:
            addon_xml = self.get_xml_for_single_addon(addon_name)
            return int(addon_xml.reviews['num'])
        except:
            self._print_search_error()

    def get_daily_users(self, addon_name):
        try:
            addon_xml = self.get_xml_for_single_addon(addon_name)
            return int(addon_xml.daily_users.string)
        except:
            self._print_search_error()

    def _strip_links_from_text(self, text):
        for i in re.findall("&lt;.+?&gt;", text, re.MULTILINE):
            text = text.replace(i, "")
        return text

    def _print_search_error(self):
        print('The addon is not in the search results.')

    def get_install_link(self, addon_name):
        try:
            return self.get_xml_for_single_addon(addon_name).install.string
        except:
            self._print_search_error()

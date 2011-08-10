#!/usr/bin/env python
#
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
# Contributor(s): Vishal
#                 Dave Hunt <dhunt@mozilla.com>
#                 David Burns
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
'''
Created on Jun 21, 2010

'''
import re
import time
import base64
import yaml


http_regex = re.compile('https?://((\w+\.)+\w+\.\w+)')


class Page(object):
    '''
    Base class for all Pages
    '''

    def __init__(self, testsetup):
        '''
        Constructor
        '''
        self.testsetup = testsetup
        self.base_url = testsetup.base_url
        self.selenium = testsetup.selenium
        self.timeout = testsetup.timeout
        self.credentials = testsetup.credentials
        self.site_version = testsetup.site_version

    @property
    def is_the_current_page(self):
        page_title = self.selenium.get_title()
        if not page_title == self._page_title:
            self.record_error()
            try:
                raise Exception("Expected page title to be: '"
                    + self._page_title + "' but it was: '" + page_title + "'")
            except Exception:
                raise Exception('Expected page title does not match actual page title.')
        else:
            return True

    def get_url_current_page(self):
        return(self.selenium.get_location())

    def get_text(self, text):
        return(self.selenium.get_text(text))

    def is_text_present(self, text):
        return self.selenium.is_text_present(text)

    def is_element_present(self, locator):
        return self.selenium.is_element_present(locator)

    def return_to_previous_page(self):
        self.selenium.go_back()
        self.selenium.wait_for_page_to_load(self.timeout)

    def refresh(self):
        self.selenium.refresh()
        self.selenium.wait_for_page_to_load(self.timeout)

    def wait_for_element_present(self, element):
        count = 0
        while not self.selenium.is_element_present(element):
            time.sleep(1)
            count += 1
            if count == self.timeout / 1000:
                self.record_error()
                raise Exception(element + ' has not loaded')

    def wait_for_element_not_present(self, element):
        count = 0
        while  self.selenium.is_element_present(element):
            time.sleep(1)
            count += 1
            if count == self.timeout / 1000:
                self.record_error()
                raise Exception(element + ' is still loaded')

    def wait_for_element_visible(self, element):
        self.wait_for_element_present(element)
        count = 0
        while not self.selenium.is_visible(element):
            time.sleep(1)
            count += 1
            if count == self.timeout / 1000:
                self.record_error()
                raise Exception(element + " is not visible")

    def wait_for_element_not_visible(self, element):
        count = 0
        while self.selenium.is_visible(element):
            time.sleep(1)
            count += 1
            if count == self.timeout / 1000:
                self.record_error()
                raise Exception(element + " is still visible")

    def wait_for_page(self, url_regex):
        count = 0
        while (re.search(url_regex, self.selenium.get_location(), re.IGNORECASE)) is None:
            time.sleep(1)
            count += 1
            if count == self.timeout / 1000:
                self.record_error()
                raise Exception("Sites Page has not loaded")

    def record_error(self):
        ''' Records an error. '''

        http_matches = http_regex.match(self.base_url)
        file_name = http_matches.group(1)

        print '-------------------'
        print 'Error at ' + self.selenium.get_location()
        print 'Page title ' + self.selenium.get_title()
        print '-------------------'
        filename = file_name + '_' + str(time.time()).split('.')[0] + '.png'

        print 'Screenshot of error in file ' + filename
        f = open(filename, 'wb')
        f.write(base64.decodestring(
            self.selenium.capture_entire_page_screenshot_to_string('')))
        f.close()

    def parse_yaml_file(self, file_name):
        stream = file(file_name, 'r')
        return yaml.load(stream)

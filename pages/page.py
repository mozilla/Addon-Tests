#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
'''
Created on Jun 21, 2010

'''
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException


class Page(object):
    """
    Base class for all Pages.
    """

    def __init__(self, testsetup):
        """
        Constructor
        """
        self.testsetup = testsetup
        self.base_url = testsetup.base_url
        self.services_base_url = testsetup.services_base_url
        self.selenium = testsetup.selenium
        self.timeout = testsetup.timeout

    def get_url(self, url):
        self.selenium.get(url)

    @property
    def is_the_current_page(self):
        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: s.title == self._page_title,
            "Expected page title: %s. Actual page title: %s" % (self._page_title, self.selenium.title))
        return True

    def get_url_current_page(self):
        WebDriverWait(self.selenium, self.timeout).until(lambda s: self.selenium.title)
        return self.selenium.current_url

    def is_element_present(self, *locator):
        self.selenium.implicitly_wait(0)
        try:
            self.selenium.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
        finally:
            # set back to where you once belonged
            self.selenium.implicitly_wait(self.testsetup.default_implicit_wait)

    def is_element_visible(self, *locator):
        try:
            return self.selenium.find_element(*locator).is_displayed()
        except (NoSuchElementException, ElementNotVisibleException):
            return False

    def return_to_previous_page(self):
        self.selenium.back()


class PageRegion(object):

    _root_locator = None

    def __init__(self, testsetup, root=None):
        self.testsetup = testsetup
        self.selenium = testsetup.selenium
        self.timeout = testsetup.timeout
        self.root_element = root

    @property
    def root(self):
        if self.root_element is None and self._root_locator is not None:
            self.root_element = self.selenium.find_element(*self._root_locator)
        return self.root_element

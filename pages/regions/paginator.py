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
# Portions created by the Initial Developer are Copyright (C) 2012
# the Initial Developer. All Rights Reserved.
#
# Contributor(s): Bebe <florin.strugariu@softvision.ro>
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


from selenium.webdriver.common.by import By

from pages.page import Page


class Paginator(Page):

    #Numbering
    _numbering_text_loactor = (By.CSS_SELECTOR, 'nav.paginator .num')
    _page_number_locator = (By.CSS_SELECTOR, 'nav.paginator .num >a:nth-child(1)')
    _total_number_of_pages_locator = (By.CSS_SELECTOR, 'nav.paginator .num >a:nth-child(2)')

    #Navigation
    _first_page_locator = (By.CSS_SELECTOR, 'nav.paginator .rel a:nth-child(1)')
    _prev_locator = (By.CSS_SELECTOR, 'nav.paginator .rel a.prev')
    _next_loactor = (By.CSS_SELECTOR, 'nav.paginator .rel a.next')
    _last_page_loactor = (By.CSS_SELECTOR, 'nav.paginator .rel a:nth-child(4)')

    #Position
    _position_text_locator = (By.CSS_SELECTOR, 'nav.paginator .pos')
    _start_item_number_locator = (By.CSS_SELECTOR, 'nav.paginator .pos b:nth-child(1)')
    _end_item_number_locator = (By.CSS_SELECTOR, 'nav.paginator .pos b:nth-child(2)')
    _toatal_item_number = (By.CSS_SELECTOR, 'nav.paginator .pos b:nth-child(3)')

    @property
    def numbering_text(self):
        return self.selenium.find_element(*self._numbering_text_loactor).text

    @property
    def page_number(self):
        return int(self.selenium.find_element(*self._page_number_locator).text)

    @property
    def total_number_of_pages(self):
        return int(self.selenium.find_element(*self._total_number_of_pages_locator))

    def go_to_first_page(self):
        self.selenium.find_element(*self._first_page_locator).click()

    @property
    def go_to_first_page_title(self):
        return self.selenium.find_element(*self._first_page_locator).get_attribute('title')

    @property
    def is_go_to_first_page_disabled(self):
        return 'disabled' in self.selenium.find_element(*self._first_page_locator).get_attribute('class')

    def prev_page(self):
        self.selenium.find_element(*self._prev_locator).click()

    @property
    def is_prev_page_disabled(self):
        return 'disabled' in self.selenium.find_element(*self._prev_locator).get_attribute('class')

    def next_page(self):
        self.selenium.find_element(*self._next_loactor).click()

    @property
    def is_next_page_disabled(self):
        return 'disabled' in self.selenium.find_element(*self._next_loactor).get_attribute('class')

    def go_to_last_page(self):
        self.selenium.find_element(*self._last_page_loactor).click()

    @property
    def go_to_last_page_title(self):
        return self.selenium.find_element(*self._last_page_loactor).get_attribute('title')

    @property
    def is_go_to_last_page_disabled(self):
        return 'disabled' in self.selenium.find_element(*self._last_page_loactor).get_attribute('class')

    @property
    def position_text(self):
        return self.selenium.find_element(*self._position_text_locator).text

    @property
    def start_item(self):
        return  int(self.selenium.find_element(*self._start_item_number_locator).text)

    @property
    def end_item(self):
        return int(self.selenium.find_element(*self._end_item_number_locator).text)

    @property
    def total_items(self):
        return long(self.selenium.find_element(*self._toatal_item_number).text)

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
# Contributor(s): Bebe <florin.strugariu@softvision.ro>
#                 Alin Trif <alin.trif@softvision.ro>
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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

from pages.page import Page
from pages.base import Base


class ExtensionsHome(Base):

    _page_title = 'Featured Extensions :: Add-ons for Firefox'
    _extensions_locator = (By.CSS_SELECTOR, "div.items div.item")
    _next_page_locator = (By.CSS_SELECTOR, ".paginator .rel > a:nth-child(3)")
    _last_page_link_locator = (By.CSS_SELECTOR, ".paginator .rel > a:nth-child(4)")
    _first_page_link_locator = (By.CSS_SELECTOR, ".paginator .rel > a:nth-child(1)")
    _default_selected_tab_locator = (By.CSS_SELECTOR, "#sorter li.selected")

    _sort_by_most_users_locator = (By.CSS_SELECTOR, "div#sorter > ul > li:nth-child(2) > a")

    _updating_locator = (By.CSS_SELECTOR, "div.updating")

    @property
    def extensions(self):
        return [Extension(self.testsetup, element)
                for element in self.selenium.find_elements(*self._extensions_locator)]

    @property
    def is_next_button_disabled(self):
        next_button = self.selenium.find_element(*self._next_page_locator)
        return 'disabled' in next_button.get_attribute('class')

    def go_to_last_page(self):
        self.selenium.find_element(*self._last_page_link_locator).click()

    def go_to_first_page(self):
        self.selenium.find_element(*self._first_page_link_locator).click()

    @property
    def default_selected_tab(self):
        return self.selenium.find_element(*self._default_selected_tab_locator).text

    def _wait_for_results_refresh(self):
        WebDriverWait(self.selenium, 10).until(lambda s: not self.is_element_present(*self._updating_locator))

    def sort_by(self, type):
        click_element = self.selenium.find_element(*getattr(self, '_sort_by_%s_locator' % type.replace(' ', '_').lower()))
        footer = self.selenium.find_element(*self._footer_locator)
        ActionChains(self.selenium).\
            move_to_element(footer).\
            move_to_element(click_element).\
            click().perform()
        self._wait_for_results_refresh()

class Extension(Page):
        _name_locator = (By.CSS_SELECTOR, "h3 a")

        def __init__(self, testsetup, element):
            Page.__init__(self, testsetup)
            self._root_element = element

        @property
        def name(self):
            return self._root_element.find_element(*self._name_locator).text

        def click(self):
            self._root_element.find_element(*self._name_locator).click()
            from pages.details import Details
            return Details(self.testsetup)

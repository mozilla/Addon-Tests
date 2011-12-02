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
# Contributor(s): Zac
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


class FilterBase(Page):

    _results_count_tag = (By.CSS_SELECTOR, 'p.cnt')

    def tag(self, lookup):
        return self.Tag(self.testsetup, lookup)

    @property
    def results_count(self):
        return self.selenium.find_element(*self._results_count_tag).text.split()[0]

    class FilterResults(Page):

        _item_link = (By.CSS_SELECTOR, ' a')
        _all_tags_locator = (By.CSS_SELECTOR, 'li#tag-facets h3')

        def __init__(self, testsetup, lookup):
            Page.__init__(self, testsetup)
            # expand the thing here to represent the proper user action
            is_expanded = self.selenium.find_element(*self._all_tags_locator).get_attribute('class')
            if ('active' not in is_expanded):
                self.selenium.find_element(*self._all_tags_locator).click()
            self._root_element = self.selenium.find_element(self._base_locator[0],
                                    "%s[a[contains(@data-params, '%s')]]" % (self._base_locator[1], lookup))

        @property
        def name(self):
            return self._root_element.text

        @property
        def is_selected(self):
            return "selected" in self._root_element.get_attribute('class')

        def click_tag(self):
            self._root_element.find_element(*self._item_link).click()

    class Tag(FilterResults):
        _base_locator = (By.XPATH, ".//*[@id='tag-facets']/ul/li")

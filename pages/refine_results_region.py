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

from base_page import BasePage
from page import Page


class RefineResults(BasePage):

    _platforms_locator = "css=#refine-platform"
    _compatible_locator = "css=#refine-compatibility"
    _tags_locator = "css=#refine-tags"

    _list_locator = " ul li"

    #Platform area
    @property
    def platform_count(self):
        return int(self.selenium.get_css_count(self._platforms_locator + self._list_locator))

    def platform(self, lookup):
        return self.Item(self.testsetup, self._platforms_locator, lookup)

    def platforms(self):
        return [self.Item(self.testsetup, self._platforms_locator, i) for i in range(self.platform_count)]

    #Compatible with  area
    @property
    def compatible_count(self):
        return int(self.selenium.get_css_count(self._compatible_locator + self._list_locator))

    def compatible(self, lookup):
        return self.Item(self.testsetup, self._compatible_locator, lookup)

    def compatibles(self):
        return [self.Item(self.testsetup, self._compatible_locator, i) for i in range(self.compatible_count)]

    #Tag area
    @property
    def tag_count(self):
        return int(self.selenium.get_css_count(self._tags_locator + self._list_locator))

    def tag(self, lookup):
        return self.Item(self.testsetup, self._tags_locator, lookup)

    def tags(self):
        return [self.Item(self.testsetup, self._tags_locator, i) for i in range(self.tag_count)]

    #general Item class
    class Item(Page):

        _name_locator = " a"
        _selected_locator = "@class"

        def __init__(self, testsetup, locator, lookup):
            Page.__init__(self, testsetup)
            self.lookup = lookup
            self.locator = locator

        def _absolute_locator(self, relative_locator):
            return self._root_locator + relative_locator

        @property
        def _root_locator(self):
            if type(self.lookup) == int:
                # lookup by index
                return "{0} ul li:nth({1})".format(self.locator, self.lookup)
            else:
                # lookup by name
                return "{0} ul li:contains({1})".format(self.locator, self.lookup)

        def click(self):
            self.selenium.click(self._absolute_locator(self._name_locator))
            self.selenium.wait_for_page_to_load(self.timeout)

        @property
        def name(self):
            return self.selenium.get_text(self._absolute_locator(self._name_locator))

        @property
        def is_selected(self):
            try:
                if self.selenium.get_attribute(self._absolute_locator(self._selected_locator)) == 'selected':
                    return True
            except:
                pass
            return False

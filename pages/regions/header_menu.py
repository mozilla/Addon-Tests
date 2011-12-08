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

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from pages.page import Page


class HeaderMenu(Page):
    #This class access the header area from the top of the AMO impala pages
    #to access it just use:
    #    HeaderMenu(self.testsetup, lookup)
    #Where lookup is:
    #    -the menu name you want to access;
    #    -the menu item number you want to access;
    #Ex:
    #    HeaderMenu(self.testsetup, 'Extensions') returns the Extension menu
    #    HeaderMenu(self.testsetup, 1) returns the Personas menu

    _header_menu_locator = (By.XPATH, '//nav[@id=\'site-nav\']/ul/li')
    _link_locator = (By.CSS_SELECTOR, 'a')
    _header_submenu_list_locator = (By.CSS_SELECTOR, 'ul > li')

    def __init__(self, testsetup, lookup):
        Page.__init__(self, testsetup)
        if type(lookup) == int:
            self._root_element = self.selenium.find_elements(*self._header_menu_locator)[lookup]
        else:
            self._root_element = self.selenium.find_element(self._header_menu_locator[0], '%s[a[text()=\'%s\']]' % (self._header_menu_locator[1], lookup))

    @property
    def name(self):
        return self._root_element.find_element(*self._link_locator).text

    def click(self):
        self._root_element.find_element(*self._link_locator).click()

        if "Extensions" in self.name:
            from pages.extensions import ExtensionsHome
            return ExtensionsHome(self.testsetup)
        elif "Personas" in self.name:
            from pages.personas import Personas
            return Personas(self.testsetup)
        elif "Themes" in self.name:
            from pages.themes import Themes
            return Themes(self.testsetup)
        elif "Collections" in self.name:
            from pages.collection import Collections
            return Collections(self.testsetup)

    @property
    def menu_items(self):
        submenu_list = self._root_element.find_elements(*self._header_submenu_list_locator)
        return [self.SubMenu(self.testsetup, i, self._root_element) for i in range(len(submenu_list))]

    class SubMenu(Page):

        _header_submenu_list_locator = (By.CSS_SELECTOR, 'ul > li')
        _link_tag = (By.CSS_SELECTOR, 'a')

        def __init__(self, testsetup, lookup, root_element):
            Page.__init__(self, testsetup)
            self._root_element = root_element
            self.lookup = lookup
            if type(self.lookup) == int:
                self._submenu_root_element = self._root_element.find_elements(*self._header_submenu_list_locator)[self.lookup]

        @property
        def name(self):
            ActionChains(self.selenium).move_to_element(self._root_element).move_to_element(self._submenu_root_element).perform()
            return self._submenu_root_element.find_element(*self._link_tag).text

        @property
        def is_featured(self):
            return self._submenu_root_element.find_element(By.CSS_SELECTOR, '*').tag_name == 'em'

        def click(self):
            submenu_link = self._submenu_root_element.find_element(*self._link_tag)
            parent_menu_name = self._root_element.find_element(*self._link_locator).text

            ActionChains(self.selenium).move_to_element(self._root_element).\
                move_to_element(submenu_link).\
                click().perform()

            if "Extensions" in parent_menu_name:
                from pages.extensions import ExtensionsHome
                return ExtensionsHome(self.testsetup)
            elif "Personas" in parent_menu_name:
                from pages.personas import Personas
                return Personas(self.testsetup)
            elif "Themes" in parent_menu_name:
                from pages.themes import Themes
                return Themes(self.testsetup)
            elif "Collections" in parent_menu_name:
                from pages.collection import Collections
                return Collections(self.testsetup)

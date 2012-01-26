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

    _menu_items_locator = (By.CSS_SELECTOR, 'ul > li')
    _name_locator = (By.CSS_SELECTOR, 'a')

    def __init__(self, testsetup, element):
        Page.__init__(self, testsetup)
        self._root_element = element

    @property
    def name(self):
        return self._root_element.find_element(*self._name_locator).text

    def click(self):
        self._root_element.find_element(*self._name_locator).click()

        if "EXTENSIONS" in menu_item_name:
            from pages.extensions import ExtensionsHome
            return ExtensionsHome(self.testsetup)
        elif "PERSONAS" in menu_item_name:
            from pages.personas import Personas
            return Personas(self.testsetup)
        elif "THEMES" in menu_item_name:
            from pages.themes import Themes
            return Themes(self.testsetup)
        elif "COLLECTIONS" in menu_item_name:
            from pages.collection import Collections
            return Collections(self.testsetup)

    def hover(self):
       element = self._root_element.find_element(*self._name_locator)
       ActionChains(self.selenium).move_to_element(element).perform()

    @property
    def items(self):
        return [self.HeaderMenuItem(self.testsetup, element, self)
                for element in self._root_element.find_elements(*self._menu_items_locator)]

    class HeaderMenuItem (Page):

        _name_locator = (By.CSS_SELECTOR, 'a')

        def __init__(self, testsetup, element, menu):
            Page.__init__(self, testsetup)
            self._root_element = element
            self._menu = menu

        @property
        def name(self):
            self._menu.hover()
            return self._root_element.find_element(*self._name_locator).text

        @property
        def is_featured(self):
            return self._root_element.find_element(By.CSS_SELECTOR, '*').tag_name == 'em'

        def click(self):
            menu_name = self._menu.name
            self._menu.hover()
            ActionChains(self.selenium).\
                move_to_element(self._root_element).\
                click().\
                perform()

            if "EXTENSIONS" in menu_name:
                from pages.extensions import ExtensionsHome
                return ExtensionsHome(self.testsetup)
            elif "PERSONAS" in menu_name:
                from pages.personas import Personas
                return Personas(self.testsetup)
            elif "THEMES" in menu_name:
                from pages.themes import Themes
                return Themes(self.testsetup)
            elif "COLLECTIONS" in menu_name:
                from pages.collection import Collections
                return Collections(self.testsetup)

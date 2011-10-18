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

    _header_menu_locator = 'css=#site-nav > ul > li'
    _link_locator = '> a'
    _menu_count_locator = '>ul > li'

    def __init__(self, testsetup, lookup):
        Page.__init__(self, testsetup)
        self.lookup = lookup

    def absolute_locator(self, relative_locator):
        return self._root_locator + relative_locator

    @property
    def _root_locator(self):
        if type(self.lookup) == int:
            # lookup by index
            return "%s:nth(%s) " % (self._header_menu_locator, self.lookup)
        else:
            # lookup by name
            return "%s:contains(%s) " % (self._header_menu_locator, self.lookup)

    @property
    def _menu_count(self):
        return self.selenium.get_css_count(self.absolute_locator(self._menu_count_locator))

    @property
    def menu(self):
        #TODO: hover
        return [self.Menu(self.testsetup, i, self.absolute_locator(self._menu_count_locator)) for i in range(self._menu_count)]

    @property
    def name(self):
        return self.selenium.get_text(self.absolute_locator(self._link_locator))

    def click(self):
        self.selenium.click(self.absolute_locator(self._link_locator))
        self.selenium.wait_for_page_to_load(self.timeout)

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

    class Menu(Page):

        _link_tag = "a"
        _featured_tag = "> em"

        def __init__(self, testsetup, lookup, locator):
            Page.__init__(self, testsetup)
            self.lookup = lookup
            self.locator = locator

        def absolute_locator(self, relative_locator):
            return self._root_locator + relative_locator

        @property
        def _root_locator(self):
            if type(self.lookup) == int:
                # lookup by index
                return "%s:nth(%s) " % (self.locator, self.lookup)
            else:
                # lookup by name
                return "%s:contains(%s) " % (self.locator, self.lookup)

        @property
        def name(self):
            return self.selenium.get_text(self.absolute_locator(self._link_tag))

        def click(self):
            self.selenium.click(self.absolute_locator(self._link_locator))
            self.selenium.wait_for_page_to_load(self.timeout)

            if "Extensions" in self.absolute_locator(self._link_locator):
                from pages.extensions import ExtensionsHome
                return ExtensionsHome(self.testsetup)
            elif "Personas" in self.absolute_locator(self._link_locator):
                from pages.personas import Personas
                return Personas(self.testsetup)
            elif "Themes" in self.absolute_locator(self._link_locator):
                from pages.themes import Themes
                return Themes(self.testsetup)
            elif "Collections" in self.absolute_locator(self._link_locator):
                from pages.collection import Collections
                return Collections(self.testsetup)

        @property
        def is_featured(self):
            #Todo: transform in visible after hover
            return self.selenium.is_element_present(self.absolute_locator(self._featured_tag))

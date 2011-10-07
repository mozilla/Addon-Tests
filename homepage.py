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
#                 David Burns
#                 Marc George
#                 Dave Hunt <dhunt@mozilla.com>
#                 Alex Rodionov <p0deje@gmail.com>
#                 Joel Andersson <janderssn@gmail.com>
#                 Marlena Compton <mcompton@mozilla.com>
#                 Teodosia Pop <teodosia.pop@softvision.ro>
#                 Alex Lakatos <alex@greensqr.com>
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

from base_page import BasePage
from page import Page


class HomePage(BasePage):

    _page_title = "Add-ons for Firefox"

    _themes_link_locator = "css=#themes > a"
    _personas_link_locator = "css=#personas > a"
    _collections_link_locator = "css=#collections > a"
    _first_addon_locator = "css=div.summary > a > h3"
    _other_applications_link_locator = "id=other-apps"

    #Most Popular List
    _most_popular_list_locator = "css=#homepage > .secondary"
    _most_popular_item_locator = "css=ol.toplist li"
    _most_popular_list_heading_locator = _most_popular_list_locator + " h2"

    _explore_featured_link_locator = "css=#side-nav .s-featured a"
    _explore_most_popular_link_locator = "css=#side-nav .s-users a"
    _explore_most_top_rated_link_locator = "css=#side-nav .s-rating a"

    _featured_personas_see_all_link = "css=#featured-personas h2 a"
    _featured_personas_locator = "id=featured-personas"
    _featured_personas_title_locator = "css=#featured-personas h2"
    _featured_personas_items_locator = "css=#featured-personas li"

    _category_list_locator = "css=ul#side-categories"

    _extensions_menu_link = "css=#extensions > a"

    def __init__(self, testsetup):
        ''' Creates a new instance of the class and gets the page ready for testing '''
        BasePage.__init__(self, testsetup)
        self.selenium.open("%s/" % self.site_version)
        self.selenium.window_maximize()

    def click_featured_personas_see_all_link(self):
        self.selenium.click(self._featured_personas_see_all_link)
        self.selenium.wait_for_page_to_load(self.timeout)
        from personas_page import PersonasPage
        return PersonasPage(self.testsetup)

    def click_personas(self):
        self.selenium.click(self._personas_link_locator)
        self.selenium.wait_for_page_to_load(self.timeout)
        from personas_page import PersonasPage
        return PersonasPage(self.testsetup)

    def click_themes(self):
        self.wait_for_element_visible(self._themes_link_locator)
        self.selenium.click(self._themes_link_locator)
        self.selenium.wait_for_page_to_load(self.timeout)
        from themes_page import ThemesPage
        return ThemesPage(self.testsetup)

    def click_collections(self):
        self.selenium.click(self._collections_link_locator)
        self.selenium.wait_for_page_to_load(self.timeout)
        from collection_page import CollectionsPage
        return CollectionsPage(self.testsetup)

    def click_extensions(self):
        self.selenium.click(self._extensions_menu_link)
        self.selenium.wait_for_page_to_load(self.timeout)
        from extensions_homepage import ExtensionsHomePage
        return ExtensionsHomePage(self.testsetup)

    def click_to_explore(self, what):
        what = what.replace(' ', '_').lower()
        self.selenium.click(getattr(self, "_explore_most_%s_link_locator" % what))
        self.selenium.wait_for_page_to_load(self.timeout)
        from extensions_homepage import ExtensionsHomePage
        return ExtensionsHomePage(self.testsetup)

    @property
    def most_popular_count(self):
        return self.selenium.get_css_count(self._most_popular_item_locator)

    @property
    def is_most_popular_list_visible(self):
        return self.selenium.is_visible(self._most_popular_list_locator)

    @property
    def most_popular_list_heading(self):
        return self.selenium.get_text(self._most_popular_list_heading_locator)

    @property
    def is_featured_personas_visible(self):
        return self.selenium.is_visible(self._featured_personas_locator)

    @property
    def featured_personas_count(self):
        return self.selenium.get_css_count(self._featured_personas_items_locator)

    @property
    def fetaured_personas_title(self):
        return self.selenium.get_text(self._featured_personas_title_locator)

    def click_on_first_addon(self):
        self.selenium.click(self._first_addon_locator)
        self.selenium.wait_for_page_to_load(self.timeout)
        from details_page import DetailsPage
        return DetailsPage(self.testsetup)

    def get_title_of_link(self, name):
        name = name.lower().replace(" ", "_")
        locator = getattr(self, "_%s_link_locator" % name)
        return self.selenium.get_attribute("%s@title" % locator)

    @property
    def categories_count(self):
        return self.selenium.get_css_count("%s li" % self._category_list_locator)

    def categories(self):
        return [self.Categories(self.testsetup, i) for i in range(self.categories_count)]

    def category(self, lookup):
        return self.Categories(self.testsetup, lookup)

    def most_popular_item(self, lookup):
        return self.MostPopularRegion(self.testsetup, lookup)

    @property
    def most_popular_items(self):
        return [self.MostPopularRegion(self.testsetup, i) for i in range(self.most_popular_count)]

    class Categories(Page):
        _categories_locator = 'css=#side-categories li'
        _link_locator = 'a'

        def __init__(self, testsetup, lookup):
            Page.__init__(self, testsetup)
            self.lookup = lookup

        def absolute_locator(self, relative_locator=""):
            return self._root_locator + relative_locator

        @property
        def _root_locator(self):
            if type(self.lookup) == int:
                # lookup by index
                return "%s:nth(%s) " % (self._categories_locator, self.lookup)
            else:
                # lookup by name
                return "%s:contains(%s) " % (self._categories_locator, self.lookup)

        @property
        def name(self):
            return self.selenium.get_text(self.absolute_locator())

        def click_link(self):
            self.selenium.click(self.absolute_locator(self._link_locator))
            self.selenium.wait_for_page_to_load(self.timeout)
            from category_page import CategoryPage
            return CategoryPage(self.testsetup)

    class MostPopularRegion(Page):
        _name_locator = " > span"
        _users_locator = " > small"

        def __init__(self, testsetup, lookup):
            Page.__init__(self, testsetup)
            self.lookup = lookup

        def absolute_locator(self, relative_locator):
            return self.root_locator + relative_locator

        @property
        def root_locator(self):
            if type(self.lookup) == int:
                # lookup by index
                return "css=.toplist > li:nth(%s) > a" % self.lookup
            else:
                # lookup by name
                return "css=.toplist > li:contains(%s) > a" % self.lookup

        @property
        def name(self):
            return self.selenium.get_text(self.absolute_locator(self._name_locator))

        @property
        def users_text(self):
            return self.selenium.get_text(self.absolute_locator(self._users_locator))

        @property
        def users_number(self):
            number_str = self.users_text.split(' ')[0]
            number_str = number_str.replace(",", "")
            return int(number_str)
            from category_page import CategoryPage
            return CategoryPage(self.testsetup)

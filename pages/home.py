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

from selenium.webdriver.common.by import By

from pages.page import Page
from pages.base import Base


class Home(Base):

    _page_title = "Add-ons for Firefox"
    _themes_link_locator = (By.CSS_SELECTOR, "#themes > a")
    _personas_link_locator = (By.CSS_SELECTOR, "#personas > a")
    _collections_link_locator = (By.CSS_SELECTOR, "#collections > a")
    _first_addon_locator = (By.CSS_SELECTOR, "div.summary > a > h3")
    _other_applications_link_locator = (By.ID, "other-apps")

    #Most Popular List
    _most_popular_item_locator = (By.CSS_SELECTOR, "ol.toplist li")
    _most_popular_list_heading_locator = (By.CSS_SELECTOR, "#homepage > .secondary h2")

    _explore_featured_link_locator = (By.CSS_SELECTOR, "#side-nav .s-featured a")
    _explore_most_popular_link_locator = (By.CSS_SELECTOR, "#side-nav .s-users a")
    _explore_most_top_rated_link_locator = (By.CSS_SELECTOR, "#side-nav .s-rating a")

    _featured_personas_see_all_link = (By.CSS_SELECTOR, "#featured-personas h2 a")
    _featured_personas_title_locator = (By.CSS_SELECTOR, "#featured-personas h2")
    _featured_personas_items_locator = (By.CSS_SELECTOR, "#featured-personas li")

    _featured_collections_locator = (By.CSS_SELECTOR, "#featured-collections h2")
    _featured_collections_elements_locator = (By.CSS_SELECTOR, "#featured-collections section:nth-child(1) li")

    _category_list_locator = (By.CSS_SELECTOR, "ul#side-categories li")

    _extensions_menu_link = (By.CSS_SELECTOR, "#extensions > a")

    def __init__(self, testsetup, open_url=True):
        ''' Creates a new instance of the class and gets the page ready for testing '''
        Base.__init__(self, testsetup)
        if open_url:
            self.selenium.get(self.base_url)

    def click_featured_personas_see_all_link(self):
        self.selenium.find_element(*self._featured_personas_see_all_link).click()
        from pages.personas import Personas
        return Personas(self.testsetup)

    def click_personas(self):
        self.selenium.find_element(*self._personas_link_locator).click()
        from pages.personas import Personas
        return Personas(self.testsetup)

    def click_themes(self):
        self.selenium.find_element(*self._themes_link_locator).click()
        from pages.themes import Themes
        return Themes(self.testsetup)

    def click_collections(self):
        self.selenium.find_element(*self._collections_link_locator).click()
        from pages.collection import Collections
        return Collections(self.testsetup)

    def click_extensions(self):
        self.selenium.find_element(*self._extensions_menu_link).click()
        from pages.extensions import ExtensionsHome
        return ExtensionsHome(self.testsetup)

    def click_featured_collections_see_all_link(self):
        self.selenium.find_element(*self._featured_collections_locator).find_element(By.CSS_SELECTOR, " a").click()
        from pages.collection import Collections
        return Collections(self.testsetup)

    def click_to_explore(self, what):
        what = what.replace(' ', '_').lower()
        self.selenium.find_element(*getattr(self, "_explore_most_%s_link_locator" % what)).click()
        from pages.extensions import ExtensionsHome
        return ExtensionsHome(self.testsetup)

    @property
    def most_popular_count(self):
        return len(self.selenium.find_elements(*self._most_popular_item_locator))

    @property
    def most_popular_list_heading(self):
        return self.selenium.find_element(*self._most_popular_list_heading_locator).text

    @property
    def featured_personas_count(self):
        return len(self.selenium.find_elements(*self._featured_personas_items_locator))

    @property
    def featured_personas_title(self):
        return self.selenium.find_element(*self._featured_personas_title_locator).text

    @property
    def featured_collections_title(self):
        return self.selenium.find_element(*self._featured_collections_locator).text

    @property
    def featured_collections_count(self):
        return len(self.selenium.find_elements(*self._featured_collections_elements_locator))

    def click_on_first_addon(self):
        self.selenium.find_element(*self._first_addon_locator).click()
        from pages.details import Details
        return Details(self.testsetup)

    def get_title_of_link(self, name):
        name = name.lower().replace(" ", "_")
        locator = getattr(self, "_%s_link_locator" % name)
        return self.selenium.find_element(*locator).get_attribute('title')

    @property
    def categories(self):
        return [self.Categories(self.testsetup, element)
                for element in self.selenium.find_elements(*self._category_list_locator)]

    def category(self, element):
        return self.Categories(self.testsetup, element)

    @property
    def most_popular_items(self):
        return [self.MostPopularRegion(self.testsetup, element)
                for element in self.selenium.find_elements(*self._most_popular_item_locator)]

    class Categories(Page):
        _link_locator = (By.CSS_SELECTOR, 'a')

        def __init__(self, testsetup, element):
            Page.__init__(self, testsetup)
            self._root_element = element

        @property
        def name(self):
            return self._root_element.text

        def click_link(self):
            self._root_element.find_element(*self._link_locator).click()
            from pages.category import Category
            return Category(self.testsetup)

    class MostPopularRegion(Page):
        _name_locator = (By.TAG_NAME, "span")
        _users_locator = (By.CSS_SELECTOR, "small")

        def __init__(self, testsetup, element):
            Page.__init__(self, testsetup)
            self._root_element = element

        @property
        def name(self):
            self._root_element.find_element(*self._name_locator).text

        @property
        def users_number(self):
            users_text = self._root_element.find_element(*self._users_locator).text
            return int(users_text.split(' ')[0].replace(',', ''))

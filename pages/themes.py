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
# Contributor(s): David Burns
#                 Marc George
#                 Dave Hunt <dhunt@mozilla.com>
#                 Alex Rodionov <p0deje@gmail.com>
#                 Joel Andersson <janderssn@gmail.com>
#                 Bebe <florin.strugariu@softvision.ro>
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
from selenium.webdriver.common.action_chains import ActionChains

from pages.base import Base


class Themes(Base):

    _sort_by_name_locator = (By.CSS_SELECTOR, "li.extras > ul > li:nth-child(1) > a")
    _sort_by_updated_locator = (By.CSS_SELECTOR, "li.extras > ul > li:nth-child(4) > a")
    _sort_by_created_locator = (By.CSS_SELECTOR, "div#sorter > ul > li:nth-child(3) > a")
    _sort_by_popular_locator = (By.CSS_SELECTOR, "li.extras > ul > li:nth-child(3) > a")
    _sort_by_rating_locator = (By.CSS_SELECTOR, "div#sorter > ul > li:nth-child(2) > a")
    _hover_more_locator = (By.CSS_SELECTOR, "li.extras > a")
    _addons_root_locator = (By.XPATH, "// div[@class = 'hovercard addon theme']")
    _addon_name_locator = (By.XPATH, _addons_root_locator[1] + " / a / div[@class='summary'] / h3")
    _addons_metadata_locator = (By.XPATH, _addons_root_locator[1] + " // div[@class = 'vital']/span[@class='updated']")
    _addons_download_locator = (By.XPATH, _addons_root_locator[1] + " / div[@class = 'vital']/span[@class='adu']")
    _addons_rating_locator = (By.XPATH, _addons_metadata_locator[1] + " / span / span")
    _category_locator = (By.CSS_SELECTOR, "#c-30 > a")
    _categories_locator = (By.CSS_SELECTOR, "#side-categories li")
    _category_link_locator = (By.CSS_SELECTOR, _categories_locator[1] + ":nth-of-type(%s) a")
    _next_link_locator = (By.CSS_SELECTOR, ".paginator .rel > a:nth-child(3)")
    _previous_link_locator = (By.CSS_SELECTOR, ".paginator .rel > a:nth-child(2)")

    def click_sort_by(self, type_):
        click_target = self.selenium.find_element(*getattr(self, "_sort_by_%s_locator" % type_))
        hover_element = self.selenium.find_element(*self._hover_more_locator)
        footer = self.selenium.find_element(*self._footer_locator)
        ActionChains(self.selenium).\
            move_to_element(footer).\
            move_to_element(hover_element).\
            move_to_element(click_target).\
            click().perform()

    def click_on_first_addon(self):
        self.selenium.find_element(*self._addon_name_locator).click()
        return Theme(self.testsetup)

    def click_on_first_category(self):
        self.selenium.find_element(*self._category_locator).click()
        return ThemesCategory(self.testsetup)

    def get_category(self, lookup):
        return self.selenium.find_element(self._category_link_locator[0],
                                          self._category_link_locator[1] % lookup).text

    @property
    def themes_category(self):
        return self.selenium.find_element(*self._category_locator).text

    @property
    def categories_count(self):
        return len(self.selenium.find_elements(*self._categories_locator))

    @property
    def addon_names(self):
        addon_name = []
        for addon in self.selenium.find_elements(*self._addon_name_locator):
            ActionChains(self.selenium).move_to_element(addon).perform()
            addon_name.append(addon.text)
        return addon_name

    def addon_name(self, lookup):
        return self.selenium.find_element(By.XPATH,
                                          "//li[%s] %s" % (lookup, self._addon_name_locator[1])).text

    @property
    def addon_count(self):
        return len(self.selenium.find_elements(*self._addon_name_locator))

    @property
    def addon_updated_dates(self):
        return self._extract_iso_dates("Updated %B %d, %Y", *self._addons_metadata_locator)

    @property
    def addon_created_dates(self):
        return self._extract_iso_dates("Added %B %d, %Y", *self._addons_metadata_locator)

    @property
    def addon_download_number(self):
        pattern = "(\d+(?:[,]\d+)*) weekly downloads"
        downloads = self._extract_integers(pattern, *self._addons_download_locator)
        return downloads

    @property
    def addon_rating(self):
        pattern = "(\d)"
        ratings = self._extract_integers(pattern, *self._addons_rating_locator)
        return ratings

    def page_forward(self):
        footer = self.selenium.find_element(*self._footer_locator)
        forward = self.selenium.find_element(*self._next_link_locator)

        ActionChains(self.selenium).move_to_element(footer).\
            move_to_element(forward).\
            click().perform()

    def page_back(self):
        footer = self.selenium.find_element(*self._footer_locator)
        back = self.selenium.find_element(*self._previous_link_locator)

        ActionChains(self.selenium).move_to_element(footer).\
            move_to_element(back).\
            click().perform()


class Theme(Base):

    _addon_title = (By.CSS_SELECTOR, "h1.addon")

    @property
    def addon_title(self):
        return self.selenium.find_element(*self._addon_title).text


class ThemesCategory(Base):

    _title_locator = (By.CSS_SELECTOR, "section.primary > h1")
    _breadcrumb_locator = (By.CSS_SELECTOR, "#breadcrumbs > ol")

    @property
    def title(self):
        return self.selenium.find_element(*self._title_locator).text

    @property
    def breadcrumb(self):
        return self.selenium.find_element(*self._breadcrumb_locator).text.replace('\n', ' ')

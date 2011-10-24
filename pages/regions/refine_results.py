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


class FilterBase(Page):

    def __init__(self, testsetup):
        Page.__init__(self, testsetup)

    def _absolute_locator(self, tag):
        return'%s %s' % (self._locator, tag)


class FilterResults(FilterBase):

    _locator = 'css=#search-facets'

    _title_tag = '> h2'
    _results_count_tag = '> p'
    _filter_tag = '> ul.facets >li.facet:contains(%s)'

    def __init__(self, testsetup):
        FilterBase.__init__(self, testsetup)

    @property
    def title(self):
        return self.selenium.get_text(self._absolute_locator(self._title_tag))

    @property
    def results_count_text(self):
        return self.selenium.get_text(self._absolute_locator(self._results_count_tag))

    @property
    def results_count_int(self):
        return int(self.selenium.get_text(self._absolute_locator(self._results_count_tag)).split()[0])

    def select_area(self, area):
        self.selenium.click(self._absolute_locator(self._filter_tag % area))
        self.wait_for_element_visible('%s > ul' % (self._absolute_locator(self._filter_tag % area)))
        if area.lower() == "category":
            return Category(self.testsetup, self._absolute_locator(self._filter_tag % area))
        elif area.lower() == "works with":
            return WorksWith(self.testsetup, self._absolute_locator(self._filter_tag % area))
        elif area.lower() == "tag":
            return Tag(self.testsetup, self._absolute_locator(self._filter_tag % area))


class Category(FilterBase):

    _filter_type_name_tag = '> h3'
    _categories_tag = '> ul.facet-group > li'

    def __init__(self, testsetup, locator):
        FilterBase.__init__(self, testsetup)
        self._locator = locator

    @property
    def name(self):
        return self.selenium.get_text(self._absolute_locator(self._filter_type_name_tag))

    @property
    def _category_count(self):
        return int(self.selenium.get_css_count(self._absolute_locator(self._categories_tag)))

    @property
    def sub_categories(self):
        return [self.SubCategories(self.testsetup, self._absolute_locator(self._categories_tag), i) for i in range(self._category_count)]

    class SubCategories(FilterBase):

        _link_tag = '> a'
        _items_tag = '> ul > li'

        def __init__(self, testsetup, locator, lookup):
            FilterBase.__init__(self, testsetup)
            self._lookup = lookup
            self._locator = locator

        def _absolute_locator(self, tag=""):
            return'%s:nth(%s)%s' % (self._locator, self._lookup, tag)

        @property
        def name(self):
            return self.selenium.get_text(self._absolute_locator(self._link_tag))

        def click(self):
            self.selenium.click(self._absolute_locator(self._name_tag))
            self.selenium.wait_for_page_to_load(self.timeout)

        @property
        def is_selected(self):
            try:
                return "selected" in self.selenium.get_attribute('%s@class' % self._absolute_locator())
            except:
                return False

        @property
        def _item_count(self):
            return self.selenium.get_css_count(self._absolute_locator(self._items_tag))

        @property
        def items(self):
            return [FilterItem(self.testsetup, self._absolute_locator(self._items_tag), i) for i in range(self._item_count)]


class WorksWith(FilterBase):

    _filter_type_name_tag = '> h3'
    _options_tag = '> ul.facet-group:nth(%s) > li'

    def __init__(self, testsetup, locator):
        FilterBase.__init__(self, testsetup)
        self._locator = locator

    @property
    def name(self):
        return self.selenium.get_text(self._absolute_locator(self._filter_type_name_tag))

    @property
    def firefox_version(self):
        count = self.selenium.get_css_count(self._absolute_locator(self._options_tag % '0'))
        return [FilterItem(self.testsetup, self._absolute_locator(self._options_tag % '0'), i) for i in range(count)]

    @property
    def os(self):
        count = self.selenium.get_css_count(self._absolute_locator(self._options_tag % '1'))
        return [FilterItem(self.testsetup, self._absolute_locator(self._options_tag % '1'), i) for i in range(count)]


class Tag(FilterBase):

    _filter_type_name_tag = '> h3'
    _options_tag = '> ul.facet-group > li'

    def __init__(self, testsetup, locator):
        FilterBase.__init__(self, testsetup)
        self._locator = locator

    @property
    def name(self):
        return self.selenium.get_text(self._absolute_locator(self._filter_type_name_tag))

    @property
    def tags(self):
        count = self.selenium.get_css_count(self._absolute_locator(self._options_tag))
        return [FilterItem(self.testsetup, self._absolute_locator(self._options_tag), i) for i in range(count)]

    def tag(self, lookup):
        return FilterItem(self.testsetup, self._absolute_locator(self._options_tag), lookup)


class FilterItem(FilterBase):

    _name_tag = '> a'

    def __init__(self, testsetup, locator, lookup):
        FilterBase.__init__(self, testsetup)
        self._locator = locator
        self._lookup = lookup

    def _absolute_locator(self, tag=''):
        if type(self._lookup) == int:
            # lookup by index
            return '%s:nth(%s)%s' % (self._locator, self._lookup, tag)
        else:
            # lookup by name
            return '%s:contains(%s)%s' % (self._locator, self._lookup, tag)
#        return'%s:nth(%s)%s' % (self._locator, self._lookup, tag)

    @property
    def name(self):
        return self.selenium.get_text(self._absolute_locator())

    def click(self):
        self.selenium.click(self._absolute_locator(self._name_tag))
        self.selenium.wait_for_page_to_load(self.timeout)

    @property
    def is_selected(self):
        try:
            return "selected" in self.selenium.get_attribute('%s@class' % self._absolute_locator())
        except:
            return False

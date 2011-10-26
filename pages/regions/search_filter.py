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

from pages.page import Page


class FilterBase(Page):

    _results_count_tag = 'css=p.cnt'

    def tag(self, lookup):
        return self.Tag(self.testsetup, lookup)

    @property
    def results_count_int(self):
        return int(self.selenium.get_text(self._results_count_tag).split()[0])

    class FilterResults(Page):

        _item = " ul.facet-group li:contains(%s)"
        _item_link = " > a"

        def __init__(self, testsetup, lookup):
            Page.__init__(self, testsetup)
            # expand the thing here to represent the proper user action
            self.selenium.click(self._base_locator)

            #ul.facets li.facet:nth(2) li:contains('development')
            self._root_locator = self._base_locator + self._item % lookup

        @property
        def name(self):
            return self.selenium.get_text(self._root_locator)

        @property
        def is_selected(self):
            return "selected" in self.selenium.get_attribute('%s@class' % self._root_locator)

        def click(self):
            self.selenium.click(self._root_locator + self._item_link)
            self.selenium.wait_for_page_to_load(self.timeout)


    class Tag(FilterResults):
        _base_locator = "css=ul.facets > li.facet:nth(2)"

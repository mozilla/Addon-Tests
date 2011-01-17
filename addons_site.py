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
# Portions created by the Initial Developer are Copyright (C) 2010
# the Initial Developer. All Rights Reserved.
#
# Contributor(s): David Burns
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


from selenium import selenium
from vars import ConnectionParameters
from page import Page

page_load_timeout = ConnectionParameters.page_load_timeout

class AddonsHomePage(Page):

    #Search box
    _search_button_locator = "css=input.submit"
    _search_textbox_locator = "name=q"

    def __init__(self, selenium):
        ''' Creates a new instance of the class and gets the page ready for testing '''
        self.sel = selenium
        self.sel.open("/")
        self.sel.window_maximize()

    def search_for(self,search_term):
        self.sel.type(self._search_textbox_locator, search_term)
        self.sel.click(self._search_button_locator)
        self.sel.wait_for_page_to_load(page_load_timeout)
        return AddonsSearchHomePage(self.sel)


class AddonsSearchHomePage(AddonsHomePage):

    _next_link = "link=Next"
    _prev_link = "link=Prev"
    _results_count_header = "css=h3.results-count"
    _page_counter = "css=div.num-results"

    def __init__(self, selenium):
        self.selenium = selenium

    @property
    def results_count(self):
        return self.selenium.get_text(self._results_count_header)

    @property
    def page_results_count(self):
        return self.selenium.get_text(self._page_counter)

    def page_forward(self):
        self.selenium.click(self._next_link)
        self.selenium.wait_for_page_to_load("30000")

    def page_back(self):
        self.selenium.click(self._prev_link)
        self.selenium.wait_for_page_to_load("30000") 

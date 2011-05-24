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


import re

from page import Page


class AddonsHomePage(Page):

    #Search box
    _search_button_locator = "css=input.submit"
    _search_textbox_locator = "name=q"
    _download_count_locator = "css=div.stats > strong"
    _themes_link_locator = "id=_t-2"
    _personas_link_locator = "id=_t-9"

    #Categories List
    _category_list_locator = "//ul[@id='categoriesdropdown']"

    #prev next links
    _next_link = "link=Next"
    _prev_link = "link=Prev"

    def __init__(self, testsetup):
        ''' Creates a new instance of the class and gets the page ready for testing '''
        Page.__init__(self, testsetup)
        self.selenium.open("/") 
        self.selenium.window_maximize()

    def search_for(self,search_term):
        self.selenium.type(self._search_textbox_locator, search_term)
        self.selenium.click(self._search_button_locator)
        self.selenium.wait_for_page_to_load(self.timeout)
        return AddonsSearchHomePage(self.testsetup)        
        
    def has_category(self, category_name):
        ''' Returns whether category_name exists in the category menu links'''
        locator = self._xpath_for_category(category_name)
        return self.selenium.get_xpath_count(locator) > 0

    def click_personas(self):
        self.selenium.click(self._personas_link_locator)
        self.selenium.wait_for_page_to_load(self.timeout)
        return AddonsPersonasPage(self.testsetup)

    def click_themes(self):
        self.selenium.click(self._themes_link_locator)
        self.selenium.wait_for_page_to_load(self.timeout)
        return AddonsThemesPage(self.testsetup)
        
    def page_forward(self):
        self.selenium.click(self._next_link)
        self.selenium.wait_for_page_to_load(self.timeout)

    def page_back(self):
        self.selenium.click(self._prev_link)
        self.selenium.wait_for_page_to_load(self.timeout)

    @property
    def download_count(self):
        return self.selenium.get_text(self._download_count_locator)


class AddonsSearchHomePage(AddonsHomePage):

    _results_count_header = "css=h3.results-count"
    _page_counter = "css=div.num-results"

    def __init__(self, testsetup):
        Page.__init__(self, testsetup)

    @property
    def results_count(self):
        return self.selenium.get_text(self._results_count_header)

    @property
    def page_results_count(self):
        return self.selenium.get_text(self._page_counter)
    
    @property
    def page_title(self):
        return self.selenium.get_title()


class AddonsThemesPage(AddonsHomePage):

    _sort_by_name_locator = 'name=_t-name'
    _sort_by_updated_locator = 'name=_t-updated'
    _sort_by_created_locator = 'name=_t-created'
    _sort_by_downloads_locator = 'name=_t-popular'
    _sort_by_rating_locator = 'name=_t-rating'
    _addons_root_locator = "//div[@class='details']"
    _addon_name_locator = _addons_root_locator + "/h4/a"
    _addons_metadata_locator = _addons_root_locator + "/p[@class='meta']"
    _addons_rating_locator = _addons_metadata_locator + "/span/span"

    def __init__(self, testsetup):
        Page.__init__(self, testsetup)

    def click_sort_by(self, type_):
        self.selenium.click(getattr(self, "_sort_by_%s_locator" % type_))
        self.selenium.wait_for_page_to_load(self.timeout)

    @property
    def addon_names(self):
        addon_count = int(self.selenium.get_xpath_count(self._addon_name_locator))
        _addon_names = [self.selenium.get_text("xpath=(" + self._addon_name_locator + ")[%s]" % str(i+1))
                        for i in xrange(addon_count)]
        return _addon_names
    
    @property
    def addon_update_dates(self):
        addon_count = int(self.selenium.get_xpath_count(self._addon_name_locator))
        _addon_dates = [self.selenium.get_text(
                            "xpath=(" + self._addons_metadata_locator + ")[%s]" % str(i+1))[8:]
                        for i in xrange(addon_count)]
        return _addon_dates

    @property
    def addon_download_number(self):
        addon_count = int(self.selenium.get_xpath_count(self._addon_name_locator))
        _addon_downloads= [int(re.search("(\d+)", self.selenium.get_text(
                            "xpath=(" + self._addons_metadata_locator + ")[%s]" % str(i+1)).replace(
                                ",","")).group(0))
                        for i in xrange(addon_count)]
        return _addon_downloads

    @property
    def addon_rating(self):
        addon_count = int(self.selenium.get_xpath_count(self._addon_name_locator))
        _addon_ratings = [self.selenium.get_text("xpath=(" + self._addons_rating_locator + ")[%s]" % str(i+1))
                        for i in xrange(addon_count)]
        return _addon_ratings


class AddonsPersonasPage(AddonsHomePage):

    def __init__(self, testsetup):
        Page.__init__(self, testsetup)

    @property
    def page_title(self):
        return self.selenium.get_title()


class DiscoveryPane(Page):

    _what_are_addons_section_locator = 'id=intro'
    _what_are_addons_text_locator = 'css=#intro p'
    _mission_section_locator = 'id=mission'
    _mission_section_text_locator = 'css=#mission > p'
    _learn_more_locator = 'link=Learn More' #Using link till 631557 implemented
    _mozilla_org_link_locator = "css=a[href=http://www.mozilla.org/]"
    _download_count_text_locator = "id=download-count"
    _personas_section_locator = "id=featured-personas"
    _personas_see_all_link = "css=.all[href='/en-US/firefox/personas/']"
    _personas_locator = "//span[@class='addon-title']/b"
    _more_ways_section_locator = "id=more-ways"
    _more_ways_addons_locator = "id=more-addons"
    _more_ways_personas_locator = "id=more-personas"
    _up_and_coming_section = "id=up-and-coming"
    _up_and_coming_item = "//section[@id='up-and-coming']/ul/li/a[@class='addon-title']"

    def __init__(self, testsetup, path):
        Page.__init__(self, testsetup)
        self.selenium.open(testsetup.base_url + path)
        self.selenium.window_maximize()

    @property
    def what_are_addons_text(self):
        return self.selenium.get_text(self._what_are_addons_text_locator)

    def click_learn_more(self):
        self.selenium.click(self._learn_more_locator)
        self.selenium.wait_for_page_to_load(self.timeout)

    def is_mission_section_visible(self):
        return self.selenium.is_visible(self._mission_section_locator)

    @property
    def mission_section(self):
        return self.selenium.get_text(self._mission_section_text_locator)

    def mozilla_org_link_visible(self):
        return self.selenium.is_visible(self._mozilla_org_link_locator)

    @property
    def download_count(self):
        return self.selenium.get_text(self._download_count_text_locator)

    def is_personas_section_visible(self):
        return self.selenium.is_visible(self._personas_section_locator)

    @property
    def personas_count(self):
        return int(self.selenium.get_xpath_count(self._personas_locator))

    def is_personas_see_all_link_visible(self):
        return self.selenium.is_visible(self._personas_see_all_link)

    @property
    def first_persona(self):
        return self.selenium.get_text(self._personas_locator)
    
    def click_on_first_persona(self):
        self.selenium.click(self._personas_locator)
        self.selenium.wait_for_page_to_load(self.timeout)
        return PersonasPage(self.testsetup)

    def more_ways_section_visible(self):
        return self.selenium.is_visible(self._more_ways_section_locator)

    @property
    def more_ways_addons(self):
        return self.selenium.get_text(self._more_ways_addons_locator)

    @property
    def more_ways_personas(self):
        return self.selenium.get_text(self._more_ways_personas_locator)

    def up_and_coming_visible(self):
        return self.selenium.is_visible(self._up_and_coming_section)

    @property
    def up_and_coming_item_count(self):
        return int(self.selenium.get_xpath_count(self._up_and_coming_item))

class PersonasPage(Page):

    _persona_title = 'css=h1.addon'

    @property
    def persona_title(self):
        return self.selenium.get_text(self._persona_title)

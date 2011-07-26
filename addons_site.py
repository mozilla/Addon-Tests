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
from datetime import datetime

from page import Page
from addons_base_page import AddonsBasePage
from addons_user_page import AddonsUserPage
import addons_search_home_page
import image_viewer_region


class AddonsHomePage(AddonsBasePage):

    _page_title = "Add-ons for Firefox"

    #Search box
    _search_button_locator = "css=input.submit"
    _search_textbox_locator = "name=q"
    _download_count_locator = "css=div.stats > strong"
    _themes_link_locator = "id=_t-2"
    _personas_link_locator = "id=_t-9"

    #Categories List
    _category_list_locator = "//ul[@id='categoriesdropdown']"
    _category_item_locator = "//li/a[text()='%s']"

    #prev next links
    _next_link_locator = "link=Next"
    _previous_link_locator = "link=Prev"

    #addons detail page
    _review_details_locator = "css=.review-detail"
    _all_reviews_link_locator = "css=#addon #reviews+.article a.more-info"
    _current_page_locator = "css=.pagination li.selected a"
    _review_locator = "css=.primary div.review"
    _last_page_link_locator = "css=.pagination a:not([rel]):last"
    _first_page_link_locator = "css=.pagination a:not([rel]):first"

    def __init__(self, testsetup):
        ''' Creates a new instance of the class and gets the page ready for testing '''
        AddonsBasePage.__init__(self, testsetup)
        self.selenium.open("%s/" % self.site_version)
        self.selenium.window_maximize()

    def page_forward(self):
        self.selenium.click(self._next_link_locator)
        self.selenium.wait_for_page_to_load(self.timeout)

    def page_back(self):
        self.selenium.click(self._previous_link_locator)
        self.selenium.wait_for_page_to_load(self.timeout)

    def search_for(self, search_term):
        self.selenium.type(self._search_textbox_locator, search_term)
        self.selenium.click(self._search_button_locator)
        self.selenium.wait_for_page_to_load(self.timeout)
        return addons_search_home_page.AddonsSearchHomePage(self.testsetup)

    @property
    def search_field_placeholder(self):
        return self.selenium.get_attribute(self._search_textbox_locator + '@placeholder')

    def has_category(self, category_name):
        ''' Returns whether category_name exists in the category menu links '''
        locator = (self._category_list_locator + self._category_item_locator) % category_name
        return self.selenium.get_xpath_count(locator) > 0

    def click_personas(self):
        self.selenium.click(self._personas_link_locator)
        self.selenium.wait_for_page_to_load(self.timeout)
        return AddonsPersonasPage(self.testsetup)

    def click_themes(self):
        self.selenium.click(self._themes_link_locator)
        self.selenium.wait_for_page_to_load(self.timeout)
        return AddonsThemesPage(self.testsetup)

    def open_details_page_for_id(self, id):
        self.selenium.open("%s/addon/%s" % (self.site_version, id))
        self.selenium.wait_for_page_to_load(self.timeout)

    def click_all_reviews_link(self):
        self.selenium.click(self._all_reviews_link_locator)
        self.selenium.wait_for_page_to_load(self.timeout)

    @property
    def review_count(self):
        return self.selenium.get_css_count(self._review_locator)

    @property
    def has_reviews(self):
        return self.selenium.get_css_count(self._review_details_locator) > 0

    @property
    def is_next_link_present(self):
        return self.selenium.is_element_present(self._next_link_locator)

    @property
    def is_next_link_visible(self):
        return self.selenium.is_visible(self._next_link_locator)

    @property
    def is_prev_link_present(self):
        return self.selenium.is_element_present(self._previous_link_locator)

    @property
    def is_prev_link_visible(self):
        return self.selenium.is_visible(self._previous_link_locator)

    @property
    def current_page(self):
        return int(self.selenium.get_text(self._current_page_locator))

    def go_to_first_page(self):
        self.selenium.click(self._first_page_link_locator)
        self.selenium.wait_for_page_to_load(self.timeout)

    def go_to_last_page(self):
        self.selenium.click(self._last_page_link_locator)
        self.selenium.wait_for_page_to_load(self.timeout)

    @property
    def download_count(self):
        return self.selenium.get_text(self._download_count_locator)

    def _extract_iso_dates(self, xpath_locator, date_format, count):
        """
        Returns a list of iso formatted date strings extracted from
        the text elements matched by the given xpath_locator and
        original date_format.

        So for example, given the following elements:
          <p>Added May 09, 2010</p>
          <p>Added June 11, 2011</p>

        A call to:
          _extract_iso_dates("//p", "Added %B %d, %Y", 2)

        Returns:
          ['2010-05-09T00:00:00','2011-06-11T00:00:00']

        """
        addon_dates = [
            self.selenium.get_text("xpath=(%s)[%d]" % (xpath_locator, i))
            for i in xrange(1, count + 1)
        ]
        iso_dates = [
            datetime.strptime(s, date_format).isoformat()
            for s in addon_dates
        ]
        return iso_dates

    def _extract_integers(self, xpath_locator, regex_pattern, count):
        """
        Returns a list of integers extracted from the text elements
        matched by the given xpath_locator and regex_pattern.
        """
        addon_numbers = [
            self.selenium.get_text("xpath=(%s)[%d]" % (xpath_locator, i))
            for i in xrange(1, count + 1)
        ]
        integer_numbers = [
            int(re.search(regex_pattern, str(x).replace(",", "")).group(1))
            for x in addon_numbers
        ]
        return integer_numbers


class AddonsDetailsPage(AddonsBasePage):

    _name_locator = "css=h2.addon > span"
    _version_number_locator = "css=span.version"
    _authors_locator = "//h4[@class='author']/a"
    _summary_locator = "css=div[id=addon-summary] > p"
    _ratings_locator = "css=span[itemprop='rating']"
    _install_button_locator = "css=p[class='install-button'] > a"
    _contribute_button_locator = "css=a[id='contribute-button']"
    _addon_rating_locator = "css=span[itemprop='rating']"
    _whats_this_license_locator = "css=h5 > span > a"
    _description_locator = "css=div[class='article userinput'] > p"
    _icon_locator = "css=img.icon"
    _featured_image_locator = "css=#addon .featured .screenshot"

    #more about this addon
    _additional_images_locator = "css=#addon .article .screenshot"
    _website_locator = "css=div#addon-summary tr:contains('Website') a"
    _other_addons_by_authors_locator = "css=div.other-author-addons"
    _other_addons_dropdown_locator = "id=addons-author-addons-select"
    _other_addons_link_list_locator = "css=div.other-author-addons ul li"

    _reviews_locator = "css=#reviews div"

    def __init__(self, testsetup, addon_name):
        #formats name for url
        self.addon_name = addon_name.replace(' ', '-').lower()
        AddonsBasePage.__init__(self, testsetup)
        self.selenium.open("%s/addon/%s" % (self.site_version, self.addon_name))

    @property
    def page_title(self):
        return self.selenium.get_title()

    @property
    def name(self):
        return self.selenium.get_text(self._name_locator)

    @property
    def version_number(self):
        return self.selenium.get_text(self._version_number_locator)

    @property
    def authors(self):
        return [self.selenium.get_text(self._authors_locator + "[%s]" % (i + 1))
            for i in range(self.selenium.get_xpath_count(self._authors_locator))]

    @property
    def summary(self):
        return self.selenium.get_text(self._summary_locator)

    @property
    def rating(self):
        return self.selenium.get_text(self._addon_rating_locator)

    def click_whats_this_license(self):
        self.selenium.click(self._whats_this_license_locator)
        self.selenium.wait_for_page_to_load(self.timeout)
        return UserFAQPage(self.testsetup)

    @property
    def description(self):
        return self.selenium.get_text(self._description_locator)

    @property
    def icon_url(self):
        return self.selenium.get_attribute(self._icon_locator + "%s" % "@src")

    @property
    def website(self):
        return self.selenium.get_text(self._website_locator)

    def click_website_link(self):
        self.selenium.open(self.website)

    @property
    def other_addons_by_authors_text(self):
        return self.selenium.get_text("%s > h4" % self._other_addons_by_authors_locator)

    @property
    def is_other_addons_dropdown_present(self):
        return self.selenium.is_element_present(self._other_addons_dropdown_locator)

    @property
    def other_addons_dropdown_values(self):
        return self.selenium.get_select_options(self._other_addons_dropdown_locator)

    def select_other_addons_dropdown_value(self, value):
        self.selenium.select(self._other_addons_dropdown_locator, value)
        self.selenium.wait_for_page_to_load(self.timeout)

    @property
    def other_addons_link_list_count(self):
        return self.selenium.get_css_count(self._other_addons_link_list_locator)

    def other_addons_link_list(self):
        return [self.selenium.get_text("%s:nth(%s) a" % (self._other_addons_link_list_locator, pos))
            for pos in range(self.other_addons_link_list_count)]

    def click_other_addon_by_this_author(self, value):
        self.selenium.click('%s:contains(%s) a' % (self._other_addons_link_list_locator, value))
        self.selenium.wait_for_page_to_load(self.timeout)

    def click_addon_image(self):
        self.selenium.click(self._featured_image_locator)
        image_viewer = image_viewer_region.ImageViewer(self.testsetup)
        image_viewer.wait_for_viewer_to_finish_animating()
        return image_viewer

    @property
    def additional_images_count(self):
        return self.selenium.get_css_count(self._additional_images_locator)

    def click_additional_image(self, index):
        self.selenium.click("%s:nth(%s)" % (self._additional_images_locator, index - 1))
        image_viewer = image_viewer_region.ImageViewer(self.testsetup)
        image_viewer.wait_for_viewer_to_finish_animating()
        return image_viewer

    def review(self, lookup):
        return self.DetailsReviewSnippet(self.testsetup, lookup)

    def reviews(self):
        return [self.DetailsReviewSnippet(self.testsetup, i) for i in range(self.review_count)]

    @property
    def review_count(self):
        self.wait_for_element_visible(self._reviews_locator)
        return int(self.selenium.get_css_count(self._reviews_locator))

    class DetailsReviewSnippet(Page):

        _reviews_locator = "css=#reviews div"  # Base locator
        _username_locator = "p.byline  a"

        def __init__(self, testsetup, lookup):
            Page.__init__(self, testsetup)
            self.lookup = lookup

        def absolute_locator(self, relative_locator):
            return self._root_locator + relative_locator

        @property
        def _root_locator(self):
            self.wait_for_element_visible(self._reviews_locator)
            if type(self.lookup) == int:
                # lookup by index
                return "%s:nth(%s) " % (self._reviews_locator, self.lookup)
            else:
                # lookup by name
                return "%s:contains(%s) " % (self._reviews_locator, self.lookup)

        @property
        def username(self):
            return self.selenium.get_text(self.absolute_locator(self._username_locator))

        def click_username(self):
            self.selenium.click(self.absolute_locator(self._username_locator))
            self.selenium.wait_for_page_to_load(self.timeout)
            return AddonsUserPage(self.testsetup)


class AddonsThemesPage(AddonsHomePage):

    _sort_by_name_locator = 'name=_t-name'
    _sort_by_updated_locator = 'name=_t-updated'
    _sort_by_created_locator = 'name=_t-created'
    _sort_by_popular_locator = 'name=_t-popular'
    _sort_by_rating_locator = 'name=_t-rating'
    _addons_root_locator = "//div[@class='details']"
    _addon_name_locator = _addons_root_locator + "/h4/a"
    _addons_metadata_locator = _addons_root_locator + "/p[@class='meta']"
    _addons_rating_locator = _addons_metadata_locator + "/span/span"
    _breadcrumb_locator = "css=ol.breadcrumbs"
    _category_locator = "css=#c-30 > a"
    _top_counter_locator = "css=div.primary>header b"
    _bottom_counter_locator = "css=div.num-results > strong:nth(2)"

    def __init__(self, testsetup):
        AddonsBasePage.__init__(self, testsetup)

    def click_sort_by(self, type_):
        self.selenium.click(getattr(self, "_sort_by_%s_locator" % type_))
        self.selenium.wait_for_page_to_load(self.timeout)

    def click_on_first_addon(self):
        self.selenium.click(self._addon_name_locator)
        self.selenium.wait_for_page_to_load(self.timeout)
        return AddonsThemePage(self.testsetup)

    def click_on_first_category(self):
        self.selenium.click(self._category_locator)
        self.selenium.wait_for_page_to_load(self.timeout)
        return AddonsThemesCategoryPage(self.testsetup)

    @property
    def page_title(self):
        return self.selenium.get_title()

    @property
    def themes_breadcrumb(self):
        return self.selenium.get_text(self._breadcrumb_locator)

    @property
    def themes_category(self):
        return self.selenium.get_text(self._category_locator)

    @property
    def addon_names(self):
        addon_count = int(self.selenium.get_xpath_count(self._addon_name_locator))
        _addon_names = [self.selenium.get_text("xpath=(" + self._addon_name_locator + ")[%s]" % str(i + 1))
                        for i in xrange(addon_count)]
        return _addon_names

    @property
    def addon_count(self):
        count = self.selenium.get_xpath_count(self._addon_name_locator)
        return int(count)

    @property
    def addon_updated_dates(self):
        count = self.addon_count
        return self._extract_iso_dates(self._addons_metadata_locator, "Updated %B %d, %Y", count)

    @property
    def addon_created_dates(self):
        count = self.addon_count
        return self._extract_iso_dates(self._addons_metadata_locator, "Added %B %d, %Y", count)

    @property
    def addon_download_number(self):
        pattern = "(\d+(?:[,]\d+)*) weekly downloads"
        downloads_locator = self._addons_metadata_locator
        downloads = self._extract_integers(downloads_locator, pattern, self.addon_count)
        return downloads

    @property
    def addon_rating(self):
        pattern = "(\d)"
        ratings_locator = self._addons_rating_locator
        ratings = self._extract_integers(ratings_locator, pattern, self.addon_count)
        return ratings

    @property
    def top_counter(self):
        return self.selenium.get_text(self._top_counter_locator)

    @property
    def bottom_counter(self):
        return self.selenium.get_text(self._bottom_counter_locator)


class AddonsThemePage(AddonsBasePage):

    _addon_title = "css=h2.addon > span"

    @property
    def addon_title(self):
        return self.selenium.get_text(self._addon_title)


class AddonsThemesCategoryPage(AddonsBasePage):

    _title_locator = "css=h2"
    _breadcrumb_locator = "css=ol.breadcrumbs"

    @property
    def title(self):
        return self.selenium.get_text(self._title_locator)

    @property
    def breadcrumb(self):
        return self.selenium.get_text(self._breadcrumb_locator)


class AddonsPersonasPage(AddonsHomePage):

    _page_title = "Personas :: Add-ons for Firefox"
    _personas_locator = "//div[@class='persona persona-small']"
    _start_exploring_locator = "css=#featured-addons.personas-home a.more-info"
    _featured_addons_locator = "css=#featured-addons.personas-home"
    _featured_personas_locator = "css=.personas-featured .persona.persona-small"
    _addons_column_locator = '//div[@class="addons-column"]'

    def __init__(self, testsetup):
        AddonsBasePage.__init__(self, testsetup)

    @property
    def persona_count(self):
        """ Returns the total number of persona links in the page. """
        return self.selenium.get_xpath_count(self._personas_locator)

    def click_persona(self, index):
        """ Clicks on the persona with the given index in the page. """
        self.selenium.click("xpath=(%s)[%d]//a" % (self._personas_locator, index))
        self.selenium.wait_for_page_to_load(self.timeout)
        return AddonsPersonasDetailPage(self.testsetup)

    def open_persona_detail_page(self, persona_key):
        self.selenium.open("%s/addon/%s" % (self.site_version, persona_key))
        self.selenium.wait_for_page_to_load(self.timeout)
        return AddonsPersonasDetailPage(self.testsetup)

    @property
    def is_featured_addons_present(self):
        return self.selenium.get_css_count(self._featured_addons_locator) > 0

    def click_start_exploring(self):
        self.selenium.click(self._start_exploring_locator)
        self.selenium.wait_for_page_to_load(self.timeout)
        return AddonsPersonasBrowsePage(self.testsetup)

    @property
    def featured_personas_count(self):
        return self.selenium.get_css_count(self._featured_personas_locator)

    def _persona_in_column_locator(self, column_index):
        """ Returns a locator for personas in the column with the given index. """
        return "%s[%d]%s" % (self._addons_column_locator, column_index, self._personas_locator)

    @property
    def recently_added_count(self):
        locator = self._persona_in_column_locator(1)
        return self.selenium.get_xpath_count(locator)

    @property
    def recently_added_dates(self):
        locator = self._persona_in_column_locator(1)
        iso_dates = self._extract_iso_dates(locator, "Added %B %d, %Y", self.recently_added_count)
        return iso_dates

    @property
    def most_popular_count(self):
        locator = self._persona_in_column_locator(2)
        return self.selenium.get_xpath_count(locator)

    @property
    def most_popular_downloads(self):
        locator = self._persona_in_column_locator(2)
        pattern = "(\d+(?:[,]\d+)*)\s+users"
        return self._extract_integers(locator, pattern, self.most_popular_count)

    @property
    def top_rated_count(self):
        locator = self._persona_in_column_locator(3)
        return self.selenium.get_xpath_count(locator)

    @property
    def top_rated_ratings(self):
        locator = self._persona_in_column_locator(3)
        pattern = "Rated\s+(\d)\s+.*"
        return self._extract_integers(locator, pattern, self.top_rated_count)


class AddonsPersonasDetailPage(AddonsBasePage):

    _page_title_regex = '.+ :: Add-ons for Firefox'
    _personas_title_locator = 'css=h2.addon'
    _breadcrumb_locator = '//ol[@class="breadcrumbs"]'
    _breadcrumb_item_index_locator = '/li[%s]//'
    _breadcrumb_item_text_locator = '/li//*[text()="%s"]'

    def __init__(self, testsetup):
        AddonsBasePage.__init__(self, testsetup)

    @property
    def is_the_current_page(self):
        # This overrides the method in the Page super class.
        if not (re.match(self._page_title_regex, self.selenium.get_title())):
            self.record_error()
            raise Exception('Expected the current page to be the personas detail page.')
        return True

    @property
    def personas_title(self):
        """ Returns the title of the currently displayed persona. """
        return self.selenium.get_text(self._personas_title_locator)

    def get_breadcrumb_item_locator(self, item):
        """ Returns an xpath locator for the given item.
            If item is an int, the item with the given index (1..N) will be located.
            If item is a str, the item with the given link text will be located.
        """
        if isinstance(item, int):
            return (self._breadcrumb_locator + self._breadcrumb_item_index_locator) % str(item)
        elif isinstance(item, str):
            return (self._breadcrumb_locator + self._breadcrumb_item_text_locator) % str(item)

    def get_breadcrumb_item_text(self, item):
        """ Returns the label of the given item in the breadcrumb menu. """
        locator = self.get_breadcrumb_item_locator(item) + 'text()'
        return self.selenium.get_text(locator)

    def get_breadcrumb_item_href(self, item):
        """ Returns the value of the href attribute for the given item in the breadcrumb menu. """
        locator = self.get_breadcrumb_item_locator(item) + '@href'
        return self.selenium.get_attribute(locator)

    def click_breadcrumb_item(self, item):
        """ Clicks on the given item in the breadcrumb menu. """
        locator = self.get_breadcrumb_item_locator(item)
        self.selenium.click(locator)
        self.selenium.wait_for_page_to_load(self.timeout)


class AddonsPersonasBrowsePage(AddonsBasePage):
    """
    The personas browse page allows browsing the personas according to
    some sort criteria (eg. top rated or most downloaded).

    """

    _selected_sort_by_locator = "css=#addon-list-options li.selected a"
    _personas_grid_locator = "css=.featured.listing ul.personas-grid"

    def __init__(self, testsetup):
        AddonsBasePage.__init__(self, testsetup)

    @property
    def sort_key(self):
        """ Returns the current value of the sort request parameter. """
        url = self.get_url_current_page()
        return re.search("[/][?]sort=(.+)[&]?", url).group(1)

    @property
    def sort_by(self):
        """ Returns the label of the currently selected sort option. """
        return self.selenium.get_text(self._selected_sort_by_locator)

    @property
    def is_the_current_page(self):
        # This overrides the method in the Page super class.
        if not (self.is_element_present(self._personas_grid_locator)):
            self.record_error()
            raise Exception('Expected the current page to be the personas browse page.')
        return True


class DiscoveryPane(AddonsBasePage):

    _what_are_addons_section_locator = 'id=intro'
    _what_are_addons_text_locator = 'css=#intro p'
    _mission_section_locator = 'id=mission'
    _mission_section_text_locator = 'css=#mission > p'
    _learn_more_locator = 'id=learn-more'
    _mozilla_org_link_locator = "css=#mission a"
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
        AddonsBasePage.__init__(self, testsetup)
        self.selenium.open("%s/%s" % (self.site_version, path))
        #resizing this page for elements that disappear when the window is < 1000
        self.selenium.get_eval("window.resizeTo(10000,10000); window.moveTo(0,0)")

    @property
    def what_are_addons_text(self):
        return self.selenium.get_text(self._what_are_addons_text_locator)

    def click_learn_more(self):
        self.selenium.click(self._learn_more_locator)
        self.selenium.wait_for_page_to_load(self.timeout)

    def is_mission_section_visible(self):
        return self.selenium.is_visible(self._mission_section_locator)

    def wait_for_mission_visible(self):
            self.wait_for_element_visible(self._mission_section_locator)

    @property
    def mission_section(self):
        return self.selenium.get_text(self._mission_section_text_locator)

    def mozilla_org_link_visible(self):
        return self.selenium.is_visible(self._mozilla_org_link_locator)

    @property
    def download_count(self):
        self.wait_for_element_visible(self._download_count_text_locator)
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
        return DiscoveryPersonasDetailPage(self.testsetup)

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


class DiscoveryPersonasDetailPage(AddonsBasePage):

    _persona_title = 'css=h1.addon'

    @property
    def persona_title(self):
        return self.selenium.get_text(self._persona_title)


class UserFAQPage(AddonsBasePage):

    _license_question_locator = "css=#license"
    _license_answer_locator = "css=#license + dd"

    @property
    def license_question(self):
        return self.selenium.get_text(self._license_question_locator)

    @property
    def license_answer(self):
        return self.selenium.get_text(self._license_answer_locator)

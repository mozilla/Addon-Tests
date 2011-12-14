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

import re

from urllib2 import urlparse
from selenium.webdriver.common.by import By

from pages.page import Page
from pages.base import Base


class Details(Base):

    _breadcrumb_locator = (By.ID, "breadcrumbs")

    #addon informations
    _title_locator = (By.CSS_SELECTOR, "#addon > hgroup > h1.addon")
    _version_number_locator = (By.CSS_SELECTOR, "span.version-number")
    _authors_locator = (By.XPATH, "//h4[@class='author']/a")
    _summary_locator = (By.ID, "addon-summary")
    _install_button_locator = (By.CSS_SELECTOR, "p[class='install-button'] > a")
    _rating_locator = (By.CSS_SELECTOR, "span[itemprop='rating']")
    _license_link_locator = (By.CSS_SELECTOR, ".source-license > a")
    _whats_this_license_locator = (By.CSS_SELECTOR, ".license-faq")
    _view_the_source_locator = (By.CSS_SELECTOR, ".source-code")
    _complete_version_history_locator = (By.CSS_SELECTOR, "p.more > a")
    _description_locator = (By.CSS_SELECTOR, "div.prose")
    _register_link_locator = (By.CSS_SELECTOR, "li.account > a")
    _login_link_locator = (By.CSS_SELECTOR, "li.account > a:nth-child(2)")
    _other_applications_locator = (By.ID, "other-apps")

    _about_addon_locator = (By.CSS_SELECTOR, "section.primary > h2")
    _version_information_locator = (By.CSS_SELECTOR, "#detail-relnotes")
    _version_information_heading_locator = (By.CSS_SELECTOR, "#detail-relnotes > h2")
    _version_information_heading_link_locator = (By.CSS_SELECTOR, "#detail-relnotes > h2 > a")
    _release_version_locator = (By.CSS_SELECTOR, "div.info > h3 > a")
    _source_code_license_information_locator = (By.CSS_SELECTOR, ".source > li > a")
    _reviews_title_locator = (By.CSS_SELECTOR, "#reviews > h2")
    _tags_locator = (By.ID, "tagbox")
    _other_addons_header_locator = (By.CSS_SELECTOR, "h2.compact-bottom")
    _other_addons_list_locator = (By.CSS_SELECTOR, ".primary .listing-grid")
    _part_of_collections_header_locator = (By.CSS_SELECTOR, "#collections-grid h2")
    _part_of_collections_list_locator = (By.CSS_SELECTOR, "#collections-grid section li")
    _icon_locator = (By.CSS_SELECTOR, "img.icon")
    _support_link_locator = (By.CSS_SELECTOR, "a.support")
    _review_details_locator = (By.CSS_SELECTOR, ".review .description")
    _all_reviews_link_locator = (By.CSS_SELECTOR, "a.more-info")
    _review_locator = (By.CSS_SELECTOR, "div.review:not(.reply)")
    _info_link_locator = (By.CSS_SELECTOR, "li > a.scrollto")
    _rating_counter_locator = (By.CSS_SELECTOR, ".grouped_ratings .num_ratings")

    _devs_comments_section_locator = (By.CSS_SELECTOR, "#developer-comments")
    _devs_comments_title_locator = (By.CSS_SELECTOR, "#developer-comments h2")
    _devs_comments_toggle_locator = (By.CSS_SELECTOR, "#developer-comments h2 a")
    _devs_comments_message_locator = (By.CSS_SELECTOR, "#developer-comments div.content")

    #more about this addon
    _website_locator = (By.CSS_SELECTOR, ".links a.home")
    #other_addons
    _other_addons_by_author_locator = (By.CSS_SELECTOR, "#author-addons > ul.listing-grid > section li")
    _other_addons_by_author_text_locator = (By.CSS_SELECTOR, '#author-addons > h2')
    _reviews_locator = (By.CSS_SELECTOR, "section#reviews div")
    _add_review_link_locator = (By.ID, "add-review")

    _add_to_collection_locator = (By.CSS_SELECTOR, ".collection-add.widget.collection")
    _add_to_collection_widget_button_locator = (By.CSS_SELECTOR, ".collection-add-login .register-button .button")
    _add_to_collection_widget_login_link_locator = (By.CSS_SELECTOR, "div.collection-add-login p:nth-child(3) > a")

    _development_channel_locator = (By.CSS_SELECTOR, "#beta-channel")
    _development_channel_toggle = (By.CSS_SELECTOR, '#beta-channel a.toggle')
    _development_channel_install_button_locator = (By.CSS_SELECTOR, '#beta-channel p.install-button a.button')
    _development_channel_title_locator = (By.CSS_SELECTOR, "#beta-channel h2")
    _development_channel_content_locator = (By.CSS_SELECTOR, "#beta-channel > div.content")
    _development_version_locator = (By.CSS_SELECTOR, '.beta-version')

    _next_link_locator = (By.CSS_SELECTOR, ".paginator .rel > a:nth-child(3)")
    _previous_link_locator = (By.CSS_SELECTOR, ".paginator .rel > a:nth-child(2)")
    _last_page_link_locator = (By.CSS_SELECTOR, ".paginator .rel > a:nth-child(4)")
    _first_page_link_locator = (By.CSS_SELECTOR, ".paginator .rel > a:nth-child(1)")

    def __init__(self, testsetup, addon_name=None):
        #formats name for url
        Base.__init__(self, testsetup)
        if (addon_name != None):
            self.addon_name = addon_name.replace(" ", "-")
            self.addon_name = re.sub(r'[^A-Za-z0-9\-]', '', self.addon_name).lower()
            self.addon_name = self.addon_name[:27]
            self.selenium.get("%s/addon/%s" % (self.base_url, self.addon_name))

    @property
    def _page_title(self):
        return "%s :: Add-ons for Firefox" % self.title

    @property
    def title(self):
        base = self.selenium.find_element(*self._title_locator).text
        '''base = "firebug 1.8.9" we will have to remove version number for it'''
        return base.replace(self.version_number, '').strip()

    @property
    def has_reviews(self):
        return self.review_count > 0

    def click_all_reviews_link(self):
        self.selenium.find_element(*self._all_reviews_link_locator).click()

    @property
    def review_count(self):
        return len(self.selenium.find_elements(*self._review_locator))

    @property
    def breadcrumb(self):
        return self.selenium.find_element(*self._breadcrumb_locator).text

    @property
    def version_number(self):
        return self.selenium.find_element(*self._version_number_locator).text

    @property
    def source_code_license_information(self):
        return self.selenium.find_element(*self._source_code_license_information_locator).text

    @property
    def authors(self):
        return [element.text for element in self.selenium.find_elements(*self._authors_locator)]

    @property
    def summary(self):
        return self.selenium.find_element(*self._summary_locator).text

    @property
    def rating(self):
        return self.selenium.find_element(*self._rating_locator).text

    def click_whats_this_license(self):
        self.selenium.find_element(*self._whats_this_license_locator).click()
        from pages.addons_site import UserFAQ
        return UserFAQ(self.testsetup)

    @property
    def license_site(self):
        return self.selenium.find_element(*self._license_link_locator).get_attribute('href')

    @property
    def license_link_text(self):
        return self.selenium.find_element(*self._license_link_locator).text

    @property
    def description(self):
        return self.selenium.find_element(*self._description_locator).text

    @property
    def register_link(self):
        return self.selenium.find_element(*self._register_link_locator).text

    @property
    def login_link(self):
        return self.selenium.find_element(*self._login_link_locator).text

    @property
    def other_apps(self):
        return self.selenium.find_element(*self._other_applications_locator).text

    @property
    def version_information_heading(self):
        return self.selenium.find_element(*self._version_information_heading_locator).text

    @property
    def version_information_href(self):
        return self.selenium.find_element(*self._version_information_heading_link_locator).get_attribute('href')

    @property
    def release_version(self):
        return self.selenium.find_element(*self._release_version_locator).text

    @property
    def about_addon(self):
        return self.selenium.find_element(*self._about_addon_locator).text

    @property
    def review_title(self):
        return self.selenium.find_element(*self._reviews_title_locator).text

    @property
    def review_details(self):
        return self.selenium.find_element(*self._review_details_locator).text

    @property
    def often_used_with_header(self):
        return self.selenium.find_element(*self._other_addons_header_locator).text

    @property
    def devs_comments_title(self):
        return self.selenium.find_element(*self._devs_comments_title_locator).text

    @property
    def devs_comments_message(self):
        return self.selenium.find_element(*self._devs_comments_message_locator).text

    def click_version_information_heading(self):
        return self.selenium.find_element(*self._version_information_heading_link_locator).click()

    @property
    def is_version_information_section_expanded(self):
        expand_info = self.selenium.find_element(*self._version_information_locator).get_attribute("class")
        return ("expanded" in expand_info)

    @property
    def is_version_information_install_button_visible(self):
        return self.is_element_visible(*self._install_button_locator)

    @property
    def is_whats_this_license_visible(self):
        return self.is_element_visible(*self._whats_this_license_locator)

    @property
    def is_source_code_license_information_visible(self):
        return self.is_element_visible(*self._source_code_license_information_locator)

    @property
    def is_view_the_source_link_visible(self):
        return self.is_element_visible(*self._view_the_source_locator)

    @property
    def is_complete_version_history_visible(self):
        return self.is_element_visible(*self._complete_version_history_locator)

    @property
    def is_version_information_section_in_view(self):
        """ Check if the information section is in view.

        The script returns the pixels the current document has been scrolled from the
        upper left corner of the window, vertically.
        If the offset is > 1000, the page has scrolled to the information section and it
        is in view.

        """
        return (self.selenium.execute_script('return window.pageYOffset')) > 1000

    @property
    def is_often_used_with_list_visible(self):
        return self.is_element_visible(*self._other_addons_list_locator)

    @property
    def are_tags_visible(self):
        return self.is_element_visible(*self._tags_locator)

    def is_devs_comments_section_expanded(self):
        is_expanded = self.selenium.find_element(*self._devs_comments_section_locator).get_attribute("class")
        return ("expanded" in is_expanded)

    @property
    def part_of_collections_header(self):
        return self.selenium.find_element(*self._part_of_collections_header_locator).text

    @property
    def part_of_collections(self):
        return [self.PartOfCollectionsSnippet(self.testsetup, element)
                for element in self.selenium.find_elements(*self._part_of_collections_list_locator)]

    def page_forward(self):
        self.selenium.find_element(*self._next_link_locator).click()

    def page_back(self):
        self.selenium.find_element(*self._previous_link_locator).click()

    def go_to_last_page(self):
        self.selenium.find_element(*self._last_page_link_locator).click()

    def go_to_first_page(self):
        self.selenium.find_element(*self._first_page_link_locator).click()

    @property
    def is_prev_link_enabled(self):
        button = self.selenium.find_element(*self._previous_link_locator).get_attribute('class')
        return not ("disabled" in button)

    @property
    def is_prev_link_visible(self):
        return self.is_element_visible(*self._previous_link_locator)

    @property
    def is_next_link_enabled(self):
        button = self.selenium.find_element(*self._next_link_locator).get_attribute('class')
        return not("disabled" in button)

    @property
    def is_next_link_visible(self):
        return self.is_element_visible(*self._next_link_locator)

    class PartOfCollectionsSnippet(Page):

        _name_locator = (By.CSS_SELECTOR, ' div.summary > h3')

        def __init__(self, testsetup, element):
            Page.__init__(self, testsetup)
            self._root_element = element

        def click_collection(self):
            self._root_element.find_element(*self._name_locator).click()
            from pages.collection import Collections
            return Collections(self.testsetup)

        @property
        def name(self):
            return self._root_element.find_element(*self._name_locator).text

    def click_other_apps(self):
        self.selenium.find_element(*self._other_applications_locator).click()

    @property
    def icon_url(self):
        return self.selenium.find_element(*self._icon_locator).get_attribute('src')

    @property
    def website(self):
        return self.selenium.find_element(*self._website_locator).get_attribute('href')

    def click_website_link(self):
        self.selenium.find_element(*self._website_locator).click()

    @property
    def support_url(self):
        support_url = self.selenium.find_element(*self._support_link_locator).get_attribute('href')
        match = re.findall("http", support_url)
        #staging url
        if len(match) > 1:
            return self._extract_url_from_link(support_url)
        #production url
        else:
            return support_url

    def _extract_url_from_link(self, url):
        #parses out extra certificate stuff from urls in staging only
        return urlparse.unquote(re.search('\w+://.*/(\w+%3A//.*)', url).group(1))

    @property
    def other_addons_by_authors_text(self):
        return self.selenium.find_element(*self._other_addons_by_author_text_locator).text

    @property
    def other_addons(self):
        return [self.OtherAddons(self.testsetup, element)
                for element in self.selenium.find_elements(*self._other_addons_by_author_locator)]

    def get_rating_counter(self, rating):
        elements = self.selenium.find_elements(*self._rating_counter_locator)
        try:
            return int(elements[5 - rating].text)
        except IndexError:
            return 0

    @property
    def previewer(self):
        return self.ImagePreviewer(self.testsetup)

    def click_add_to_collection_widget(self):
        self.selenium.find_element(*self._add_to_collection_locator).click()

    @property
    def collection_widget_button(self):
        return self.selenium.find_element(*self._add_to_collection_widget_button_locator).text

    @property
    def collection_widget_login_link(self):
        return self.selenium.find_element(*self._add_to_collection_widget_login_link_locator).text

    class ImagePreviewer(Page):

        #navigation
        _next_locator = (By.CSS_SELECTOR, 'section.previews.carousel > a.next')
        _prev_locator = (By.CSS_SELECTOR, 'section.previews.carousel > a.prev')

        _image_locator = (By.CSS_SELECTOR, '#preview li')
        _link_locator = (By.TAG_NAME, 'a')

        def next_set(self):
            self.selenium.find_element(*self._next_locator).click()

        def prev_set(self):
            self.selenium.find_element(*self._prev_locator).click()

        def click_image(self, image_no=0):
            images = self.selenium.find_elements(*self._image_locator)
            images[image_no].find_element(*self._link_locator).click()
            from pages.regions.image_viewer import ImageViewer
            image_viewer = ImageViewer(self.testsetup)
            image_viewer.wait_for_image_viewer_to_finish_animating()
            return image_viewer

        def image_title(self, image_no):
            return self.selenium.find_element(self._image_locator[0],
                        '%s:nth-child(%s) a' % (self._image_locator[1], image_no + 1)).get_attribute('title')

        def image_link(self, image_no):
            return self.selenium.find_element(self._image_locator[0],
                        '%s:nth-child(%s) a img' % (self._image_locator[1], image_no + 1)).get_attribute('src')

        @property
        def image_count(self):
            return len(self.selenium.find_elements(*self._image_locator))

        @property
        def image_set_count(self):
            if self.image_count % 3 == 0:
                return self.image_count / 3
            else:
                return self.image_count / 3 + 1

    def review(self, element):
        return self.DetailsReviewSnippet(self.testsetup, element)

    @property
    def reviews(self):
        return [self.DetailsReviewSnippet(self.testsetup, element)
                for element in self.selenium.find_elements(*self._reviews_locator)]

    @property
    def version_info_link(self):
        return self.selenium.find_element(*self._info_link_locator).get_attribute('href')

    def click_version_info_link(self):
        self.selenium.find_element(*self._info_link_locator).click()

    def click_version_information_header(self):
        self.selenium.find_element(*self._version_information_heading_link_locator).click()

    def click_devs_comments(self):
        self.selenium.find_element(*self._devs_comments_toggle_locator).click()

    class OtherAddons(Page):

        _name_locator = (By.CSS_SELECTOR, 'div.summary h3')

        def __init__(self, testsetup, element):
            Page.__init__(self, testsetup)
            self._root_element = element

        @property
        def name(self):
            return self._root_element.find_element(*self._name_locator).text

        def click_addon_link(self):
            self._root_element.find_element(*self._name_locator).click()
            #return Details(self.testsetup)

    class DetailsReviewSnippet(Page):

        _reviews_locator = (By.CSS_SELECTOR, '#reviews div')  # Base locator
        _username_locator = (By.CSS_SELECTOR, 'p.byline a')

        def __init__(self, testsetup, element):
            Page.__init__(self, testsetup)
            self._root_element = element

        @property
        def username(self):
            return self._root_element.find_element(*self._username_locator).text

        def click_username(self):
            self._root_element.find_element(*self._username_locator).click()
            from pages.user import User
            return User(self.testsetup)

    def click_to_write_review(self):
        self.selenium.find_element(*self._add_review_link_locator).click()
        from pages.addons_site import WriteReviewBlock
        return WriteReviewBlock(self.testsetup)

    @property
    def development_channel_text(self):
        return self.selenium.find_element(*self._development_channel_title_locator).text

    def click_development_channel(self):
        self.selenium.find_element(*self._development_channel_toggle).click()

    @property
    def is_development_channel_expanded(self):
        is_expanded = self.selenium.find_element(*self._development_channel_locator).get_attribute('class')
        return "expanded" in is_expanded

    @property
    def is_development_channel_install_button_visible(self):
        return self.is_element_visible(*self._development_channel_install_button_locator)

    @property
    def development_channel_content(self):
        return self.selenium.find_element(*self._development_channel_content_locator).text

    @property
    def beta_version(self):
        return self.selenium.find_element(*self._development_version_locator).text

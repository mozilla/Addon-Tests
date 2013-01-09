#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re
import time

from urllib2 import urlparse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

from pages.page import Page
from pages.desktop.base import Base


class Details(Base):

    _breadcrumb_locator = (By.ID, "breadcrumbs")

    #addon informations
    _title_locator = (By.CSS_SELECTOR, "#addon > hgroup > h1.addon")
    _version_number_locator = (By.CSS_SELECTOR, "span.version-number")
    _no_restart_locator = (By.CSS_SELECTOR, "span.no-restart")
    _authors_locator = (By.XPATH, "//h4[@class='author']/a")
    _summary_locator = (By.ID, "addon-summary")
    _install_button_locator = (By.CSS_SELECTOR, '.button.prominent.add.installer')
    _install_button_attribute_locator = (By.CSS_SELECTOR, '.install-wrapper .install-shell .install.clickHijack')
    _rating_locator = (By.CSS_SELECTOR, "span.stars.large")
    _license_link_locator = (By.CSS_SELECTOR, ".source-license > a")
    _whats_this_license_locator = (By.CSS_SELECTOR, "a.license-faq")
    _view_the_source_locator = (By.CSS_SELECTOR, "a.source-code")
    _complete_version_history_locator = (By.CSS_SELECTOR, "p.more > a")
    _description_locator = (By.CSS_SELECTOR, "div.prose")
    _other_applications_locator = (By.ID, "other-apps")
    _compatibility_locator = (By.CSS_SELECTOR, '.meta.compat')
    _review_link_locator = (By.ID, 'reviews-link')
    _daily_users_link_locator = (By.CSS_SELECTOR, '#daily-users > a.stats')

    _about_addon_locator = (By.CSS_SELECTOR, "section.primary > h2")
    _version_information_locator = (By.ID, "detail-relnotes")
    _version_information_heading_locator = (By.CSS_SELECTOR, "#detail-relnotes > h2")
    _version_information_heading_link_locator = (By.CSS_SELECTOR, "#detail-relnotes > h2 > a")
    _version_information_button_locator = (By.CSS_SELECTOR, "#detail-relnotes > h2 > a > b")
    _version_information_content_locator = (By.CSS_SELECTOR, "#detail-relnotes > div.content")
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
    _all_reviews_link_locator = (By.CSS_SELECTOR, "#reviews a.more-info")
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
    _other_addons_by_author_locator = (By.CSS_SELECTOR, "#author-addons > ul.listing-grid > section li > div.addon")
    _other_addons_by_author_text_locator = (By.CSS_SELECTOR, '#author-addons > h2')
    _reviews_section_header_locator = (By.CSS_SELECTOR, '#reviews > h2')
    _reviews_locator = (By.CSS_SELECTOR, "section#reviews div")
    _add_review_link_locator = (By.ID, "add-review")

    _add_to_collection_locator = (By.CSS_SELECTOR, ".collection-add.widget.collection")
    _add_to_collection_widget_button_locator = (By.CSS_SELECTOR, ".collection-add-login .register-button .button")
    _add_to_collection_widget_login_link_locator = (By.CSS_SELECTOR, "div.collection-add-login p:nth-child(3) > a")
    _add_to_favorites_widget_locator = (By.CSS_SELECTOR, 'div.widgets > a.favorite')

    _development_channel_locator = (By.CSS_SELECTOR, "#beta-channel")
    _development_channel_toggle = (By.CSS_SELECTOR, '#beta-channel a.toggle')
    _development_channel_install_button_locator = (By.CSS_SELECTOR, '#beta-channel p.install-button a.button.caution')
    _development_channel_title_locator = (By.CSS_SELECTOR, "#beta-channel h2")
    _development_channel_content_locator = (By.CSS_SELECTOR, "#beta-channel > div.content")
    _development_version_locator = (By.CSS_SELECTOR, '.beta-version')

    _add_to_favorites_updating_locator = (By.CSS_SELECTOR, "a.ajax-loading")

    # contribute to addon
    _contribute_button_locator = (By.ID, 'contribute-button')
    _paypal_login_dialog_locator = (By.CSS_SELECTOR, '#page .content')

    def __init__(self, testsetup, addon_name=None):
        #formats name for url
        Base.__init__(self, testsetup)
        if (addon_name is not None):
            self.addon_name = addon_name.replace(" ", "-")
            self.addon_name = re.sub(r'[^A-Za-z0-9\-]', '', self.addon_name).lower()
            self.addon_name = self.addon_name[:27]
            self.selenium.get("%s/addon/%s" % (self.base_url, self.addon_name))
        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: self.is_element_visible(*self._title_locator))

    @property
    def _page_title(self):
        return "%s :: Add-ons for Firefox" % self.title

    @property
    def title(self):
        base = self.selenium.find_element(*self._title_locator).text
        '''base = "firebug 1.8.9" we will have to remove version number for it'''
        return base.replace(self.version_number, '').replace(self.no_restart, '').strip()

    @property
    def no_restart(self):
        if self.is_element_present(*self._no_restart_locator):
            return self.selenium.find_element(*self._no_restart_locator).text
        else:
            return ""

    @property
    def has_reviews(self):
        return self.review_count > 0

    def click_all_reviews_link(self):
        self.selenium.find_element(*self._all_reviews_link_locator).click()

        from pages.desktop.addons_site import ViewReviews
        return ViewReviews(self.testsetup)

    @property
    def review_count(self):
        return len(self.selenium.find_elements(*self._review_locator))

    @property
    def total_reviews_count(self):
        text = self.selenium.find_element(*self._review_link_locator).text
        return int(text.split()[0].replace(',', ''))

    def click_view_statistics(self):
        self.selenium.find_element(*self._daily_users_link_locator).click()
        from pages.desktop.statistics import Statistics
        stats_page = Statistics(self.testsetup)
        WebDriverWait(self.selenium, self.timeout).until(lambda s: stats_page.is_chart_loaded)
        return stats_page

    @property
    def daily_users_number(self):
        text = self.selenium.find_element(*self._daily_users_link_locator).text
        return int(text.split()[0].replace(',', ''))

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
        return re.findall("\d", self.selenium.find_element(*self._rating_locator).text)[0]

    def click_whats_this_license(self):
        self.selenium.find_element(*self._whats_this_license_locator).click()
        from pages.desktop.addons_site import UserFAQ
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
        return [review.text for review in self.selenium.find_elements(*self._review_details_locator)]

    @property
    def often_used_with_header(self):
        return self.selenium.find_element(*self._other_addons_header_locator).text

    @property
    def devs_comments_title(self):
        return self.selenium.find_element(*self._devs_comments_title_locator).text

    @property
    def devs_comments_message(self):
        return self.selenium.find_element(*self._devs_comments_message_locator).text

    @property
    def compatible_applications(self):
        return self.selenium.find_element(*self._compatibility_locator).text

    @property
    def is_version_information_install_button_visible(self):
        return self.is_element_visible(*self._install_button_locator)

    def click_and_hold_install_button_returns_class_value(self):
        click_element = self.selenium.find_element(*self._install_button_locator)
        ActionChains(self.selenium).\
            click_and_hold(click_element).\
            perform()
        return self.selenium.find_element(*self._install_button_attribute_locator).get_attribute("class")

    @property
    def is_whats_this_license_visible(self):
        return self.is_element_visible(*self._whats_this_license_locator)

    @property
    def license_faq_text(self):
        return self.selenium.find_element(*self._whats_this_license_locator).text

    @property
    def is_source_code_license_information_visible(self):
        return self.is_element_visible(*self._source_code_license_information_locator)

    @property
    def is_view_the_source_link_visible(self):
        return self.is_element_visible(*self._view_the_source_locator)

    def click_view_source_code(self):
        self.selenium.find_element(*self._view_the_source_locator).click()
        from pages.desktop.addons_site import ViewAddonSource
        addon_source = ViewAddonSource(self.testsetup)
        WebDriverWait(self.selenium, self.timeout).until(lambda s: addon_source.is_file_viewer_visible)
        return addon_source

    @property
    def view_source_code_text(self):
        return self.selenium.find_element(*self._view_the_source_locator).text

    @property
    def is_complete_version_history_visible(self):
        return self.is_element_visible(*self._complete_version_history_locator)

    @property
    def is_often_used_with_list_visible(self):
        return self.is_element_visible(*self._other_addons_list_locator)

    @property
    def are_tags_visible(self):
        return self.is_element_visible(*self._tags_locator)

    @property
    def is_devs_comments_section_present(self):
        return self.is_element_present(*self._devs_comments_section_locator)

    @property
    def is_devs_comments_section_expanded(self):
        return self.is_element_visible(*self._devs_comments_message_locator)

    @property
    def part_of_collections_header(self):
        return self.selenium.find_element(*self._part_of_collections_header_locator).text

    @property
    def part_of_collections(self):
        return [self.PartOfCollectionsSnippet(self.testsetup, web_element)
                for web_element in self.selenium.find_elements(*self._part_of_collections_list_locator)]

    @property
    def is_reviews_section_in_view(self):
        return self.selenium.execute_script('return window.pageYOffset') > 1000

    @property
    def is_reviews_section_visible(self):
        return self.is_element_visible(*self._reviews_section_header_locator)

    class PartOfCollectionsSnippet(Page):

        _name_locator = (By.CSS_SELECTOR, ' div.summary > h3')

        def __init__(self, testsetup, element):
            Page.__init__(self, testsetup)
            self._root_element = element

        def click_collection(self):
            self._root_element.find_element(*self._name_locator).click()
            from pages.desktop.collections import Collections
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
        url = self.selenium.find_element(*self._website_locator).get_attribute('href')
        return self._extract_url_from_link(url)

    def click_website_link(self):
        self.selenium.find_element(*self._website_locator).click()
        WebDriverWait(self.selenium, self.timeout).until(lambda s: self.selenium.title)

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
        return [self.OtherAddons(self.testsetup, other_addon_web_element)
                for other_addon_web_element in self.selenium.find_elements(*self._other_addons_by_author_locator)]

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

            from pages.desktop.regions.image_viewer import ImageViewer
            image_viewer = ImageViewer(self.testsetup)
            WebDriverWait(self.selenium, self.timeout).until(lambda s: image_viewer.is_visible)
            return image_viewer

        def image_title(self, image_no):
            return self.selenium.find_element(
                self._image_locator[0],
                '%s:nth-child(%s) a' % (self._image_locator[1], image_no + 1)
            ).get_attribute('title')

        def image_link(self, image_no):
            return self.selenium.find_element(
                self._image_locator[0],
                '%s:nth-child(%s) a img' % (self._image_locator[1], image_no + 1)
            ).get_attribute('src')

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
        return [self.DetailsReviewSnippet(self.testsetup, web_element)
                for web_element in self.selenium.find_elements(*self._reviews_locator)]

    @property
    def version_info_link(self):
        return self.selenium.find_element(*self._info_link_locator).get_attribute('href')

    def click_version_info_link(self):
        self.selenium.find_element(*self._info_link_locator).click()

    def click_user_reviews_link(self):
        self.selenium.find_element(*self._review_link_locator).click()
        WebDriverWait(self.selenium, self.timeout).until(lambda s: (self.selenium.execute_script('return window.pageYOffset')) > 1000)

    def expand_version_information(self):
        self.selenium.find_element(*self._version_information_button_locator).click()
        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: self.is_version_information_section_expanded)

    @property
    def is_version_information_section_expanded(self):
        return self.is_element_visible(*self._version_information_content_locator)

    def expand_devs_comments(self):
        self.selenium.find_element(*self._devs_comments_toggle_locator).click()
        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: self.is_devs_comments_section_expanded)

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
            from pages.desktop.user import User
            return User(self.testsetup)

    def click_to_write_review(self):
        self.selenium.find_element(*self._add_review_link_locator).click()
        from pages.desktop.addons_site import WriteReviewBlock
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

    class ContributionSnippet(Page):

        _make_contribution_button_locator = (By.ID, 'contribute-confirm')

        def __init__(self, testsetup):
            Page.__init__(self, testsetup)

            WebDriverWait(self.selenium, self.timeout).until(
                lambda s: s.find_element(*self._make_contribution_button_locator),
                "Timeout waiting for 'make contribution' button.")

        def click_make_contribution_button(self):
            self.selenium.find_element(*self._make_contribution_button_locator).click()
            from pages.desktop.regions.paypal_frame import PayPalFrame
            return PayPalFrame(self.testsetup)

        @property
        def is_make_contribution_button_visible(self):
            return self.is_element_visible(*self._make_contribution_button_locator)

        @property
        def make_contribution_button_name(self):
            return self.selenium.find_element(*self._make_contribution_button_locator).text

    def click_contribute_button(self):
        self.selenium.find_element(*self._contribute_button_locator).click()
        return self.ContributionSnippet(self.testsetup)

    @property
    def is_paypal_login_dialog_visible(self):
        return self.is_element_visible(*self._paypal_login_dialog_locator)

    def _wait_for_favorite_addon_to_be_added(self):
        WebDriverWait(self.selenium, self.timeout).until(lambda s: not self.is_element_present(*self._add_to_favorites_updating_locator))

    def click_add_to_favorites(self):
        self.selenium.find_element(*self._add_to_favorites_widget_locator).click()
        self._wait_for_favorite_addon_to_be_added()

    @property
    def is_addon_marked_as_favorite(self):
        is_favorite = self.selenium.find_element(*self._add_to_favorites_widget_locator).text
        return 'Remove from favorites' in is_favorite

    @property
    def total_review_count(self):
        return self.selenium.find_element(*self._total_review_count_locator).text

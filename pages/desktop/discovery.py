#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.page import Page
from pages.desktop.base import Base


class DiscoveryPane(Base):

    _what_are_addons_text_locator = (By.CSS_SELECTOR, '#intro p')
    _mission_section_text_locator = (By.CSS_SELECTOR, '#mission > p')
    _learn_more_locator = (By.ID, 'learn-more')
    _mozilla_org_link_locator = (By.CSS_SELECTOR, '#mission a')
    _download_count_text_locator = (By.ID, 'download-count')
    _themes_section_locator = (By.ID, 'featured-themes')
    _themes_see_all_link = (By.CSS_SELECTOR, ".all[href='/en-US/firefox/themes/']")
    _themes_locator = (By.CSS_SELECTOR, '#featured-themes ul li')
    _themes_link_locator = (By.CSS_SELECTOR, '#featured-themes ul a')
    _more_ways_section_locator = (By.ID, 'more-ways')
    _more_ways_addons_locator = (By.ID, 'more-addons')
    _more_ways_complete_themes_locator = (By.ID, 'more-complete-themes')
    _up_and_coming_item = (By.XPATH, "//section[@id='up-and-coming']/ul/li/a[@class='addon-title']")
    _logout_link_locator = (By.CSS_SELECTOR, '#logout > a')

    _carousel_panels_locator = (By.CSS_SELECTOR, '#promos .slider li.panel')
    _carousel_next_panel_button_locator = (By.CSS_SELECTOR, '#nav-features .nav-next a')
    _carousel_previous_panel_button_locator = (By.CSS_SELECTOR, '#nav-features .nav-prev a')

    _featured_addons_base_locator = (By.CSS_SELECTOR, '#featured-addons .addon-title ')

    def __init__(self, testsetup, path):
        Base.__init__(self, testsetup)
        self.selenium.get(self.base_url + path)
        #resizing this page for elements that disappear when the window is < 1000
        #self.selenium.set_window_size(1000, 1000) Commented because this selenium call is still in beta

    @property
    def what_are_addons_text(self):
        return self.selenium.find_element(*self._what_are_addons_text_locator).text

    def click_learn_more(self):
        self.selenium.find_element(*self._learn_more_locator).click()

    @property
    def mission_section(self):
        return self.selenium.find_element(*self._mission_section_text_locator).text

    def mozilla_org_link_visible(self):
        return self.is_element_visible(*self._mozilla_org_link_locator)

    @property
    def download_count(self):
        return self.selenium.find_element(*self._download_count_text_locator).text

    @property
    def is_themes_section_visible(self):
        return self.is_element_visible(*self._themes_section_locator)

    @property
    def themes_count(self):
        return len(self.selenium.find_elements(*self._themes_locator))

    @property
    def is_themes_see_all_link_visible(self):
        return self.is_element_visible(*self._themes_see_all_link)

    @property
    def first_theme(self):
        return self.selenium.find_elements(*self._themes_locator)[0].text

    def click_on_first_theme(self):
        self.selenium.find_element(*self._themes_link_locator).click()
        return DiscoveryThemesDetail(self.testsetup)

    @property
    def more_ways_section_visible(self):
        return self.is_element_visible(*self._more_ways_section_locator)

    @property
    def browse_all_addons(self):
        return self.selenium.find_element(*self._more_ways_addons_locator).text

    @property
    def see_all_complete_themes(self):
        return self.selenium.find_element(*self._more_ways_complete_themes_locator).text

    @property
    def up_and_coming_item_count(self):
        return len(self.selenium.find_elements(*self._up_and_coming_item))

    def click_logout(self):
        self.selenium.find_element(*self._logout_link_locator).click()
        from pages.desktop.home import Home
        return Home(self.testsetup, open_url=False)

    @property
    def carousel_panels(self):
        return [self.CarouselPanelRegion(self.testsetup, element)
                for element in self.selenium.find_elements(*self._carousel_panels_locator)]

    def show_next_carousel_panel(self):
        self.selenium.find_element(*self._carousel_next_panel_button_locator).click()

    def show_previous_carousel_panel(self):
        self.selenium.find_element(*self._carousel_previous_panel_button_locator).click()

    class CarouselPanelRegion(Page):

        _heading_locator = (By.CSS_SELECTOR, 'h2')

        def __init__(self, testsetup, element):
            Page.__init__(self, testsetup)
            self._root_element = element

        @property
        def heading(self):
            return self._root_element.find_element(*self._heading_locator).text

        @property
        def is_visible(self):
            return self._root_element.is_displayed()

        def wait_for_next_promo(self):
            WebDriverWait(self.selenium, self.timeout).until(lambda s:
                                                         self._root_element.find_element(*self._heading_locator).is_displayed())


class DiscoveryThemesDetail(Base):

    _theme_title = (By.CSS_SELECTOR, 'h1.addon')

    @property
    def theme_title(self):
        return self.selenium.find_element(*self._theme_title).text

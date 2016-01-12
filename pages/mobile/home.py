# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.mobile.base import Base
from pages.page import Page


class Home(Base):

    _page_title = 'Add-ons for Firefox'

    _header_locator = (By.CSS_SELECTOR, 'h1.site-title > a')
    _header_logo_locator = (By.CSS_SELECTOR, '.site-title > a > img')
    _header_statement_locator = (By.CSS_SELECTOR, '#home-header > hgroup > h2')
    _learn_more_locator = (By.CSS_SELECTOR, '#learnmore')
    _learn_more_msg_locator = (By.CSS_SELECTOR, '#learnmore-msg')
    _tabs_locator = (By.CSS_SELECTOR, 'nav.tabs > ul > li')
    _search_box_locator = (By.CSS_SELECTOR, 'form#search > input')
    _search_button_locator = (By.CSS_SELECTOR, 'form#search > button')
    _logo_title_locator = (By.CSS_SELECTOR, 'h1.site-title > a')
    _logo_image_locator = (By.CSS_SELECTOR, 'h1.site-title > a > img')
    _subtitle_locator = (By.CSS_SELECTOR, 'hgroup > h2')

    _all_featured_addons_locator = (By.CSS_SELECTOR, '#list-featured > li > a')
    _default_selected_tab_locator = (By.CSS_SELECTOR, 'li.selected a')
    _categories_list_locator = (By.CSS_SELECTOR, '#listing-categories ul')
    _category_item_locator = (By.CSS_SELECTOR, 'li')

    def __init__(self, base_url, selenium):
        Base.__init__(self, base_url, selenium)
        self.selenium.get(self.base_url)
        self.is_the_current_page

    def search_for(self, search_term, click_button=True):
        search_box = self.selenium.find_element(*self._search_box_locator)
        search_box.send_keys(search_term)

        if click_button:
            self.selenium.find_element(*self._search_button_locator).click()
        else:
            search_box.submit()

        from pages.mobile.search_results import SearchResults
        return SearchResults(self.base_url, self.selenium, search_term)

    @property
    def header_text(self):
        return self.selenium.find_element(*self._header_locator).text

    @property
    def header_title(self):
        return self.selenium.find_element(*self._header_locator).get_attribute('title')

    @property
    def header_statement_text(self):
        return self.selenium.find_element(*self._header_statement_locator).text

    @property
    def is_header_firefox_logo_visible(self):
        return self.selenium.find_element(*self._header_logo_locator).is_displayed()

    @property
    def firefox_header_logo_src(self):
        return self.selenium.find_element(*self._header_logo_locator).get_attribute('src')

    @property
    def learn_more_text(self):
        return self.selenium.find_element(*self._learn_more_locator).text

    def click_learn_more(self):
        self.selenium.find_element(*self._learn_more_locator).click()

    @property
    def learn_more_msg_text(self):
        return self.selenium.find_element(*self._learn_more_msg_locator).text

    @property
    def is_learn_more_msg_visible(self):
        return self.is_element_visible(*self._learn_more_msg_locator)

    def click_all_featured_addons_link(self):
        self.scroll_to_element(*self._all_featured_addons_locator)
        self.selenium.find_element(*self._all_featured_addons_locator).click()
        from pages.mobile.extensions import Extensions
        extensions_page = Extensions(self.base_url, self.selenium)
        WebDriverWait(self.selenium, self.timeout).until(lambda s: self.is_element_visible(*extensions_page._sort_by_locator))
        return extensions_page

    @property
    def default_selected_tab_text(self):
        return self.selenium.find_element(*self._default_selected_tab_locator).text

    @property
    def tabs(self):
        return [self.Tabs(self.base_url, self.selenium, web_element)
                for web_element in self.selenium.find_elements(*self._tabs_locator)]

    def tab(self, value):
        if type(value) == int:
            return self.tabs[value]
        elif type(value) == str:
            for tab in self.tabs:
                if tab.name == value:
                    return tab

    class Tabs(Page):

        _tab_name_locator = (By.CSS_SELECTOR, 'a')
        _tab_content_locator = (By.ID, 'listing')

        def __init__(self, base_url, selenium, element):
            Page.__init__(self, base_url, selenium)
            self._root_element = element

        @property
        def name(self):
            return self._root_element.find_element(*self._tab_name_locator).text

        def click(self):
            self._root_element.find_element(*self._tab_name_locator).click()

        @property
        def is_tab_selected(self):
            is_selected = self._root_element.get_attribute('class')
            return 'selected' in is_selected

        @property
        def is_tab_content_visible(self):
            content = (self._tab_content_locator[0], '%s-%s' % (self._tab_content_locator[1], self.name.lower()))
            return self.is_element_visible(*content)

    @property
    def is_search_box_visible(self):
        return self.is_element_visible(*self._search_box_locator)

    @property
    def search_box_placeholder(self):
        return self.selenium.find_element(*self._search_box_locator).get_attribute('placeholder')

    @property
    def is_search_button_visible(self):
        return self.is_element_visible(*self._search_button_locator)

    @property
    def logo_title(self):
        return self.selenium.find_element(*self._logo_title_locator).get_attribute('title')

    @property
    def logo_text(self):
        return self.selenium.find_element(*self._logo_title_locator).text

    @property
    def logo_image_src(self):
        return self.selenium.find_element(*self._logo_image_locator).get_attribute('src')

    @property
    def subtitle(self):
        return self.selenium.find_element(*self._subtitle_locator).text

    @property
    def is_categories_region_visible(self):
        return self.is_element_visible(*self._categories_list_locator)

    @property
    def categories(self):
        return [self.Category(self.base_url, self.selenium, category_element)
                for category_element in self.selenium.find_element(*self._categories_list_locator).find_elements(*self._category_item_locator)]

    class Category(Page):

        _link_locator = (By.TAG_NAME, 'a')

        def __init__(self, base_url, selenium, category_element):
            Page.__init__(self, base_url, selenium)
            self._root_element = category_element

        @property
        def name(self):
            return self._root_element.text

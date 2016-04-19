# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.page import PageRegion


class ImageViewer(PageRegion):

    _root_locator = (By.ID, 'lightbox')
    _close_locator = (By.CLASS_NAME, 'close')
    _previous_locator = (By.CSS_SELECTOR, '.control.prev')
    _next_locator = (By.CSS_SELECTOR, '.control.next')
    _caption_locator = (By.CLASS_NAME, 'caption')
    _image_locator = (By.CSS_SELECTOR, '.content > img')

    @property
    def is_displayed(self):
        return self.root.is_displayed()

    def close(self):
        self.root.find_element(*self._close_locator).click()
        WebDriverWait(self.selenium, self.timeout).until(lambda s: not self.root.is_displayed())

    @property
    def images(self):
        return [self.Image(self.base_url, self.selenium, el) for el in
                self.root.find_elements(*self._image_locator)]

    @property
    def is_previous_displayed(self):
        return self.root.find_element(*self._previous_locator).is_displayed()

    def click_previous(self):
        self.root.find_element(*self._previous_locator).click()

    @property
    def is_next_displayed(self):
        return self.root.find_element(*self._next_locator).is_displayed()

    def click_next(self):
        self.root.find_element(*self._next_locator).click()

    @property
    def caption(self):
        return self.root.find_element(*self._caption_locator).text

    class Image(PageRegion):

        @property
        def is_displayed(self):
            return self.root.is_displayed

        @property
        def source(self):
            return self.root.get_attribute('src')

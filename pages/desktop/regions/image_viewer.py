# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.page import Page


class ImageViewer(Page):

    _image_viewer = (By.CSS_SELECTOR, '#lightbox > section')
    # controls
    _next_locator = (By.CSS_SELECTOR, 'div.controls > a.control.next')
    _previous_locator = (By.CSS_SELECTOR, 'div.controls > a.control.prev')
    _caption_locator = (By.CSS_SELECTOR, 'div.caption span')
    _close_locator = (By.CSS_SELECTOR, 'div.content > a.close')

    # content
    _images_locator = (By.CSS_SELECTOR, 'div.content > img')
    _current_image_locator = (By.CSS_SELECTOR, 'div.content > img[style*="opacity: 1"]')

    @property
    def is_visible(self):
        return self.is_element_visible(*self._image_viewer)

    @property
    def images_count(self):
        return len(self.selenium.find_elements(*self._images_locator))

    @property
    def is_next_present(self):
        return 'disabled' not in self.selenium.find_element(*self._next_locator).get_attribute('class')

    @property
    def is_previous_present(self):
        return 'disabled' not in self.selenium.find_element(*self._previous_locator).get_attribute('class')

    @property
    def image_link(self):
        return self.selenium.find_element(*self._current_image_locator).get_attribute('src')

    def click_next(self):
        self.selenium.find_element(*self._next_locator).click()

    def click_previous(self):
        self.selenium.find_element(*self._previous_locator).click()

    def close(self):
        self.selenium.find_element(*self._close_locator).click()
        WebDriverWait(self.selenium, self.timeout).until(lambda s: not self.is_element_visible(*self._image_viewer))

    @property
    def caption(self):
        return self.selenium.find_element(*self._caption_locator).text

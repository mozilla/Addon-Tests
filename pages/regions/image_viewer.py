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

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.page import Page


class ImageViewer(Page):

    _image_viewer = (By.CSS_SELECTOR, '#lightbox > section')
    #controls
    _next_locator = (By.CSS_SELECTOR, 'div.controls > a.control.next')
    _previous_locator = (By.CSS_SELECTOR, 'div.controls > a.control.prev')
    _caption_locator = (By.CSS_SELECTOR, 'div.caption span')
    _close_locator = (By.CSS_SELECTOR, 'div.content > a.close')

    #content
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
        WebDriverWait(self.selenium, 10).until(lambda s: not self.is_element_visible(*self._image_viewer))

    @property
    def caption(self):
        return self.selenium.find_element(*self._caption_locator).text

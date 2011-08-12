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
from page import Page


class ImageViewer(Page):

    _overlay_locator = "id=jquery-overlay"
    _viewer_locator = "id=jquery-lightbox"
    _image_locator = "id=lightbox-image"
    _loading_locator = "id=lightbox-loading"

    #information
    _caption_locator = "id=lightbox-image-details-caption"
    _current_number_locator = "id=lightbox-image-details-currentNumber"

    #navigation
    _image_navigator_locator = "id=lightbox-nav"
    _next_locator = "id=lightbox-nav-btnNext"
    _previous_locator = "id=lightbox-nav-btnPrev"
    _close_locator = "id=lightbox-secNav-btnClose"

    @property
    def is_visible(self):
        try:
            return self.selenium.is_visible(self._viewer_locator)
        except:
            pass
        return False

    def wait_for_viewer_to_finish_animating(self):
        self.wait_for_element_visible(self._image_navigator_locator)

    #information
    @property
    def caption(self):
        return self.get_text(self._caption_locator)

    @property
    def current_number(self):
        return self.selenium.get_text(self._current_number_locator)

    @property
    def current_image(self):
        return int(self.current_number.split(' ')[1])

    @property
    def total_images_count(self):
        return int(self.current_number.split(' ')[3])

    #navigation
    def close(self):
        self.selenium.click(self._close_locator)
        self.wait_for_element_not_present(self._viewer_locator)

    @property
    def is_close_visible(self):
        return self.selenium.is_visible(self._close_locator)

    def click_next(self):
            self.selenium.click(self._next_locator)
            self.wait_for_viewer_to_finish_animating()

    @property
    def is_next_link_visible(self):
        return  self.selenium.is_visible(self._next_locator)

    def click_previous(self):
            self.selenium.click(self._previous_locator)
            self.wait_for_viewer_to_finish_animating()

    @property
    def is_previous_link_visible(self):
        return self.selenium.is_visible(self._previous_locator)


class ImpalaImageViewer(Page):

    #controls
    _next_locator = 'css=div.controls > a.control.next'
    _previous_locator = 'css=div.controls > a.control.prev'
    _caption_locator = 'css=div.caption'
    _close_locator = 'css=div.content > a.close'

    #content
    _images_locator = 'css=div.content > img'

    @property
    def images_count(self):
        return self.selenium.get_css_count(self._images_locator)

    @property
    def is_next_visible(self):
        try:
            self.selenium.is_visible('%s.disabled' % self._next_locator)
            return False
        except:
            pass
        return True

    @property
    def is_previous_visible(self):
        try:
            self.selenium.is_visible('%s.disabled' % self._previous_locator)
            return False
        except:
            pass
        return True

    def is_nr_image_visible(self, img_nr):
        return self.selenium.is_visible('%s:nth(%s)' % (self._images_locator, img_nr))

    @property
    def image_visible(self):
        for i in range(self.images_count):
            if 'opacity: 1' in self.selenium.get_attribute('%s:nth(%s)@style' % (self._images_locator, i)):
                return i

    def click_next(self):
        current_image = self.image_visible
        self.selenium.click(self._next_locator)
        self.wait_for_element_visible('%s:nth(%s)' % (self._images_locator, current_image))

    def click_previous(self):
        return self.selenium.click(self._previous_locator)

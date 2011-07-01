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

from unittestzero import Assert
from addons_site import AddonsDetailsPage


class TestAddonDetails:

    def test_details_more_images(self, testsetup):
        """
        Litmus 4846
        https://litmus.mozilla.org/show_test.cgi?id=4846
        """
        amo_detail_page = AddonsDetailsPage(testsetup, 'firebug')

        amo_detail_page.click_addon_image()
        Assert.true(amo_detail_page.is_viewer_visible)
        amo_detail_page.viewer_close()
        Assert.false(amo_detail_page.is_viewer_visible)

        img_count = amo_detail_page.screenshot_count
        for img_no in range(0, img_count):
            amo_detail_page.screenshot_click(img_no)
            Assert.equal(img_no + 2 , int(amo_detail_page.viewer_image_count.split(' ')[1]))
            Assert.true(amo_detail_page.is_viewer_visible)
            amo_detail_page.viewer_close()
            Assert.false(amo_detail_page.is_viewer_visible)


        amo_detail_page.screenshot_click()
        Assert.true(amo_detail_page.is_viewer_visible)
        img_count = int(amo_detail_page.viewer_image_count.split(' ')[3])
        img_current = int(amo_detail_page.viewer_image_count.split(' ')[1])

        for current in range(img_current, img_count + 1):
            Assert.true(amo_detail_page.is_viewer_visible)
            Assert.equal(current , int(amo_detail_page.viewer_image_count.split(' ')[1]))
            if current != img_count:
                amo_detail_page.viewer_next()

        for current in range(img_count, 0, -1):
            Assert.true(amo_detail_page.is_viewer_visible)
            Assert.equal(current , int(amo_detail_page.viewer_image_count.split(' ')[1]))
            if current != 1:
                amo_detail_page.viewer_previous()

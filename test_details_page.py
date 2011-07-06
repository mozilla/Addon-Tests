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

from unittestzero import Assert
from addons_site import AddonsDetailsPage


class TestAddonDetails:

    def test_details_more_images(self, testsetup):
        """
        Litmus 4846
        https://litmus.mozilla.org/show_test.cgi?id=4846
        """
        amo_detail_page = AddonsDetailsPage(testsetup, 'firebug')

        image_viewer = amo_detail_page.click_addon_image()
        Assert.true(image_viewer.is_visible)
        image_viewer.close()
        Assert.false(image_viewer.is_visible)

        additional_images_count = amo_detail_page.additional_images_count
        for i in range(1, additional_images_count):
            image_viewer = amo_detail_page.click_additional_image(i)
            Assert.equal(i + 1, image_viewer.current_image)
            Assert.true(image_viewer.is_visible)
            image_viewer.close()
            Assert.false(image_viewer.is_visible)

        image_viewer = amo_detail_page.click_additional_image(1)
        Assert.true(image_viewer.is_visible)

        for i in range(2, image_viewer.total_images_count + 1):
            Assert.true(image_viewer.is_visible)
            Assert.equal(i, image_viewer.current_image)
            Assert.true(image_viewer.is_close_visible)
            Assert.equal("Image %s of %s" % (i, additional_images_count + 1), image_viewer.current_number)
            if image_viewer.is_next_link_visible:
                image_viewer.click_next()

        Assert.false(image_viewer.is_next_link_visible)
        Assert.true(image_viewer.is_previous_link_visible)

        for i in range(image_viewer.total_images_count, 0, -1):
            Assert.true(image_viewer.is_visible)
            Assert.equal(i, image_viewer.current_image)
            Assert.true(image_viewer.is_close_visible)
            Assert.equal("Image %s of %s" % (i, additional_images_count + 1), image_viewer.current_number)
            if image_viewer.is_previous_link_visible:
                image_viewer.click_previous()

        Assert.true(image_viewer.is_next_link_visible)
        Assert.false(image_viewer.is_previous_link_visible)

        image_viewer.close()
        Assert.false(image_viewer.is_visible)

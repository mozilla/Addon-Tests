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
# Contributor(s): Tobias Markus <tobbi.bugs@googlemail.com>
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
import pytest
from unittestzero import Assert

from addons_site import AddonsHomePage

class TestReviews:

    def test_that_all_reviews_hyperlink_works(self, testsetup):
        """ Test for litmus 4843
            https://litmus.mozilla.org/show_test.cgi?id=4843
        """
        amo_home_page = AddonsHomePage(testsetup)
        amo_home_page.open_details_page_for_id(1865)
        Assert.true(amo_home_page.has_reviews)

        amo_home_page.click_all_reviews_link()
        Assert.equal(amo_home_page.review_count, 20)
        
        #Go to the last page and check that the next button is not present
        amo_home_page.go_to_last_page()
        Assert.false(amo_home_page.is_next_link_present)
        
        #Go one page back, check that it has 20 reviews
        #that the page number decreases and that the next link is visible
        page_number = amo_home_page.current_page
        amo_home_page.page_back()
        Assert.true(amo_home_page.is_next_link_visible)
        Assert.equal(amo_home_page.review_count, 20)
        Assert.equal(amo_home_page.current_page, page_number - 1)

        #Go to the first page and check that the prev button is not present
        amo_home_page.go_to_first_page()
        Assert.false(amo_home_page.is_prev_link_present)
        
        #Go one page forward, check that it has 20 reviews,
        #that the page number increases and that the prev link is visible
        page_number = amo_home_page.current_page
        amo_home_page.page_forward()
        Assert.true(amo_home_page.is_prev_link_visible)
        Assert.equal(amo_home_page.review_count, 20)
        Assert.equal(amo_home_page.current_page, page_number + 1)

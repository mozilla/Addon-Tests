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
#                 Alex Rodionov <p0deje@gmail.com>
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

import pytest

from datetime import datetime
from unittestzero import Assert

from pages.home import Home
from pages.details import Details

xfail = pytest.mark.xfail
nondestructive = pytest.mark.nondestructive
destructive = pytest.mark.destructive


class TestReviews:

    @nondestructive
    def test_that_all_reviews_hyperlink_works(self, mozwebqa):
        """ Test for litmus 4843
            https://litmus.mozilla.org/show_test.cgi?id=4843
        """
        #Open details page for Adblock Plus
        details_page = Details(mozwebqa, 'Adblock Plus')
        Assert.true(details_page.has_reviews)

        details_page.click_all_reviews_link()
        Assert.equal(details_page.review_count, 20)

        #Go to the last page and check that the next button is not present
        details_page.go_to_last_page()
        Assert.false(details_page.is_next_link_enabled)

        #Go one page back, check that it has 20 reviews
        #that the page number decreases and that the next link is visible
        page_number = details_page.current_page
        details_page.page_back()
        Assert.true(details_page.is_next_link_visible)
        Assert.equal(details_page.review_count, 20)
        Assert.equal(details_page.current_page, page_number - 1)

        #Go to the first page and check that the prev button is not present
        details_page.go_to_first_page()
        Assert.false(details_page.is_prev_link_enabled)

        #Go one page forward, check that it has 20 reviews,
        #that the page number increases and that the prev link is visible
        page_number = details_page.current_page
        details_page.page_forward()
        Assert.true(details_page.is_prev_link_visible)
        Assert.equal(details_page.review_count, 20)
        Assert.equal(details_page.current_page, page_number + 1)

    @xfail(reason="bug 708970")
    @destructive
    def test_that_new_review_is_saved(self, mozwebqa):
        """ Litmus 22921
            https://litmus.mozilla.org/show_test.cgi?id=22921 """
        # Step 1 - Login into AMO
        home_page = Home(mozwebqa)
        home_page.login("browserID")
        Assert.true(home_page.is_the_current_page)
        Assert.true(home_page.header.is_user_logged_in)

        # Step 2 - Load any addon detail page
        details_page = Details(mozwebqa, 'Adblock Plus')

        # Step 3 - Click on "Write review" button
        write_review_block = details_page.click_to_write_review()

        # Step 4 - Write a review
        body = 'Automatic addon review by Selenium tests %s' % datetime.now()
        write_review_block.enter_review_with_text(body)
        write_review_block.set_review_rating(1)
        review_page = write_review_block.click_to_save_review()

        # Step 5 - Assert review
        review = review_page.reviews[0]
        Assert.equal(review.rating, 1)
        Assert.equal(review.author, mozwebqa.credentials['default']['name'])
        date = datetime.now().strftime("%B %d, %Y")
        # there are no leading zero-signs on day so we need to remove them too
        date = date.replace(' 0', ' ')
        Assert.equal(review.date, date)
        Assert.equal(review.text, body)

    @xfail(reason="refactoring to compensate for purchased addons http://bit.ly/ucH6Ow")
    @destructive
    def test_that_one_star_rating_increments(self, mozwebqa):
        """ Litmus 22916
            https://litmus.mozilla.org/show_test.cgi?id=22916 """
        # Step 1 - Login into AMO
        home_page = Home(mozwebqa)
        home_page.login("browserID")
        Assert.true(home_page.header.is_user_logged_in)

        # Step 2 - Go to add-ons listing page sorted by rating
        extensions_home_page = home_page.click_to_explore('Top Rated')

        # Step 3 - Pick an addon with no reviews
        extensions_home_page.go_to_last_page()
        addon = extensions_home_page.extensions[-1]  # the last one is without rating
        details_page = addon.click()

        # Step 4 - Click on the "Write review" button
        write_review_block = details_page.click_to_write_review()

        # Step 5 - Add review with 1-star rating
        body = 'Automatic addon review by Selenium tests'
        write_review_block.enter_review_with_text(body)
        write_review_block.set_review_rating(1)
        view_reviews = write_review_block.click_to_save_review()

        # Step 6 - Ensure rating increased by one
        view_reviews.breadcrumbs[2].click_breadcrumb()
        details_page = Details(mozwebqa)
        new_rating_counter = details_page.get_rating_counter(1)
        Assert.equal(new_rating_counter, 1)

    @xfail(reason="refactoring to compensate for purchased addons http://bit.ly/ucH6Ow")
    @destructive
    def test_that_two_star_rating_increments(self, mozwebqa):
        """ Litmus 22917
            https://litmus.mozilla.org/show_test.cgi?id=22917 """
        # Step 1 - Login into AMO
        home_page = Home(mozwebqa)
        home_page.login("browserID")
        Assert.true(home_page.header.is_user_logged_in)

        # Step 2 - Go to add-ons listing page sorted by rating
        extensions_home_page = home_page.click_to_explore('Top Rated')

        # Step 3 - Pick an addon with no reviews
        extensions_home_page.go_to_last_page()
        addon = extensions_home_page.extensions[-1]  # the last one is without rating
        details_page = addon.click()

        # Step 4 - Click on the "Write review" button
        write_review_block = details_page.click_to_write_review()

        # Step 5 - Add review with 1-star rating
        body = 'Automatic addon review by Selenium tests'
        write_review_block.enter_review_with_text(body)
        write_review_block.set_review_rating(2)
        view_reviews = write_review_block.click_to_save_review()

        # Step 6 - Ensure rating increased by one
        view_reviews.breadcrumbs[2].click_breadcrumb()
        details_page = Details(mozwebqa)
        new_rating_counter = details_page.get_rating_counter(2)
        Assert.equal(new_rating_counter, 1)

    @xfail(reason="refactoring to compensate for purchased addons http://bit.ly/ucH6Ow")
    @destructive
    def test_that_three_star_rating_increments(self, mozwebqa):
        """ Litmus 22918
            https://litmus.mozilla.org/show_test.cgi?id=22918 """
        # Step 1 - Login into AMO
        home_page = Home(mozwebqa)
        home_page.login("browserID")
        Assert.true(home_page.header.is_user_logged_in)

        # Step 2 - Go to add-ons listing page sorted by rating
        extensions_home_page = home_page.click_to_explore('Top Rated')

        # Step 3 - Pick an addon with no reviews
        extensions_home_page.go_to_last_page()
        addon = extensions_home_page.extensions[-1]  # the last one is without rating
        details_page = addon.click()

        # Step 4 - Click on the "Write review" button
        write_review_block = details_page.click_to_write_review()

        # Step 5 - Add review with 1-star rating
        body = 'Automatic addon review by Selenium tests'
        write_review_block.enter_review_with_text(body)
        write_review_block.set_review_rating(3)
        view_reviews = write_review_block.click_to_save_review()

        # Step 6 - Ensure rating increased by one
        view_reviews.breadcrumbs[2].click_breadcrumb()
        details_page = Details(mozwebqa)
        new_rating_counter = details_page.get_rating_counter(3)
        Assert.equal(new_rating_counter, 1)

    @xfail(reason="refactoring to compensate for purchased addons http://bit.ly/ucH6Ow")
    @destructive
    def test_that_four_star_rating_increments(self, mozwebqa):
        """ Litmus 22919
            https://litmus.mozilla.org/show_test.cgi?id=22918 """
        # Step 1 - Login into AMO
        home_page = Home(mozwebqa)
        home_page.login("browserID")
        Assert.true(home_page.header.is_user_logged_in)

        # Step 2 - Go to add-ons listing page sorted by rating
        extensions_home_page = home_page.click_to_explore('Top Rated')

        # Step 3 - Pick an addon with no reviews
        extensions_home_page.go_to_last_page()
        addon = extensions_home_page.extensions[-1]  # the last one is without rating
        details_page = addon.click()

        # Step 4 - Click on the "Write review" button
        write_review_block = details_page.click_to_write_review()

        # Step 5 - Add review with 1-star rating
        body = 'Automatic addon review by Selenium tests'
        write_review_block.enter_review_with_text(body)
        write_review_block.set_review_rating(4)
        view_reviews = write_review_block.click_to_save_review()

        # Step 6 - Ensure rating increased by one
        view_reviews.breadcrumbs[2].click_breadcrumb()
        details_page = Details(mozwebqa)
        new_rating_counter = details_page.get_rating_counter(4)
        Assert.equal(new_rating_counter, 1)

    @xfail(reason="refactoring to compensate for purchased addons http://bit.ly/ucH6Ow")
    @destructive
    def test_that_five_star_rating_increments(self, mozwebqa):
        """ Litmus 22920
            https://litmus.mozilla.org/show_test.cgi?id=22920 """
        # Step 1 - Login into AMO
        home_page = Home(mozwebqa)
        home_page.login("browserID")
        Assert.true(home_page.header.is_user_logged_in)

        # Step 2 - Go to add-ons listing page sorted by rating
        extensions_home_page = home_page.click_to_explore('Top Rated')

        # Step 3 - Pick an addon with no reviews
        extensions_home_page.go_to_last_page()
        addon = extensions_home_page.extensions[-1]  # the last one is without rating
        details_page = addon.click()

        # Step 4 - Click on the "Write review" button
        write_review_block = details_page.click_to_write_review()

        # Step 5 - Add review with 1-star rating
        body = 'Automatic addon review by Selenium tests'
        write_review_block.enter_review_with_text(body)
        write_review_block.set_review_rating(5)
        view_reviews = write_review_block.click_to_save_review()

        # Step 6 - Ensure rating increased by one
        view_reviews.breadcrumbs[2].click_breadcrumb()
        details_page = Details(mozwebqa)
        new_rating_counter = details_page.get_rating_counter(5)
        Assert.equal(new_rating_counter, 1)

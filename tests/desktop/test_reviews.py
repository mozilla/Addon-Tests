#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from datetime import datetime
from unittestzero import Assert

from pages.desktop.home import Home
from pages.desktop.details import Details


class TestReviews:

    @pytest.mark.nondestructive
    def test_that_all_reviews_hyperlink_works(self, mozwebqa):
        """
        Test for Litmus 4843.
        https://litmus.mozilla.org/show_test.cgi?id=4843
        """
        #Open details page for MemChaser
        details_page = Details(mozwebqa, "Firebug")
        Assert.true(details_page.has_reviews)

        details_page.click_all_reviews_link()
        Assert.equal(details_page.review_count, 20)

        #Go to the last page and check that the next button is not present
        details_page.paginator.click_last_page()
        Assert.true(details_page.paginator.is_next_page_disabled)

        #Go one page back, check that it has 20 reviews
        #that the page number decreases and that the next link is visible
        page_number = details_page.paginator.page_number
        details_page.paginator.click_prev_page()
        Assert.false(details_page.paginator.is_next_page_disabled)
        Assert.equal(details_page.review_count, 20)
        Assert.equal(details_page.paginator.page_number, page_number - 1)

        #Go to the first page and check that the prev button is not present
        details_page.paginator.click_first_page()
        Assert.true(details_page.paginator.is_prev_page_disabled)

        #Go one page forward, check that it has 20 reviews,
        #that the page number increases and that the prev link is visible
        page_number = details_page.paginator.page_number
        details_page.paginator.click_next_page()
        Assert.false(details_page.paginator.is_prev_page_disabled)
        Assert.equal(details_page.review_count, 20)
        Assert.equal(details_page.paginator.page_number, page_number + 1)

    @pytest.mark.native
    @pytest.mark.login
    def test_that_new_review_is_saved(self, mozwebqa):
        """
        Test for Litmus 22921.
        https://litmus.mozilla.org/show_test.cgi?id=22921
        """
        # Step 1 - Login into AMO
        home_page = Home(mozwebqa)
        home_page.login("browserID")
        Assert.true(home_page.is_the_current_page)
        Assert.true(home_page.header.is_user_logged_in)

        # Step 2 - Load any addon detail page
        details_page = Details(mozwebqa, 'Memchaser')

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

        review.delete()

        details_page = Details(mozwebqa, 'Memchaser')
        review_page = details_page.click_all_reviews_link()

        for review in review_page.reviews:
            Assert.false(body in review.text)

    @pytest.mark.native
    @pytest.mark.xfail(reason="refactoring to compensate for purchased addons http://bit.ly/ucH6Ow")
    @pytest.mark.login
    def test_that_one_star_rating_increments(self, mozwebqa):
        """
        Test for Litmus 22916.
        https://litmus.mozilla.org/show_test.cgi?id=22916
        """
        # Step 1 - Login into AMO
        home_page = Home(mozwebqa)
        home_page.login("browserID")
        Assert.true(home_page.header.is_user_logged_in)

        # Step 2 - Go to add-ons listing page sorted by rating
        extensions_home_page = home_page.click_to_explore('Top Rated')

        # Step 3 - Pick an addon with no reviews
        extensions_home_page.paginator.click_last_page()
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
        view_reviews.breadcrumbs[2].click()
        details_page = Details(mozwebqa)
        new_rating_counter = details_page.get_rating_counter(1)
        Assert.equal(new_rating_counter, 1)

    @pytest.mark.native
    @pytest.mark.xfail(reason="refactoring to compensate for purchased addons http://bit.ly/ucH6Ow")
    @pytest.mark.login
    def test_that_two_star_rating_increments(self, mozwebqa):
        """
        Test for Litmus 22917.
        https://litmus.mozilla.org/show_test.cgi?id=22917
        """
        # Step 1 - Login into AMO
        home_page = Home(mozwebqa)
        home_page.login("browserID")
        Assert.true(home_page.header.is_user_logged_in)

        # Step 2 - Go to add-ons listing page sorted by rating
        extensions_home_page = home_page.click_to_explore('Top Rated')

        # Step 3 - Pick an addon with no reviews
        extensions_home_page.paginator.click_last_page()
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
        view_reviews.breadcrumbs[2].click()
        details_page = Details(mozwebqa)
        new_rating_counter = details_page.get_rating_counter(2)
        Assert.equal(new_rating_counter, 1)

    @pytest.mark.native
    @pytest.mark.xfail(reason="refactoring to compensate for purchased addons http://bit.ly/ucH6Ow")
    @pytest.mark.login
    def test_that_three_star_rating_increments(self, mozwebqa):
        """
        Test for Litmus 22918.
        https://litmus.mozilla.org/show_test.cgi?id=22918
        """
        # Step 1 - Login into AMO
        home_page = Home(mozwebqa)
        home_page.login("browserID")
        Assert.true(home_page.header.is_user_logged_in)

        # Step 2 - Go to add-ons listing page sorted by rating
        extensions_home_page = home_page.click_to_explore('Top Rated')

        # Step 3 - Pick an addon with no reviews
        extensions_home_page.paginator.click_last_page()
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
        view_reviews.breadcrumbs[2].click()
        details_page = Details(mozwebqa)
        new_rating_counter = details_page.get_rating_counter(3)
        Assert.equal(new_rating_counter, 1)

    @pytest.mark.native
    @pytest.mark.xfail(reason="refactoring to compensate for purchased addons http://bit.ly/ucH6Ow")
    @pytest.mark.login
    def test_that_four_star_rating_increments(self, mozwebqa):
        """
        Test for Litmus 22919.
        https://litmus.mozilla.org/show_test.cgi?id=22918
        """
        # Step 1 - Login into AMO
        home_page = Home(mozwebqa)
        home_page.login("browserID")
        Assert.true(home_page.header.is_user_logged_in)

        # Step 2 - Go to add-ons listing page sorted by rating
        extensions_home_page = home_page.click_to_explore('Top Rated')

        # Step 3 - Pick an addon with no reviews
        extensions_home_page.paginator.click_last_page()
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
        view_reviews.breadcrumbs[2].click()
        details_page = Details(mozwebqa)
        new_rating_counter = details_page.get_rating_counter(4)
        Assert.equal(new_rating_counter, 1)

    @pytest.mark.native
    @pytest.mark.xfail(reason="refactoring to compensate for purchased addons http://bit.ly/ucH6Ow")
    @pytest.mark.login
    def test_that_five_star_rating_increments(self, mozwebqa):
        """
        Test for Litmus 22920
        https://litmus.mozilla.org/show_test.cgi?id=22920
        """
        # Step 1 - Login into AMO
        home_page = Home(mozwebqa)
        home_page.login("browserID")
        Assert.true(home_page.header.is_user_logged_in)

        # Step 2 - Go to add-ons listing page sorted by rating
        extensions_home_page = home_page.click_to_explore('Top Rated')

        # Step 3 - Pick an addon with no reviews
        extensions_home_page.paginator.click_last_page()
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
        view_reviews.breadcrumbs[2].click()
        details_page = Details(mozwebqa)
        new_rating_counter = details_page.get_rating_counter(5)
        Assert.equal(new_rating_counter, 1)

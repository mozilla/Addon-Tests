# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from datetime import datetime

import pytest
from pytz import timezone

from pages.desktop.home import Home
from pages.desktop.details import Details


class TestReviews:

    @pytest.mark.nondestructive
    def test_that_all_reviews_hyperlink_works(self, base_url, selenium):
        # Open details page for MemChaser
        details_page = Details(base_url, selenium, "Firebug")
        assert details_page.has_reviews

        view_reviews = details_page.click_all_reviews_link()
        assert 20 == len(view_reviews.reviews)

        # Go to the last page and check that the next button is not present
        view_reviews.paginator.click_last_page()
        assert view_reviews.paginator.is_next_page_disabled

        # Go one page back, check that it has 20 reviews
        # that the page number decreases and that the next link is visible
        page_number = view_reviews.paginator.page_number
        view_reviews.paginator.click_prev_page()
        assert not view_reviews.paginator.is_next_page_disabled
        assert 20 == len(view_reviews.reviews)
        assert page_number - 1 == view_reviews.paginator.page_number

        # Go to the first page and check that the prev button is not present
        view_reviews.paginator.click_first_page()
        assert view_reviews.paginator.is_prev_page_disabled

        # Go one page forward, check that it has 20 reviews,
        # that the page number increases and that the prev link is visible
        page_number = view_reviews.paginator.page_number
        view_reviews.paginator.click_next_page()
        assert not view_reviews.paginator.is_prev_page_disabled
        assert 20 == len(view_reviews.reviews)
        assert page_number + 1 == view_reviews.paginator.page_number

    @pytest.mark.native
    @pytest.mark.login
    def test_that_new_review_is_saved(self, base_url, selenium, existing_user):
        # Step 1 - Login into AMO
        home_page = Home(base_url, selenium)
        home_page.login(existing_user['email'], existing_user['password'])
        assert home_page.is_the_current_page
        assert home_page.header.is_user_logged_in

        # Step 2 - Load any addon detail page
        details_page = Details(base_url, selenium, 'Memchaser')

        # Step 3 - Click on "Write review" button
        write_review_block = details_page.click_to_write_review()

        # Step 4 - Write a review
        body = 'Automatic addon review by Selenium tests %s' % datetime.now()
        write_review_block.enter_review_with_text(body)
        write_review_block.set_review_rating(1)
        review_page = write_review_block.click_to_save_review()

        # Step 5 - Assert review
        review = review_page.reviews[0]
        assert 1 == review.rating
        assert existing_user['name'] == review.author
        date = datetime.now(timezone('US/Pacific')).strftime("%B %d, %Y")
        # there are no leading zero-signs on day so we need to remove them too
        expected_date = date.replace(' 0', ' ')
        assert expected_date == review.date, 'Date of review does not match the expected value.'
        assert body == review.text, 'Review text does not match expected value.'

        review.delete()

        details_page = Details(base_url, selenium, 'Memchaser')
        review_page = details_page.click_all_reviews_link()

        for review in review_page.reviews:
            assert body not in review.text

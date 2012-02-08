#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from pages.base import Base


class WriteReviewBlock(Base):

    _add_review_input_field_locator = (By.ID, "id_body")
    _add_review_input_rating_locator = (By.CSS_SELECTOR, "span[class='ratingwidget stars stars-0'] > label")
    _add_review_submit_button_locator = (By.CSS_SELECTOR, "#review-box input[type=submit]")

    _add_review_box = (By.CSS_SELECTOR, '#review-box')

    def enter_review_with_text(self, text):
        self.selenium.find_element(*self._add_review_input_field_locator).send_keys(text)

    def set_review_rating(self, rating):
        locator = self.selenium.find_element(self._add_review_input_rating_locator[0],
                                             '%s[data-stars="%s"]' % (self._add_review_input_rating_locator[1], rating))
        ActionChains(self.selenium).move_to_element(locator).\
            click().perform()

    def click_to_save_review(self):
        self.selenium.find_element(*self._add_review_submit_button_locator).click()
        return ViewReviews(self.testsetup)

    @property
    def is_review_box_visible(self):
        return self.is_element_visible(*self._add_review_box)


class ViewReviews(Base):

    _review_locator = (By.CSS_SELECTOR, "div.primary div.review")

    @property
    def reviews(self):
        """Returns review object with index."""
        return [self.ReviewSnippet(self.testsetup, element) for element in self.selenium.find_elements(*self._review_locator)]

    class ReviewSnippet(Base):

        _review_text_locator = (By.CSS_SELECTOR, ".description")
        _review_rating_locator = (By.CSS_SELECTOR, "span[itemprop=rating]")
        _review_author_locator = (By.CSS_SELECTOR, "a:not(.permalink)")
        _review_date_locator = (By.CSS_SELECTOR, ".byline")

        def __init__(self, testsetup, element):
            Base.__init__(self, testsetup)
            self._root_element = element

        @property
        def text(self):
            return self._root_element.find_element(*self._review_text_locator).text

        @property
        def rating(self):
            return int(self._root_element.find_element(*self._review_rating_locator).text)

        @property
        def author(self):
            return self._root_element.find_element(*self._review_author_locator).text

        @property
        def date(self):
            date = self._root_element.find_element(*self._review_date_locator).text
            # we need to parse the string first to get date
            date = re.match('^(.+on\s)([A-Za-z]+\s[\d]+,\s[\d]+)', date)
            return date.group(2)


class UserFAQ(Base):

    _license_question_locator = (By.CSS_SELECTOR, '#license')
    _license_answer_locator = (By.CSS_SELECTOR, '#license + dd')

    @property
    def license_question(self):
        return self.selenium.find_element(*self._license_question_locator).text

    @property
    def license_answer(self):
        return self.selenium.find_element(*self._license_answer_locator).text

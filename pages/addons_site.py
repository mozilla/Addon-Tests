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
# Contributor(s): David Burns
#                 Marc George
#                 Dave Hunt <dhunt@mozilla.com>
#                 Alex Rodionov <p0deje@gmail.com>
#                 Joel Andersson <janderssn@gmail.com>
#                 Bebe <florin.strugariu@softvision.ro>
#                 Marlena Compton <mcompton@mozilla.com>
#                 Teodosia Pop <teodosia.pop@softvision.ro>
#                 Alex Lakatos <alex@greensqr.com>
#                 Alin Trif <alin.trif@softvision.ro>
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

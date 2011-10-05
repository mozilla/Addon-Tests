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
import urllib2
from urllib2 import urlparse

from page import Page
from base_page import BasePage


class WriteReviewBlock(BasePage):

    _add_review_input_field_locator = "id=id_body"
    _add_review_input_rating_locator = "css=.ratingwidget input"
    _add_review_submit_button_locator = "css=#review-box input[type=submit]"

    _add_review_box = 'css=#review-box'

    def enter_review_with_text(self, text):
        self.selenium.type(self._add_review_input_field_locator, text)

    def set_review_rating(self, rating):
        locator = "%s[value=%s]" % (self._add_review_input_rating_locator, rating)
        self.selenium.click(locator)

    def click_to_save_review(self):
        self.selenium.click(self._add_review_submit_button_locator)
        self.selenium.wait_for_page_to_load(self.timeout)
        return ViewReviewsPage(self.testsetup)

    @property
    def is_review_box_visible(self):
        return self.selenium.is_visible(self._add_review_box)


class ViewReviewsPage(BasePage):

    _review_locator = "css=div.primary div.review"

    def review(self, index=0):
        """ Returns review object with index. """
        return self.ReviewSnippet(self.testsetup, index)

    def reviews(self):
        """ Returns all reviews on the page. """
        return [self.ReviewSnippet(self.testsetup, i) for i in
                range(self.selenium.get_css_count(self._review_locator))]

    class ReviewSnippet(BasePage):

        _review_locator = "css=div.primary div.review"
        _review_text_locator = "p.review-body"
        _review_rating_locator = "span[itemprop=rating]"
        _review_author_locator = "a:not(.permalink)"
        _review_date_locator = "div.reviewed-on"

        def __init__(self, testsetup, index):
            BasePage.__init__(self, testsetup)
            self.index = index

        def absolute_locator(self, relative_locator):
            return "%s:nth(%s) %s" % (self._review_locator,
                                      self.index, relative_locator)

        @property
        def text(self):
            text_locator = self.absolute_locator(self._review_text_locator)
            return self.selenium.get_text(text_locator)

        @property
        def rating(self):
            _rating_locator = self.absolute_locator(self._review_rating_locator)
            return int(self.selenium.get_text(_rating_locator))

        @property
        def author(self):
            author_locator = self.absolute_locator(self._review_author_locator)
            return self.selenium.get_text(author_locator)

        @property
        def date(self):
            date_locator = self.absolute_locator(self._review_date_locator)
            date = self.selenium.get_text(date_locator)
            # we need to parse the string first to get date
            date = re.match('^(.+on\s)([A-Za-z]+\s[\d]+,\s[\d]+)(.+)$', date)
            return date.group(2)


class UserFAQPage(BasePage):

    _license_question_locator = "css=#license"
    _license_answer_locator = "css=#license + dd"

    @property
    def license_question(self):
        return self.selenium.get_text(self._license_question_locator)

    @property
    def license_answer(self):
        return self.selenium.get_text(self._license_answer_locator)

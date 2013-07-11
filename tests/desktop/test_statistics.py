#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from urlparse import urlparse
from datetime import datetime, timedelta
import json

import requests
import pytest
from unittestzero import Assert

from pages.desktop.details import Details


class TestStatistics:

    @pytest.mark.nondestructive
    def test_that_verifies_the_url_of_the_statistics_page(self, mozwebqa):
        """ Test for Litmus 25710
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=25710
        """

        details_page = Details(mozwebqa, "Firebug")
        statistics_page = details_page.click_view_statistics()

        Assert.true(statistics_page.is_the_current_page)
        Assert.contains("/statistics", statistics_page.get_url_current_page())

    @pytest.mark.skipif('urlparse(config.getvalue("base_url")).netloc != "addons.mozilla.org"')
    @pytest.mark.skip_selenium
    @pytest.mark.nondestructive
    def test_that_checks_content_in_json_endpoints_from_statistics_urls(self, mozwebqa):
        """https://github.com/mozilla/Addon-Tests/issues/621"""

        # make statistics url template
        base_url = mozwebqa.base_url
        temp_url = '/firefox/addon/firebug/statistics/overview-day-%(start)s-%(end)s.json'
        statistics_url_template = base_url + temp_url

        # set statistics timeframe
        last_date = datetime.today().date() - timedelta(days=1)
        first_date = datetime.today().date() - timedelta(days=30)

        # convert datetime objects to required string representation
        end = str(last_date).replace('-', '')
        start = str(first_date).replace('-', '')

        # make request and assert that status code is OK
        r = requests.get(statistics_url_template % locals())
        Assert.equal(r.status_code, 200,
                     'request to %s failed with %s status code' % (r.url, r.status_code))

        # decode response and assert it's not empty
        response = json.loads(r.content)
        Assert.equal(len(response), 30,
                     'some dates (or all) dates are missing in response')

        dates = []
        for value in response:
            dates.append(value['date'])
            downloads, updates = value['data'].values()
            # check that download and update values are equal or greater than zero
            Assert.greater_equal(downloads, 0)
            Assert.greater_equal(updates, 0)

        # ensure that response contains all dates for given timeframe
        Assert.equal(dates, [str(last_date - timedelta(days=i)) for i in xrange(30)],
                     'wrong dates in response')

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from datetime import datetime, timedelta
import json

import requests
import pytest

from pages.desktop.details import Details


class TestStatistics:

    @pytest.mark.nondestructive
    def test_that_verifies_the_url_of_the_statistics_page(self, base_url, selenium):
        details_page = Details(base_url, selenium, "Firebug")
        statistics_page = details_page.click_view_statistics()
        assert statistics_page.is_the_current_page
        assert '/statistics' in statistics_page.get_url_current_page()

    @pytest.mark.nondestructive
    def test_that_checks_content_in_json_endpoints_from_statistics_urls(self, base_url):
        """https://github.com/mozilla/Addon-Tests/issues/621"""

        # make statistics url template
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
        assert requests.codes.ok == r.status_code, 'request to %s failed with %s status code' % (r.url, r.status_code)

        # Decode response and assert it's not empty.
        # Only run against prod, data on dev & stage is insufficient.
        if 'mozilla.org' in base_url:
            response = json.loads(r.content)
            assert 30 == len(response), 'some dates (or all) dates are missing in response'

            dates = []
            for value in response:
                dates.append(value['date'])
                downloads, updates = value['data'].values()
                # check that download and update values are equal or greater than zero
                assert downloads >= 0
                assert updates >= 0

            # ensure that response contains all dates for given timeframe
            expected_dates = [str(last_date - timedelta(days=i)) for i in xrange(30)]
            assert expected_dates == dates, 'wrong dates in response'

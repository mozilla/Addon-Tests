# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from datetime import datetime, timedelta

import requests
import pytest

from pages.desktop.details import Details


@pytest.mark.nondestructive
def test_that_verifies_the_url_of_the_statistics_page(base_url, selenium):
    details_page = Details(base_url, selenium, "Firebug")
    statistics_page = details_page.click_view_statistics()
    assert statistics_page.is_the_current_page
    assert '/statistics' in statistics_page.get_url_current_page()


@pytest.mark.nondestructive
@pytest.mark.skipif(
    'mozilla.org' not in pytest.config.getoption('base_url'),
    reason='Only run against prod, data on dev & stage is insufficient')
def test_that_checks_content_in_json_endpoints_from_statistics_urls(base_url):
    """https://github.com/mozilla/Addon-Tests/issues/621"""

    # set statistics timeframe
    base = datetime.today().date() - timedelta(days=2)
    dates = [base - timedelta(days=x) for x in range(0, 30)]

    # make request and assert that status code is OK
    url = '/firefox/addon/firebug/statistics/overview-day-{}-{}.json'.format(
        dates[-1].strftime('%Y%m%d'), dates[0].strftime('%Y%m%d'))
    response = requests.get(base_url + url).json()

    expected = [d.strftime('%Y-%m-%d') for d in dates]
    actual = [d['date'] for d in response]
    assert expected == actual

    for data in [d['data'] for d in response]:
        assert data['downloads'] >= 0
        assert data['updates'] >= 0

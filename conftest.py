# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest


@pytest.fixture(scope='session')
def capabilities(capabilities):
    capabilities.setdefault('tags', []).append('amo')
    return capabilities


def pytest_addoption(parser):
    parser.addoption("--servicesbaseurl",
                     action="store",
                     dest='services_base_url',
                     metavar='str',
                     default="",
                     help="specify the api url")


@pytest.fixture(scope='session')
def services_base_url(request, base_url):
    config = request.config
    services_base_url = config.getoption('services_base_url')
    return services_base_url or base_url


@pytest.fixture
def stored_users(variables):
    return variables['users']


@pytest.fixture
def existing_user(stored_users):
    return stored_users['default']


@pytest.fixture
def editable_user(stored_users):
    """Returns a user that can be safely edited by the tests."""
    return stored_users['editable']


@pytest.fixture
def paypal_user(variables):
    return variables['paypal']


@pytest.fixture
def selenium(selenium):
    selenium.implicitly_wait(10)
    return selenium

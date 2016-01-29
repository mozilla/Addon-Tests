# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from fxapom.fxapom import FxATestAccount
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
def fxa_account():
    return FxATestAccount()


@pytest.fixture
def existing_user(request, base_url, stored_users):
    if '-dev' in base_url:
        # Firefox Accounts is only active on dev at this time
        fxa_account = request.getfuncargvalue('fxa_account')
        user = {'email': fxa_account.email,
                'password': fxa_account.password,
                'name': fxa_account.email.split('@')[0]}
        # FIXME: This is an ugly workaround that creates an account in AMO for
        # the generated Firefox Account. https://github.com/mozilla/olympia/issues/1551
        selenium = request.getfuncargvalue('selenium')
        from pages.desktop.home import Home
        Home(base_url, selenium).login(user['email'], user['password'])
        from pages.desktop.user import EditProfile
        profile = EditProfile(base_url, selenium)
        profile.type_username(user['name'])
        profile.click_update_account()
        profile.header.click_logout()
        return user
    return stored_users['default']


@pytest.fixture
def editable_user(request, base_url, stored_users):
    """Returns a user that can be safely edited by the tests."""
    if '-dev' in base_url:
        # FxA is only active on dev at this time
        return request.getfuncargvalue('existing_user')
    return stored_users['editable']


@pytest.fixture
def paypal_user(variables):
    return variables['paypal']


@pytest.fixture
def selenium(selenium):
    selenium.implicitly_wait(10)
    return selenium

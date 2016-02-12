# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from fxapom.fxapom import DEV_URL, PROD_URL, FxATestAccount
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
def fxa_account(base_url):
    url = DEV_URL if 'dev' in base_url else PROD_URL
    return FxATestAccount(url)


@pytest.fixture
def user(request, base_url):
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


@pytest.fixture
def paypal_user(variables):
    return variables['paypal']


@pytest.fixture
def selenium(selenium):
    selenium.implicitly_wait(10)
    return selenium

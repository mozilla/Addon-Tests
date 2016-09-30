# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import datetime
import urlparse

from fxapom.fxapom import DEV_URL, PROD_URL, FxATestAccount
import jwt
import pytest
import requests


@pytest.fixture(scope='session')
def session_capabilities(session_capabilities):
    session_capabilities.setdefault('tags', []).append('amo')
    return session_capabilities


@pytest.fixture
def fxa_account(base_url):
    url = DEV_URL if 'dev' in base_url else PROD_URL
    return FxATestAccount(url)


@pytest.fixture
def jwt_token(base_url, variables):
    variables = variables['api'][urlparse.urlsplit(base_url).hostname]
    payload = {
        'iss': variables['jwt_issuer'],
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30)}
    return jwt.encode(payload, variables['jwt_secret'], algorithm='HS256')


@pytest.fixture
def user(base_url, fxa_account, jwt_token):
    user = {
        'email': fxa_account.email,
        'password': fxa_account.password,
        'username': fxa_account.email.split('@')[0]}
    url = '{base_url}/api/v3/accounts/super-create/'.format(base_url=base_url)
    params = {
        'email': user['email'],
        'username': user['username'],
        'fxa_id': fxa_account.session.uid}
    headers = {'Authorization': 'JWT {token}'.format(token=jwt_token)}
    r = requests.post(url, data=params, headers=headers)
    assert requests.codes.created == r.status_code
    user.update(r.json())
    return user


@pytest.fixture
def paypal_user(variables):
    return variables['paypal']


@pytest.fixture
def selenium(selenium):
    selenium.implicitly_wait(10)
    return selenium


@pytest.fixture
def logged_in(base_url, selenium, user):
    selenium.get(base_url)
    selenium.delete_all_cookies()
    selenium.add_cookie({
        'name': user['session_cookie']['name'],
        'value': user['session_cookie']['value'],
        'path': '/',
        'domain': urlparse.urlsplit(base_url).hostname,
        'secure': True})

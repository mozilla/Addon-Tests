#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import py
import pytest


def pytest_runtest_setup(item):
    pytest_mozwebqa = py.test.config.pluginmanager.getplugin("mozwebqa")
    pytest_mozwebqa.TestSetup.services_base_url = item.config.option.services_base_url


def pytest_addoption(parser):
    parser.addoption("--servicesbaseurl",
                     action="store",
                     dest='services_base_url',
                     metavar='str',
                     default="",
                     help="specify the api url")


def pytest_funcarg__mozwebqa(request):
    pytest_mozwebqa = py.test.config.pluginmanager.getplugin("mozwebqa")
    return pytest_mozwebqa.TestSetup(request)


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

#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import mozwebqa


def pytest_runtest_setup(item):
    mozwebqa.TestSetup.api_base_url = item.config.option.api_base_url


def pytest_addoption(parser):
    parser.addoption("--apibaseurl",
                     action="store",
                     dest='api_base_url',
                     metavar='str',
                     default="https://addons-dev.allizom.org",
                     help="specify the api url")


def pytest_funcarg__mozwebqa(request):
    return mozwebqa.TestSetup(request)

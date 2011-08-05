#!/usr/bin/env python
#
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
# Contributor(s): Dave Hunt <dhunt@mozilla.com>
#                 Bebe <florin.strugariu@softvision.ro>
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

import json

import pytest
import py
from selenium import selenium


def pytest_runtest_setup(item):
    item.host = item.config.option.host
    item.port = item.config.option.port
    item.browser_name = item.config.option.browser_name
    item.browser_version = item.config.option.browser_version
    item.platform = item.config.option.platform
    TestSetup.base_url = item.config.option.base_url
    TestSetup.timeout = item.config.option.timeout
    TestSetup.credentials = item.config.option.credentialsfile
    item.sauce_labs_username = item.config.option.sauce_labs_username
    item.sauce_labs_api = item.config.option.sauce_labs_api

    TestSetup.site_version = 'impala' in item.keywords and '/i' or ''

    if not 'skip_selenium' in item.keywords:
        TestSetup.skip_selenium = False
        if item.sauce_labs_username:
            TestSetup.selenium = selenium('ondemand.saucelabs.com', '80',
                                          json.dumps({
                                            'username': item.sauce_labs_username,
                                            'access-key':  item.sauce_labs_api,
                                            'os': item.platform,
                                            'browser': item.browser_name,
                                            'browser-version': item.browser_version,
                                            'name': item.keywords.keys()[0],
                                            'public': True,
                                            'tags': ['amo']}),
                                          TestSetup.base_url)
        else:
            TestSetup.selenium = selenium(item.host, item.port, item.browser_name, TestSetup.base_url)

        if item.config.option.capturenetwork:
            TestSetup.selenium.start("captureNetworkTraffic=true")
        else:
            TestSetup.selenium.start()

        TestSetup.selenium.set_timeout(TestSetup.timeout)
    else:
        TestSetup.skip_selenium = True


def pytest_runtest_teardown(item):
    if not TestSetup.skip_selenium:
        if item.config.option.capturenetwork:
            traffic = TestSetup.selenium.captureNetworkTraffic("json")
            filename = item.keywords.keys()[0]
            f = open("%s.json" % filename, "w")
            f.write(traffic)
            f.close()

        TestSetup.selenium.stop()


def pytest_funcarg__testsetup(request):
    return TestSetup(request)


def pytest_addoption(parser):
    parser.addoption("--host",
                     action="store",
                     default="localhost",
                     help="host that Selenium server is listening on")
    parser.addoption("--port",
                     action="store",
                     default="4444",
                     help="port that Selenium server is listening on")
    parser.addoption("--browser-name",
                     action="store",
                     dest="browser_name",
                     help="target browser")
    parser.addoption("--browser-version",
                     action="store",
                     dest="browser_version",
                     help="target browser version")
    parser.addoption("--platform",
                     action="store",
                     help="target platform")
    parser.addoption("--base-url",
                     action="store",
                     dest="base_url",
                     default="http://addons.allizom.org",
                     help="base URL for the application under test")
    parser.addoption("--timeout",
                     action="store",
                     type="int",
                     default=120000,
                     help="timeout for page loads, etc")
    parser.addoption("--capturenetwork",
                     action="store_true",
                     default=False,
                     help="tells the Selenium server to capture the network traffic. this will store the results in test_method_name.json")
    parser.addoption("--sauce-labs-username",
                     action="store",
                     dest="sauce_labs_username",
                     help="sauce labs username")
    parser.addoption("--sauce-labs-api",
                     action="store",
                     dest="sauce_labs_api",
                     help="sauce labs api key")
    parser.addoption("--credentialsfile",
                     action="store",
                     default="credentials.yaml",
                     help="provide the credentials filename")


class TestSetup:
    def __init__(self, request):
        self.request = request

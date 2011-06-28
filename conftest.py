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

import pytest
import py
from selenium import selenium


def pytest_runtest_setup(item):
    item.host = item.config.option.hub
    item.browser = item.config.option.browser
    item.port = item.config.option.port
    TestSetup.base_url = item.config.option.site
    TestSetup.timeout = item.config.option.timeout

    if not 'skip_selenium' in item.keywords:
        TestSetup.skip_selenium = False
        TestSetup.selenium = selenium(item.host, item.port,
            item.browser, TestSetup.base_url)
         
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
    parser.addoption("--hub", action="store", default="localhost",
        help="specify where to run")
    parser.addoption("--port", action="store", default="4444",
        help="specify where to run")
    parser.addoption("--browser", action="store", default="*firefox",
        help="specify the browser")
    parser.addoption("--site", action="store", default="http://addons.allizom.org",
        help="specify the AUT")
    parser.addoption("--timeout", action="store", default=120000,
        help="specify the timeout")
    parser.addoption("--capturenetwork", action="store_true", default=False,
        help="tells the Selenium server to capture the network traffic. this will store the results in test_method_name.json")


class TestSetup:
    def __init__(self, request):
        self.request = request

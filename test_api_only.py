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
# Contributor(s): Marlena Compton <mcompton@mozilla.com>
#                 Teodosia Pop <teodosia.pop@softvision.ro>
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

from addons_api import AddOnsAPI
from unittestzero import Assert
import pytest

#These tests should only call the api.
#There should be no tests requiring selenium in this class.


@pytest.mark.skip_selenium
class TestAPIOnlyTests:

    def test_that_firebug_is_listed_first_in_addons_search_for_fire(self, mozwebqa):
        """TestCase for Litmus 15314"""
        addons_xml = AddOnsAPI(mozwebqa, 'fire')
        Assert.equal("Firebug", addons_xml.get_name_of_first_addon())

    def test_that_firebug_is_listed_first_in_addons_search_for_firebug(self, mozwebqa):
        """TestCase for Litmus 15316"""
        addons_xml = AddOnsAPI(mozwebqa)
        Assert.equal("Firebug", addons_xml.get_name_of_first_addon())

    def test_that_firebug_addon_type_name_is_extension(self, mozwebqa):
        """Testcase for Litmus 15316"""
        addons_xml = AddOnsAPI(mozwebqa)
        Assert.equal("Extension", addons_xml.get_addon_type_name("Firebug"))

    def test_that_firebug_addon_type_id_is_1(self, mozwebqa):
        """Testcase for Litmus 15316"""
        addon_xml = AddOnsAPI(mozwebqa)
        Assert.equal("1", addon_xml.get_addon_type_id("Firebug"))

    def test_firebug_version_number(self, mozwebqa):
        """Testcase for Litmus 15317"""
        addon_xml = AddOnsAPI(mozwebqa)
        Assert.equal("1.8.1", addon_xml.get_addon_version_number("Firebug"))

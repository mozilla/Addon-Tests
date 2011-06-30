#!/usr/bin/env python
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
# Contributor(s): Bebe <florin.strugariu@softvision.ro>
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

from unittestzero import Assert
import pytest
from addons_site import AddonsDetailsPage
xfail = pytest.mark.xfail


class TestAddonDetails:

    def test_other_addons_dropdown(self, testsetup):
        """
        Litmus 11926
        https://litmus.mozilla.org/show_test.cgi?id=11926
        """
        amo_detail_page = AddonsDetailsPage(testsetup, 'firebug')

        Assert.true(len(amo_detail_page.authors) > 1)
        Assert.true(amo_detail_page.other_addons_by_authors_text.endswith('these authors'))

        addons = amo_detail_page.other_addons_dropdown_values
        for i in range(len(addons) - 1, 0, -1): # Not checking the first item in the drop-down https://bugzilla.mozilla.org/show_bug.cgi?id=660706
            amo_detail_page.select_other_addons_dropdown_value(addons[i])
            Assert.true(amo_detail_page.name.startswith(addons[i].rstrip('.')))
            AddonsDetailsPage(testsetup, 'firebug')

    def test_other_addons_links(self, testsetup):
        """
        Litmus 11926
        https://litmus.mozilla.org/show_test.cgi?id=1192"""

        amo_detail_page = AddonsDetailsPage(testsetup, 'adblock-plus')

        Assert.equal(len(amo_detail_page.authors), 1)
        Assert.true(amo_detail_page.other_addons_by_authors_text.endswith(amo_detail_page.authors[0]))

        addons = amo_detail_page.other_addos_link_list()

        for i in range(amo_detail_page.other_addons_link_list_count):
            amo_detail_page.other_addons_link_list_click(addons[i])
            Assert.true(amo_detail_page.name.startswith(addons[i].rstrip('.')))
            AddonsDetailsPage(testsetup, 'adblock-plus')

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
# Contributor(s): Joel Andersson <janderssn@gmail.com>
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
from addons_site import AddonsHomePage, AddonsPersonasPage


class TestPersonas:

    def test_that_personas_is_listed_as_a_category(self, testsetup):
        """ Test for Litmus 9589
            https://litmus.mozilla.org/show_test.cgi?id=9589"""
        amo_home_page = AddonsHomePage(testsetup)
        Assert.true(amo_home_page.has_category(AddonsPersonasPage._category_name))

    def test_page_title_for_personas_landing_page(self, testsetup):
        """ Test for Litmus 15391
            https://litmus.mozilla.org/show_test.cgi?id=15391"""
        amo_home_page = AddonsHomePage(testsetup)
        amo_personas_page = amo_home_page.click_personas()
        Assert.true(amo_personas_page.is_the_current_page)

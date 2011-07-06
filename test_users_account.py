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
import addons_site
import addons_user_page


class TestAccounts:

    def test_user_can_login_and_logout(self, testsetup):
        """ Test for litmus 7857
            https://litmus.mozilla.org/show_test.cgi?id=7857
            Test for litmus 4859
            https://litmus.mozilla.org/show_test.cgi?id=4859
        """

        amo_home_page = addons_site.AddonsHomePage(testsetup)
        credentials = amo_home_page.credentials_of_user('default')

        Assert.false(amo_home_page.header.is_user_logged_in)
        addons_login_page = amo_home_page.header.click_login()

        addons_login_page.login(credentials['email'], credentials['password'])
        Assert.true(amo_home_page.header.is_user_logged_in)
        amo_home_page.header.click_logout()

        Assert.false(amo_home_page.header.is_user_logged_in)

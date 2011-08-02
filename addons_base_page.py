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

from page import Page


class AddonsBasePage(Page):

    def credentials_of_user(self, user):
        return self.parse_yaml_file(self.credentials)[user]

    @property
    def header(self):
        return AddonsBasePage.HeaderRegion(self.testsetup)

    class HeaderRegion(Page):

        _other_apps_locator = "id=other-apps"

        #Not LogedIn
        _login_locator = "css=.amo-header .context a:nth(1)"  # Until https://bugzilla.mozilla.org/show_bug.cgi?id=669646
        _register_locator = "css=.amo-header .context a:nth(0)"

        #LogedIn
        _account_controller_locator = 'css=#aux-nav .account .controller'
        _dropdown_locator = "css=#aux-nav .account ul"

        @property
        def other_applications_tooltip(self):
            return self.selenium.get_attribute("%s@title" % self._other_apps_locator)

        def click_my_account(self):
            self.selenium.click(self._account_controller_locator)
            self.wait_for_element_visible(self._dropdown_locator)

        def click_login(self):
            self.selenium.click(self._login_locator)
            self.selenium.wait_for_page_to_load(self.timeout)

        def click_logout(self):
            self.click_my_account()
            if self.selenium.get_text('%s > li:nth(3) a' % self._dropdown_locator) == "Log out":  # Until the https://bugzilla.mozilla.org/show_bug.cgi?id=669650
                self.selenium.click('%s > li:nth(3) a' % self._dropdown_locator)
            else:
                self.selenium.click('%s > li:nth(4) a' % self._dropdown_locator)
            self.selenium.wait_for_page_to_load(self.timeout)

        @property
        def is_user_logged_in(self):
            try:
                return self.selenium.is_visible(self._account_controller_locator)
            except:
                pass
            return False

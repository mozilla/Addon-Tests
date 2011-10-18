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
#                 Alex Lakatos <alex@greensqr.com>
#                 Teodosia Pop <teodosia.pop@softvision.ro>
#
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

from pages.home import HomePage


class TestAmoLayout:

    def test_other_applications_thunderbird(self, mozwebqa):
        """ Test for litmus 5037
            https://litmus.mozilla.org/show_test.cgi?id=5037
        """

        home_page = HomePage(mozwebqa)

        home_page.header.click_other_applications()
        home_page.header.click_thunderbird()
        Assert.true("thunderbird" in home_page.get_url_current_page())

        home_page.header.click_other_applications()
        Assert.false(home_page.header.is_thunderbird_visible())

    def test_that_checks_the_tooltip_for_amo_logo(self, mozwebqa):
        """
        Litmus 22924
        https://litmus.mozilla.org/show_test.cgi?id=22924
        """
        home_page = HomePage(mozwebqa)
        Assert.true(home_page.is_amo_logo_visible)
        Assert.equal(home_page.amo_logo_title, "Return to the Firefox Add-ons homepage")

    def test_that_checks_the_image_for_amo_logo(self, mozwebqa):
        """
        Litmus 25742
        https://litmus.mozilla.org/show_test.cgi?id=25742
        """
        home_page = HomePage(mozwebqa)
        Assert.true(home_page.is_amo_logo_image_visible)
        Assert.contains("-cdn.allizom.org/media/img/app-icons/med/firefox.png", home_page.amo_logo_image_source)

    def test_that_clicking_mozilla_logo_loads_mozilla_dot_org(self, mozwebqa):
        """
        Litmus 22922
        https://litmus.mozilla.org/show_test.cgi?id=22922
        """
        home_page = HomePage(mozwebqa)
        Assert.true(home_page.is_mozilla_logo_visible)
        home_page.click_mozilla_logo()
        Assert.equal(home_page.get_url_current_page(), "http://www.mozilla.org/")

    def test_that_other_applications_link_has_tooltip(self, mozwebqa):
        """ Litmus 22925
            https://litmus.mozilla.org/show_test.cgi?id=29698 """
        home_page = HomePage(mozwebqa)
        tooltip = home_page.get_title_of_link('Other applications')
        Assert.equal(tooltip, 'Find add-ons for other applications')

    #TODO: Add a method to check the mouse hover on "Other Applications" link after the hover issue is fixed
    def test_the_applications_listed_in_other_applications(self, mozwebqa):
        """
        Test for Litmus 25740
        https://litmus.mozilla.org/show_test.cgi?id=25740
        """
        expected_apps = [
            "Thunderbird",
            "Mobile",
            "SeaMonkey",
            "Sunbird"]
        home_page = HomePage(mozwebqa)
        other_apps = home_page.header.other_applications

        for app in other_apps:
            Assert.contains(app.name, expected_apps[app.index])
            Assert.true(app.is_application_visible)

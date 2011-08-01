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


import random
import pytest
xfail = pytest.mark.xfail

from unittestzero import Assert
from addons_site import AddonsHomePage
from addons_site import AddonsPersonasPage


class TestPersonas:

    def test_that_personas_is_listed_as_a_category(self, testsetup):
        """ Test for Litmus 9589
            https://litmus.mozilla.org/show_test.cgi?id=9589"""
        amo_home_page = AddonsHomePage(testsetup)
        Assert.true(amo_home_page.has_category("Personas"))

    def test_start_exploring_link_in_the_promo_box(self, testsetup):
        """ Test for Litmus 12037
            https://litmus.mozilla.org/show_test.cgi?id=12037"""
        amo_home_page = AddonsHomePage(testsetup)
        amo_personas_page = amo_home_page.click_personas()
        Assert.true(amo_personas_page.is_the_current_page)
        Assert.true(amo_personas_page.is_featured_addons_present)
        browse_personas_page = amo_personas_page.click_start_exploring()
        Assert.true(browse_personas_page.is_the_current_page)
        Assert.equal("up-and-coming", browse_personas_page.sort_key)
        Assert.equal("Up & Coming", browse_personas_page.sort_by)

    def test_page_title_for_personas_landing_page(self, testsetup):
        """ Test for Litmus 15391
            https://litmus.mozilla.org/show_test.cgi?id=15391"""
        amo_home_page = AddonsHomePage(testsetup)
        amo_personas_page = amo_home_page.click_personas()
        Assert.true(amo_personas_page.is_the_current_page)

    @xfail(reason="Disabled until bug 674374 is fixed.")
    def test_the_featured_personas_section(self, testsetup):
        """ Test for Litmus 15392
            https://litmus.mozilla.org/show_test.cgi?id=15392"""
        amo_home_page = AddonsHomePage(testsetup)
        amo_personas_page = amo_home_page.click_personas()
        Assert.true(amo_personas_page.is_the_current_page)
        Assert.equal(6, amo_personas_page.featured_personas_count)

    def test_the_recently_added_section(self, testsetup):
        """ Test for Litmus 15393
            https://litmus.mozilla.org/show_test.cgi?id=15393"""
        amo_home_page = AddonsHomePage(testsetup)
        amo_personas_page = amo_home_page.click_personas()
        Assert.true(amo_personas_page.is_the_current_page)
        Assert.equal(6, amo_personas_page.recently_added_count)
        recently_added_dates = amo_personas_page.recently_added_dates
        Assert.is_sorted_descending(recently_added_dates)

    def test_the_most_popular_section(self, testsetup):
        """ Test for Litmus 15394
            https://litmus.mozilla.org/show_test.cgi?id=15394"""
        amo_home_page = AddonsHomePage(testsetup)
        amo_personas_page = amo_home_page.click_personas()
        Assert.true(amo_personas_page.is_the_current_page)
        Assert.equal(6, amo_personas_page.most_popular_count)
        downloads = amo_personas_page.most_popular_downloads
        Assert.is_sorted_descending(downloads)

    def test_the_top_rated_section(self, testsetup):
        """ Test for Litmus 15395
            https://litmus.mozilla.org/show_test.cgi?id=15395"""
        amo_home_page = AddonsHomePage(testsetup)
        amo_personas_page = amo_home_page.click_personas()
        Assert.true(amo_personas_page.is_the_current_page)
        Assert.equal(6, amo_personas_page.top_rated_count)
        ratings = amo_personas_page.top_rated_ratings
        Assert.is_sorted_descending(ratings)

    def test_breadcrumb_menu_in_persona_details_page(self, testsetup):
        """ Test for Litmus 12046
            https://litmus.mozilla.org/show_test.cgi?id=12046"""

        # Step 1, 2: Access AMO Homepage, Click on Persona category link.
        amo_home_page = AddonsHomePage(testsetup)
        amo_personas_page = amo_home_page.click_personas()
        Assert.true(amo_personas_page.is_the_current_page)

        # Step 3: Click on any persona.
        random_persona_index = random.randint(1, amo_personas_page.persona_count)
        print 'random_persona_index: %s' % str(random_persona_index)
        amo_personas_detail_page = amo_personas_page.click_persona(random_persona_index)
        print 'url_current_page:     %s' % str(amo_personas_detail_page.get_url_current_page())
        Assert.true(amo_personas_detail_page.is_the_current_page)

        # Verify breadcrumb menu format, i.e. Add-ons for Firefox > Personas > {Persona Name}.
        persona_title = amo_personas_detail_page.personas_title
        Assert.equal("Add-ons for Firefox", amo_personas_detail_page.get_breadcrumb_item_text(1))
        Assert.equal("Personas", amo_personas_detail_page.get_breadcrumb_item_text(2))
        Assert.equal(persona_title, amo_personas_detail_page.get_breadcrumb_item_text(3))

        # Step 4: Click on the links present in the Breadcrumb menu.
        # Verify that the Personas link loads the Personas home page.
        amo_personas_detail_page.click_breadcrumb_item("Personas")
        Assert.true(amo_personas_page.is_the_current_page)

        amo_personas_page.return_to_previous_page()
        Assert.true(amo_personas_detail_page.is_the_current_page)

        # Verify that the Add-ons for Firefox link loads the AMO home page.
        amo_personas_detail_page.click_breadcrumb_item("Add-ons for Firefox")
        Assert.true(amo_home_page.is_the_current_page)

    def test_breadcrumb_menu_for_rainbow_firefox_persona(self, testsetup):
        """ Verify the breadcrumb menu for a known persona.
            https://preview.addons.mozilla.org/en-us/firefox/addon/rainbow-firefox/"""
        amo_personas_page = AddonsPersonasPage(testsetup)
        rainbow_personas_detail_page = amo_personas_page.open_persona_detail_page("rainbow-firefox")
        Assert.equal("rainbow firefox", rainbow_personas_detail_page.personas_title)
        Assert.equal("Add-ons for Firefox", rainbow_personas_detail_page.get_breadcrumb_item_text(1))
        Assert.equal("Personas", rainbow_personas_detail_page.get_breadcrumb_item_text(2))
        Assert.equal("rainbow firefox", rainbow_personas_detail_page.get_breadcrumb_item_text(3))

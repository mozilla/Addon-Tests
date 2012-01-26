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
#                 Alin Trif <alin.trif@softvision.ro>
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

from unittestzero import Assert

from pages.home import Home
from pages.personas import Personas

xfail = pytest.mark.xfail
nondestructive = pytest.mark.nondestructive


class TestPersonas:

    @xfail(reason="disabled until Selenium issue http://code.google.com/p/selenium/issues/detail?id=3182 is fixed")
    @nondestructive
    def test_start_exploring_link_in_the_promo_box(self, mozwebqa):
        """
        Test for Litmus 12037.
        https://litmus.mozilla.org/show_test.cgi?id=12037
        """
        home_page = Home(mozwebqa)
        personas_page = home_page.header.application_masthead("Personas").click()
        Assert.true(personas_page.is_the_current_page)
        Assert.true(personas_page.is_featured_addons_present)
        browse_personas_page = personas_page.click_start_exploring()
        Assert.true(browse_personas_page.is_the_current_page)
        Assert.equal("up-and-coming", browse_personas_page.sort_key)
        Assert.equal("Up & Coming", browse_personas_page.sort_by)

    @nondestructive
    def test_page_title_for_personas_landing_page(self, mozwebqa):
        """
        Test for Litmus 15391.
        https://litmus.mozilla.org/show_test.cgi?id=15391
        """
        home_page = Home(mozwebqa)
        personas_page = home_page.header.application_masthead("Personas").click()
        Assert.true(personas_page.is_the_current_page)

    @nondestructive
    def test_the_featured_personas_section(self, mozwebqa):
        """
        Test for Litmus 15392.
        https://litmus.mozilla.org/show_test.cgi?id=15392
        """
        home_page = Home(mozwebqa)
        personas_page = home_page.header.application_masthead("Personas").click()
        Assert.true(personas_page.is_the_current_page)
        Assert.equal(6, personas_page.featured_personas_count)

    @nondestructive
    def test_the_recently_added_section(self, mozwebqa):
        """
        Test for Litmus Litmus 15393.
        https://litmus.mozilla.org/show_test.cgi?id=15393
        """
        home_page = Home(mozwebqa)
        personas_page = home_page.header.application_masthead("Personas").click()
        Assert.true(personas_page.is_the_current_page)
        Assert.equal(6, personas_page.recently_added_count)
        recently_added_dates = personas_page.recently_added_dates
        Assert.is_sorted_descending(recently_added_dates)

    @nondestructive
    def test_the_most_popular_section(self, mozwebqa):
        """
        Test for Litmus 15394.
        https://litmus.mozilla.org/show_test.cgi?id=15394
        """
        home_page = Home(mozwebqa)
        personas_page = home_page.header.application_masthead("Personas").click()
        Assert.true(personas_page.is_the_current_page)
        Assert.equal(6, personas_page.most_popular_count)
        downloads = personas_page.most_popular_downloads
        Assert.is_sorted_descending(downloads)

    @nondestructive
    def test_the_top_rated_section(self, mozwebqa):
        """
        Test for Litmus 15395.
        https://litmus.mozilla.org/show_test.cgi?id=15395
        """
        home_page = Home(mozwebqa)
        personas_page = home_page.header.application_masthead("Personas").click()
        Assert.true(personas_page.is_the_current_page)
        Assert.equal(6, personas_page.top_rated_count)
        ratings = personas_page.top_rated_ratings
        Assert.is_sorted_descending(ratings)

    @nondestructive
    def test_breadcrumb_menu_in_persona_details_page(self, mozwebqa):
        """
        Test for Litmus Litmus 12046.
        https://litmus.mozilla.org/show_test.cgi?id=12046
        """

        # Step 1, 2: Access AMO Home, Click on Persona category link.
        home_page = Home(mozwebqa)
        personas_page = home_page.header.application_masthead("Personas").click()
        Assert.true(personas_page.is_the_current_page)

        # Step 3: Click on any persona.
        random_persona_index = random.randint(1, personas_page.persona_count)

        personas_detail_page = personas_page.click_persona(random_persona_index)
        Assert.true(personas_detail_page.is_the_current_page)

        # Verify breadcrumb menu format, i.e. Add-ons for Firefox > Personas > {Persona Name}.
        persona_title = personas_detail_page.title
        Assert.equal("Add-ons for Firefox", personas_detail_page.breadcrumbs[0].text)
        Assert.equal("Personas", personas_detail_page.breadcrumbs[1].text)

        persona_breadcrumb_title = len(persona_title) > 40 and '%s...' % persona_title[:40] or persona_title

        Assert.equal(personas_detail_page.breadcrumbs[2].text, persona_breadcrumb_title)

        # Step 4: Click on the links present in the Breadcrumb menu.
        # Verify that the Personas link loads the Personas home page.
        personas_detail_page.breadcrumbs[1].click()
        Assert.true(personas_page.is_the_current_page)

        personas_page.return_to_previous_page()
        Assert.true(personas_detail_page.is_the_current_page)

        # Verify that the Add-ons for Firefox link loads the AMO home page.
        personas_detail_page.breadcrumbs[0].click()
        Assert.true(home_page.is_the_current_page)

    @nondestructive
    def test_breadcrumb_menu_for_rainbow_firefox_persona(self, mozwebqa):
        """
        Verify the breadcrumb menu for a known persona.
        https://preview.addons.mozilla.org/en-us/firefox/addon/rainbow-firefox/
        """
        personas_page = Personas(mozwebqa)
        rainbow_personas_detail_page = personas_page.open_persona_detail_page("rainbow-firefox")
        Assert.equal("rainbow firefox", rainbow_personas_detail_page.title)
        Assert.equal("Add-ons for Firefox", rainbow_personas_detail_page.breadcrumbs[0].text)
        Assert.equal("Personas", rainbow_personas_detail_page.breadcrumbs[1].text)
        Assert.equal("rainbow firefox", rainbow_personas_detail_page.breadcrumbs[2].text)

    @nondestructive
    def test_personas_breadcrumb_format(self, mozwebqa):
        """
        Verify the breadcrumb format in personas page
        https://litmus.mozilla.org/show_test.cgi?id=12034
        """
        home_page = Home(mozwebqa)

        personas_page = home_page.header.application_masthead("Personas").click()
        Assert.equal(personas_page.breadcrumbs[0].text, 'Add-ons for Firefox')
        Assert.equal(personas_page.breadcrumbs[1].text, 'Personas')

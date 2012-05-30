#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import random
import pytest

from unittestzero import Assert

from pages.desktop.home import Home
from pages.desktop.personas import Personas


class TestPersonas:

    @pytest.mark.nondestructive
    def test_start_exploring_link_in_the_promo_box(self, mozwebqa):
        """
        Test for Litmus 12037.
        https://litmus.mozilla.org/show_test.cgi?id=12037
        """
        home_page = Home(mozwebqa)
        personas_page = home_page.header.site_navigation_menu("Personas").click()
        Assert.true(personas_page.is_the_current_page)
        Assert.true(personas_page.is_featured_addons_present)
        browse_personas_page = personas_page.click_start_exploring()
        Assert.true(browse_personas_page.is_the_current_page)
        Assert.equal("up-and-coming", browse_personas_page.sort_key)
        Assert.equal("Up & Coming", browse_personas_page.sort_by)

    @pytest.mark.nondestructive
    def test_page_title_for_personas_landing_page(self, mozwebqa):
        """
        Test for Litmus 15391.
        https://litmus.mozilla.org/show_test.cgi?id=15391
        """
        home_page = Home(mozwebqa)
        personas_page = home_page.header.site_navigation_menu("Personas").click()
        Assert.true(personas_page.is_the_current_page)

    @pytest.mark.smoke
    @pytest.mark.nondestructive
    def test_the_featured_personas_section(self, mozwebqa):
        """
        Test for Litmus 15392.
        https://litmus.mozilla.org/show_test.cgi?id=15392
        """
        home_page = Home(mozwebqa)
        personas_page = home_page.header.site_navigation_menu("Personas").click()
        Assert.true(personas_page.is_the_current_page)
        Assert.less_equal(personas_page.featured_personas_count, 6)

    @pytest.mark.smoke
    @pytest.mark.nondestructive
    def test_the_recently_added_section(self, mozwebqa):
        """
        Test for Litmus Litmus 15393.
        https://litmus.mozilla.org/show_test.cgi?id=15393
        """
        home_page = Home(mozwebqa)
        personas_page = home_page.header.site_navigation_menu("Personas").click()
        Assert.true(personas_page.is_the_current_page)
        Assert.equal(6, personas_page.recently_added_count)
        recently_added_dates = personas_page.recently_added_dates
        Assert.is_sorted_descending(recently_added_dates)

    @pytest.mark.smoke
    @pytest.mark.nondestructive
    def test_the_most_popular_section(self, mozwebqa):
        """
        Test for Litmus 15394.
        https://litmus.mozilla.org/show_test.cgi?id=15394
        """
        home_page = Home(mozwebqa)
        personas_page = home_page.header.site_navigation_menu("Personas").click()
        Assert.true(personas_page.is_the_current_page)
        Assert.equal(6, personas_page.most_popular_count)
        downloads = personas_page.most_popular_downloads
        Assert.is_sorted_descending(downloads)

    @pytest.mark.nondestructive
    def test_the_top_rated_section(self, mozwebqa):
        """
        Test for Litmus 15395.
        https://litmus.mozilla.org/show_test.cgi?id=15395
        """
        home_page = Home(mozwebqa)
        personas_page = home_page.header.site_navigation_menu("Personas").click()
        Assert.true(personas_page.is_the_current_page)
        Assert.equal(6, personas_page.top_rated_count)
        ratings = personas_page.top_rated_ratings
        Assert.is_sorted_descending(ratings)

    @pytest.mark.nondestructive
    def test_breadcrumb_menu_in_persona_details_page(self, mozwebqa):
        """
        Test for Litmus Litmus 12046.
        https://litmus.mozilla.org/show_test.cgi?id=12046
        """

        # Step 1, 2: Access AMO Home, Click on Persona category link.
        home_page = Home(mozwebqa)
        personas_page = home_page.header.site_navigation_menu("Personas").click()
        Assert.true(personas_page.is_the_current_page)

        # Step 3: Click on any persona.
        random_persona_index = random.randint(0, personas_page.persona_count - 1)

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

    @pytest.mark.nondestructive
    def test_personas_breadcrumb_format(self, mozwebqa):
        """
        Verify the breadcrumb format in personas page
        https://litmus.mozilla.org/show_test.cgi?id=12034
        """
        home_page = Home(mozwebqa)

        personas_page = home_page.header.site_navigation_menu("Personas").click()
        Assert.equal(personas_page.breadcrumbs[0].text, 'Add-ons for Firefox')
        Assert.equal(personas_page.breadcrumbs[1].text, 'Personas')

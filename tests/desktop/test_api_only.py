# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest


from pages.desktop.addons_api import AddonsAPI

# These tests should only call the api.
# There should be no tests requiring selenium in this class.


class TestAPIOnlyTests:

    @pytest.mark.nondestructive
    def test_that_firebug_is_listed_first_in_addons_search_for_firebug(self, base_url):
        response = AddonsAPI(base_url, 'Firebug')
        assert 'firebug' == response.get_addon_name()

    @pytest.mark.nondestructive
    def test_that_firebug_addon_type_name_is_extension(self, base_url):
        response = AddonsAPI(base_url, 'Firebug')
        assert 'extension' == response.get_addon_type()

    @pytest.mark.nondestructive
    def test_that_firebug_addon_type_id_is_1(self, base_url):
        response = AddonsAPI(base_url, 'Firebug')
        assert 1 == response.get_addon_type_id()

    @pytest.mark.nondestructive
    def test_that_firebug_status_id_is_4_and_fully_reviewed(self, base_url):
        response = AddonsAPI(base_url, 'Firebug')
        assert 4 == response.get_addon_status_id()
        assert 'fully reviewed' == response.get_addon_status()

    @pytest.mark.nondestructive
    def test_that_firebug_has_install_link(self, base_url):
        response = AddonsAPI(base_url, 'Firebug')
        assert 'fx.xpi?src=api' in response.get_install_link()

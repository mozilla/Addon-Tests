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
# Contributor(s): Alin Trif <alin.trif@softvision.ro>
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

import pytest

from unittestzero import Assert
from pages.home import Home

nondestructive = pytest.mark.nondestructive


class TestExtensions:

    @nondestructive
    def test_featured_tab_is_highlighted_by_default(self, mozwebqa):
        """
        Litmus 29706
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=29706
        """
        home_page = Home(mozwebqa)
        featured_extensions_page = home_page.header.application_masthead("Extensions").click()
        Assert.equal(featured_extensions_page.default_selected_tab, "Featured")

    @nondestructive
    def test_next_button_is_disabled_on_the_last_page(self, mozwebqa):
        """
        Litmus 29710
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=29710
        """
        home_page = Home(mozwebqa)
        featured_extensions_page = home_page.header.application_masthead("Extensions").click()
        featured_extensions_page.sort_by('most_users')
        featured_extensions_page.paginator.click_last_page()

        Assert.true(featured_extensions_page.paginator.is_next_page_disabled, 'Next button is available')

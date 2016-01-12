# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.mobile.details import Details


class TestDetails:

    @pytest.mark.nondestructive
    def test_that_contribute_button_is_not_present_on_the_mobile_page(self, base_url, selenium):
        details_page = Details(base_url, selenium, 'MemChaser')
        assert details_page.is_the_current_page
        assert not details_page.is_contribute_button_present

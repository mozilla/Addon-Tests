# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pages.page import Page


class AddonItem(Page):

    def __init__(self, base_url, selenium, element):
        Page.__init__(self, base_url, selenium)
        self._root_element = element

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.desktop.base import Base


class Agreement(Base):

    _accept_agreement_locator = (By.ID, 'accept-agreement')

    def accept_agreement(self):
        from distribution import Distribution
        self.selenium.find_element(*self._accept_agreement_locator).click()
        return Distribution(self.base_url, self.selenium)

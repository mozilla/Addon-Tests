# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait

from pages.page import Page
from pages.desktop.base import Base


class Submit(Base):

    _select_a_file_locator = (By.ID, "upload-addon")

    def select_file(self, path):
        file_selector = self.selenium.find_element(*self._select_a_file_locator)
        file_selector.send_keys(path)

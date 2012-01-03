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
# Contributor(s): Sergey Tupchiy(tupchii.sergii@gmail.com)
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

import re

from selenium.webdriver.common.by import By

from pages.base import Base


class Statistics(Base):

    _title_locator = (By.CSS_SELECTOR, '.addon')
    _total_downloads_locator = (By.CSS_SELECTOR, '.island.two-up div:nth-child(1) a')
    _usage_locator = (By.CSS_SELECTOR, '.island.two-up div:nth-child(2) a')

    def __init__(self, testsetup, addon=None):
        #formats name for url
        Base.__init__(self, testsetup)
        if (addon != None):
            self.addon = addon.replace(" ", "-")
            self.addon = re.sub(r'[^A-Za-z0-9\-]', '', self.addon).lower()
            self.addon = self.addon[:27]
            self.selenium.get("%s/addon/%s/statistics" % (self.base_url, self.addon))

    @property
    def _page_title(self):
        return "%s :: Statistics Dashboard :: Add-ons for Firefox" % self.addon_name

    @property
    def addon_name(self):
        base = self.selenium.find_element(*self._title_locator).text
        return base.replace('Statistics for', '').strip()

    @property
    def total_downloads_number(self):
        return ''.join(re.findall("[0-9]", self.selenium.find_element(*self._total_downloads_locator).text))

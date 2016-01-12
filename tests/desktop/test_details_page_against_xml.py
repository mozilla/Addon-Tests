# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re
from urllib2 import urlparse

import pytest

from pages.desktop.details import Details
from pages.desktop.addons_api import AddonsAPI


class TestDetailsAgainstXML:

    firebug = "Firebug"

    @pytest.mark.nondestructive
    def test_that_firebug_page_title_is_correct(self, base_url, selenium):
        firebug_page = Details(base_url, selenium, self.firebug)
        assert re.search(self.firebug, firebug_page.page_title) is not None

    @pytest.mark.nondestructive
    def test_that_firebug_version_number_is_correct(self, base_url, selenium):
        firebug_page = Details(base_url, selenium, self.firebug)
        assert len(str(firebug_page.version_number)) > 0

    @pytest.mark.nondestructive
    def test_that_firebug_authors_is_correct(self, base_url, selenium):

        # get authors from browser
        firebug_page = Details(base_url, selenium, self.firebug)
        browser_authors = firebug_page.authors

        # get authors from xml
        addons_xml = AddonsAPI(base_url, self.firebug)
        xml_authors = addons_xml.get_list_of_addon_author_names()

        # check that both lists have the same number of authors
        assert len(browser_authors) == len(xml_authors)

        # cross check both lists with each other
        for i in range(len(xml_authors)):
            assert xml_authors[i] == browser_authors[i]

    @pytest.mark.nondestructive
    def test_that_firebug_images_is_correct(self, base_url, selenium):

        # get images links from browser
        firebug_page = Details(base_url, selenium, self.firebug)
        images_count = firebug_page.previewer.image_count
        browser_images = []
        for i in range(images_count):
            browser_images.append(firebug_page.previewer.image_link(i))

        # get images links from xml
        addons_xml = AddonsAPI(base_url, self.firebug)
        xml_images = addons_xml.get_list_of_addon_images_links()

        # check that both lists have the same number of images
        assert len(browser_images) == len(xml_images)

        # cross check both lists with each other
        for i in range(len(xml_images)):
            assert re.sub('src=api(&amp;|&)', '', xml_images[i]) == browser_images[i]

    @pytest.mark.nondestructive
    def test_that_firebug_summary_is_correct(self, base_url, selenium):
        # browser
        firebug_page = Details(base_url, selenium, self.firebug)
        browser_summary = firebug_page.summary

        # api
        addons_xml = AddonsAPI(base_url, self.firebug)
        xml_summary = addons_xml.get_addon_summary()

        assert xml_summary == browser_summary

    @pytest.mark.nondestructive
    def test_that_firebug_rating_is_correct(self, base_url, selenium):
        firebug_page = Details(base_url, selenium, self.firebug)
        assert '5' == firebug_page.rating

    @pytest.mark.nondestructive
    def test_that_description_text_is_correct(self, base_url, selenium):
        # browser
        firebug_page = Details(base_url, selenium, self.firebug)
        browser_description = firebug_page.description

        # api
        addons_xml = AddonsAPI(base_url, self.firebug)
        xml_description = addons_xml.get_addon_description()

        assert browser_description.replace('\n', '') == xml_description.replace('\n', '')

    @pytest.mark.nondestructive
    def test_that_icon_is_correct(self, base_url, selenium):
        # browser
        firebug_page = Details(base_url, selenium, self.firebug)
        browser_icon = firebug_page.icon_url

        # api
        addons_xml = AddonsAPI(base_url, self.firebug)
        xml_icon = addons_xml.get_icon_url()

        assert browser_icon == xml_icon

    @pytest.mark.nondestructive
    def test_that_support_url_is_correct(self, base_url, selenium):
        # browser
        firebug_page = Details(base_url, selenium, self.firebug)
        browser_support_url = firebug_page.support_url

        # api
        addons_xml = AddonsAPI(base_url, self.firebug)
        xml_support_url = addons_xml.get_support_url()

        assert browser_support_url == xml_support_url

    @pytest.mark.nondestructive
    def test_that_rating_in_api_equals_rating_in_details_page(self, base_url, selenium):
        # browser
        firebug_page = Details(base_url, selenium, self.firebug)
        browser_rating = firebug_page.rating

        # api
        addons_xml = AddonsAPI(base_url, self.firebug)
        xml_rating = addons_xml.get_rating()

        assert browser_rating == xml_rating

    @pytest.mark.nondestructive
    def test_that_compatible_applications_equal(self, base_url, selenium):
        # browser
        firebug_page = Details(base_url, selenium, self.firebug)
        firebug_page.expand_version_information()
        browser_compatible_applications = firebug_page.compatible_applications

        # api
        addons_xml = AddonsAPI(base_url, self.firebug)
        xml_compatible_applications = addons_xml.get_compatible_applications()
        name = xml_compatible_applications[0]
        min_version = xml_compatible_applications[1]
        max_version = xml_compatible_applications[2]

        # E.g.: Works with Firefox 1.0
        meta_compat_prefix = 'Works with %s %s ' % (name, min_version)
        # E.g.: Works with Firefox 1.0 and later
        meta_compat_abbrev = meta_compat_prefix + 'and later'
        # E.g.: Works with Firefox 1.0 - 16.0a1
        meta_compat_full = "%s- %s" % (meta_compat_prefix, max_version)

        assert (browser_compatible_applications == meta_compat_full or
                browser_compatible_applications == meta_compat_abbrev or
                browser_compatible_applications.startswith(meta_compat_prefix)
                ), "Listed compat. versions don't match versions listed in API."

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_addon_number_of_total_downloads_is_correct(self, base_url, selenium):
        # browser
        firebug_page = Details(base_url, selenium, self.firebug)
        statistics_page = firebug_page.click_view_statistics()
        browser_downloads = statistics_page.total_downloads_number

        # api
        addons_xml = AddonsAPI(base_url, self.firebug)
        xml_downloads = addons_xml.get_total_downloads()

        assert browser_downloads == xml_downloads

    @pytest.mark.nondestructive
    def test_that_learn_more_link_is_correct(self, base_url, selenium):
        # api
        addons_xml = AddonsAPI(base_url, self.firebug)
        learn_more_url = addons_xml.get_learn_more_url()

        # browser
        details_page = Details(base_url, selenium, self.firebug)
        details_page.get_url(learn_more_url)

        assert self.firebug in details_page.page_title

    @pytest.mark.nondestructive
    def test_that_firebug_devs_comments_is_correct(self, base_url, selenium):
        # browser
        firebug_page = Details(base_url, selenium, self.firebug)
        firebug_page.expand_devs_comments()
        browser_devs_comments = firebug_page.devs_comments_message

        # api
        addons_xml = AddonsAPI(base_url, self.firebug)
        xml_devs_comments = addons_xml.get_devs_comments()

        assert xml_devs_comments == browser_devs_comments

    @pytest.mark.nondestructive
    def test_that_home_page_in_api_equals_home_page_in_details_page(self, base_url, selenium):
        # browser
        firebug_page = Details(base_url, selenium, self.firebug)
        browser_home_page = urlparse.unquote(firebug_page.website)

        # api
        addons_xml = AddonsAPI(base_url, self.firebug)
        xml_home_page = addons_xml.get_home_page()

        assert xml_home_page in browser_home_page

    @pytest.mark.nondestructive
    def test_that_reviews_in_api_equals_reviews_in_details_page(self, base_url, selenium):
        # browser
        firebug_page = Details(base_url, selenium, self.firebug)
        browser_reviews = firebug_page.total_reviews_count

        # api
        addons_xml = AddonsAPI(base_url, self.firebug)
        xml_reviews = addons_xml.get_reviews_count()

        assert browser_reviews == xml_reviews

    @pytest.mark.nondestructive
    def test_that_daily_users_in_api_equals_daily_users_in_details_page(self, base_url, selenium):
        # browser
        firebug_page = Details(base_url, selenium, self.firebug)
        browser_daily_users = firebug_page.daily_users_number

        # api
        addons_xml = AddonsAPI(base_url, self.firebug)
        xml_daily_users = addons_xml.get_daily_users()

        assert browser_daily_users == xml_daily_users

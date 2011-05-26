from page import Page

class RefineResults(Page):

    _platforms_locator = "css=#refine-platform"
    _tags_locator = "css=#refine-tags"

    _list_locator = " ul li"

    @property
    def platform_count(self):
         return int(self.selenium.get_css_count(self._platforms_locator + self._list_locator))

    def platform(self, lookup):
        return self.Item(self.testsetup, self._platforms_locator, lookup)

    @property
    def tag_count(self):
        return int(self.selenium.get_css_count(self._tags_locator + self._list_locator))

    def tag(self, lookup):
        return self.Item(self.testsetup, self._tags_locator, lookup)

    def tags(self):
        return [self.Item(self.testsetup, self._tags_locator, i) for i in range(self.tag_count)]

    class Item(Page):

        _name_locator = " a"

        def __init__(self, testsetup, locator, lookup):
            Page.__init__(self, testsetup)
            self.lookup = lookup
            self.locator = locator

        def absolute_locator(self, relative_locator):
            return self.root_locator + relative_locator

        @property
        def root_locator(self):
            if type(self.lookup) == int:
                # lookup by index
                return "{0} ul li:nth({1})".format(self.locator, self.lookup)
            else:
                # lookup by name
                return "{0} ul li:contains({1})".format(self.locator, self.lookup)

        def click(self):
            self.selenium.click(self.absolute_locator(self._name_locator))
            self.selenium.wait_for_page_to_load(self.timeout)

        @property
        def name(self):
            return self.selenium.get_text(self.absolute_locator(self._name_locator))

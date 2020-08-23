from scrapy import Spider
from scrapy.shell import inspect_response

from ...settings import INSPECTED_URL_IN_SHELL


class JuwaiSpider(Spider):
    """A spider basic class

        Support:
            - Debug mode (enter scrapy shell)
            - Object stat

    """
    def __init__(self, *a, **kw):
        super(JuwaiSpider, self).__init__(*a, **kw)
        self.__obj_count_table = {}

    def _enter_debug_shell_by_url(self, response):
        """
            Enter into `Shell Mode` for debug
                if Inspected Url is contained in request URL.

            @param response: instance of Http Response
            @type response: scrapy.http.response

        """
        if INSPECTED_URL_IN_SHELL and INSPECTED_URL_IN_SHELL in response.url:
            inspect_response(response, self)

    def terminate(self, reason):
        """Quit scraping"""
        self.crawler.engine.close_spider(self, reason)
        self.print_stat()

    def assign_value_to_tag(self, tag: str, value):
        """Assign a value to a tag"""
        self.__obj_count_table[tag] = value

    def add_ref_count_by_tag(self, tag: str):
        """Add reference count for a stat tag"""
        value = self.__obj_count_table.get(tag)
        if value:
            self.__obj_count_table[tag] = value + 1
        else:
            self.__obj_count_table[tag] = 0

    def print_stat(self):
        """Print stat info."""
        print('*** Objects Count: ***')

        for k, v in self.__obj_count_table.items():
            print(
                'Object Name: {}  & Count: {}'.format(k, v)
            )

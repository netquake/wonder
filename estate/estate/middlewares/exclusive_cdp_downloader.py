from time import sleep
import sys

from scrapy import signals
from scrapy.http import HtmlResponse
from scrapy.http import Request

from jw import app
from ..utils.chrome_dev_client import ChromeBrowser
from ..utils.chrome_dev_client import ExclusiveTab


class ExclusiveCDPDownloaderMiddleware(object):
    """It's a `Sequential requests` sender for Scrapy,
            because it's based on 1 tab.

        1. Open browser
        2. New a tab of browser
        3. Send request from this tab

        *** Lock the `tab` for each tab. ***

    """
    def __init__(self, download_delay, valid_page_filter):
        self.__browser = ChromeBrowser(ExclusiveTab)
        self.__exclusive_tab = self.__browser.new_tab()
        self.__download_delay = download_delay
        self.__valid_page_filter = valid_page_filter

    @classmethod
    def from_crawler(cls, crawler):
        """Initialize the middleware with the crawler settings"""
        middleware = cls(
            crawler.settings['DOWNLOAD_DELAY'],
            crawler.settings['FILTER_METHOD_OBJ']
        )

        crawler.signals.connect(
            middleware.spider_closed, signals.spider_closed
        )

        return middleware

    def __response_retry(self, request):
        """Request again when get invalid page."""
        request = request.copy()

        retry_times = request.meta.get('retry_times', 0)
        request.dont_filter = True
        request.meta['retry_times'] = retry_times + 1

        return request

    def process_request(self, request, spider):
        """Process a request using the CDP"""
        if not isinstance(request, Request):
            return None

        html_response = self.__exclusive_tab.exclusive_request(
            request.url,
            download_delay=self.__download_delay,
            inject_js="""
            delete navigator.webdriver;
            delete navigator.__proto__.webdriver;
            UserActivation.defineProperty(
            navigator, 'userActivation', {hasBeenActive: true, isActive: true}
            );
            """
        )

        if not self.__valid_page_filter(html_response):
            app.logger.error(
                '........... get forbidden & retry again............'
            )
            app.logger.error(request.url)

            sleep(60*30)    # sleep 30 minutes

            return self.__response_retry(request)

        return HtmlResponse(
            request.url,
            body=html_response,
            encoding='utf-8',
            request=request,
            headers=request.headers.copy()
        )

    def spider_closed(self):
        """Maybe could Shutdown all tabs in browser here, like:

            self.__browser.close_all_tabs()
        """
        pass

"""
    Implement a exclusive tab class for `Chrome.Tab`

    Only 1 request could be activated on 1 tab when it's idle.

"""
from random import choice
from random import randrange
from threading import Lock
from time import sleep

from .basic_tab import ChromeBasicTab
from jw import app


class _RandomRequestInterval(object):
    """Sleep random time_t which based on `DOWNLOAD_DELAY`"""
    RANDOM_PERCENTAGE_TABLE_0 = (0.5, 1.8, 1.9, 0.9)
    RANDOM_PERCENTAGE_TABLE_1 = (0.1, 2, 1.8)
    RANDOM_PERCENTAGE_TABLE_2 = (1.2, 0.4, 0.9, 1.3)
    RANDOM_TABLE_ARRAY = (
        RANDOM_PERCENTAGE_TABLE_0,
        RANDOM_PERCENTAGE_TABLE_1,
        RANDOM_PERCENTAGE_TABLE_2
    )

    def delay(self, download_delay):
        """Cal. a random delay time_t with a percentage & sleep()"""
        if not download_delay:
            return

        PERCENTAGE_TABLE = self.RANDOM_TABLE_ARRAY[randrange(0, 3)]
        percent = choice(PERCENTAGE_TABLE)
        delay_time_t = download_delay * percent

        app.logger.info(
            ' *** download delay time_t: {} ***'.format(delay_time_t)
        )
        sleep(delay_time_t)


class ExclusiveTab(ChromeBasicTab):
    """Implement exclusive Request for 1 tab (thread safe)"""
    def __init__(self, tab):
        """Constructor

            @param tab: instance of Browser.Tab
            @type tab: object
        """
        super(ExclusiveTab, self).__init__(tab)
        self.__tab_req_resp_lock = Lock()
        self.__request_interval = _RandomRequestInterval()

    def _on_frame_stopped_loading(self, frameId):
        pass

    def _on_request_will_be_sent(self, **kwargs):
        pass

    def _on_response_received(self, **kwargs):
        pass

    def exclusive_request(
        self, uri, download_delay=0, inject_js=None, timeout=3
    ):
        """A exclusive request of a tab [Thread safe]:
            means cannot activate a new request before the last
                    request is completed.

            @param uri: Request URL
            @type uri: string
            @param download_delay: time to delay for each request
            @type download_delay: integer
            @param inject_js: javascript which will be inject into `DOM`
            @type inject_js: string
            @param timeout: timeout setting for request
            @type timeout: integer
            @return: response of http
            @rtype: string
        """
        with self.__tab_req_resp_lock:

            self.__request_interval.delay(download_delay)
            self._goto_uri(uri, timeout, inject_js)

            return self._get_html_response()

"""
    A wrapper for `Chrome.Browser` and always activate a Chrome(Dev)
        process while using it.

    Chrome DevTools Protocal (CDP) Doc:

        - https://developers.google.com/web/tools/chrome-devtools

    CDP is a kind of `Bridge` from Chrome(DevMode) for python.

    Website still could recognize the access comes from Dev Environment,
        not a normal Browser.


    Library supports:
        Python==3.8
        Scrapy==2.2.1
        pychrome==0.2.3
        SQLAlchemy==1.3.3
        git+ssh://git@github.com/juwai/python-config.git@master#egg=juwai_config
        git+ssh://git@github.com/juwai/python-logging.git@master#egg=juwai_logging
        zerorpc==0.6.1


    Usage:
        from browser import ChromeBrowser
        from exclusive_tab import ExclusiveTab

        with ChromeBrowser(ExclusiveTab) as br:
            tab = br.new_tab()

            print(
                tab.exclusive_request(
                    'https://www.abc.com'
                )
            )

"""
from contextlib import closing
import socket
from time import sleep

from pychrome import Browser
from pychrome import RuntimeException

from jw import app
from ...settings import START_DEVTOOL_CHROME_COMMAND


class _CDPPortDetector(object):
    """
    Telnet the CDP port & activate a chrome process if CDP port doesn't exist
    """
    def __init__(self, ip='127.0.0.1', port=9222):
        """Set ip & port of CDP Server of chrome"""
        self.__ip = ip
        self.__port = port

    def is_alive(self):
        """Telnet tcp port for alive testing of chrome process"""
        with closing(
                socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ) as test_sock:
            try:
                test_sock.settimeout(3)
                test_sock.connect(
                    (self.__ip, self.__port)
                )

                return True
            except Exception:
                pass

            return False

    def activate_dev_chrome_process(self):
        """Activate chrome process"""
        if self.is_alive():
            app.logger.info('Chrome dev. process is already started.')
            return

        app.logger.info('Chrome dev. process is starting...')
        import os
        os.system(START_DEVTOOL_CHROME_COMMAND + ' &')
        app.logger.info('Chrome dev. process is started!')
        sleep(10)


class ChromeBrowser(object):
    """Handle of Chrome Browser."""
    def __init__(self, tab_cls):
        """Prepare Connection of Chrome DevTools Bridge

            @param tab_cls: class of `Chrome.Tab`
            @type tab_cls: class
        """
        _CDPPortDetector().activate_dev_chrome_process()

        self.__tab_cls = tab_cls
        self.__browser = Browser()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_all_tabs()

    def new_tab(self):
        """Create a new tab instance in Browser & Return"""
        tab = self.__browser.new_tab()

        return self.__tab_cls(tab)

    def close_all_tabs(self):
        """Close all tabs for the Chrome Browser"""
        if len(self.__browser.list_tab()):
            for tab in self.__browser.list_tab():
                try:
                    tab.stop()
                except RuntimeException:
                    pass

                self.__browser.close_tab(tab)

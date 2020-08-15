from platform import system


# ## EXTERNAL ARGUMENTS ###################################
# RemoteDebuggingPort for `Chrome DevTools Protocal` (tcp port: 9222)
if 'linux' in system().lower():
    START_DEVTOOL_CHROME_COMMAND = 'google-chrome --user-data-dir=/tmp/chrome --ssl-key-log-file=/tmp/chrome_ssl_key.log --remote-debugging-port=9222 --disable-http2'  # noqa
else:
    START_DEVTOOL_CHROME_COMMAND = r'/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --user-data-dir=/tmp/chrome --ssl-key-log-file=/tmp/chrome_ssl_key.log --remote-debugging-port=9222 --disable-http2'  # noqa


# ## DEFINITIONS OF SPIDERS ###############################

BOT_NAME = 'estate'
SPIDER_MODULES = ['estate.spiders']
NEWSPIDER_MODULE = 'estate.spiders'


# ## DEFINITION OF SPIDER CRAWL RULES ######################

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 10
# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 8
# Radndom delay : DOWNLOAD_DELAY * 0.5 < x < DOWNLOAD_DELAY * 1.5
# Sample Code in library: `random.uniform(0.5 * self.delay, 1.5 * self.delay)`
RANDOMIZE_DOWNLOAD_DELAY = True
DOWNLOAD_TIMEOUT = 15      # 15 seconds


# ## DEFINITION OF SPIDER REQUEST RULES ######################

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html, application/xhtml+xml, application/xml',
  'Accept-Language': 'zh-CN,zh;q=0.8'
}

# Enable and configure HTTP caching (disabled by default)
HTTPCACHE_ENABLED = False
HTTPCACHE_EXPIRATION_SECS = 60*60*24      # one day
HTTPCACHE_DIR = 'juwai_httpcache'


# ## OTHER RULES ###############################

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Specify which URLs of 1 spider need to be debug in `SHELL`, default: None
# Then, people could use `selector` for debuging
INSPECTED_URL_IN_SHELL = None

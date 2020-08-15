"""This file is spider crawling policy definitions:


    Crawling Singapore agent lists from `www.propertyguru.com.sg`:

     - Root URL: `https://www.propertyguru.com.sg/property-agent-directory`

     - JIRA URL: `https://juwai.atlassian.net/browse/HW-2165`


    Protocal support for `Scrapy`:

     - HTTP 1.1 + TLS only.    Don't support HTTP/2 which used in Chrome.

     - Start Chrome with HTTP 1.1 by command :
        - `Chrome --user-data-dir=/tmp/chrome
                --ssl-key-log-file=/tmp/chrome_ssl_key.log --disable-http2`


    Execute js code in tag for each page to avoid forbidden from WebServer:

     - Anti-Forbidden Js:
            `<script type="text/javascript" src="/propguru198806.js" defer>`

     - But the code of Js had been `Obfuscated`, So need a Dom/Js simulator if
            we cannot spell fingerprint of Chrome

"""
from os import environ
from os.path import join as path_join
from urllib.parse import urljoin

from scrapy.http import Request
from ...common.spider import JuwaiSpider

from .items import AgentContact
from .items import AgentContactLoader


def _valid_page_filter(html_response):
    """Used in `ExclusiveCDPDownloaderMiddleware`

        Return True: the response is valid page, then scrape this page.
        Return False: the reponse is invalid page(wrong url / forbidden...)
                        , then request this page again

    """
    if 'Results Found' in html_response or\
            'CEA Licence No' in html_response:
        return True

    return False


class SingaporeAgents(JuwaiSpider):
    """
        Crawling rules definitions

        Data sources category list:
            `D12-D14` `D15-D16` `D17-D18` `D19-D20` `D22-D24` `D25-D28`

    """
    name = 'propertyguru_agents'    # should be a Global Unique name

    SQLITE3_CONNECTION = 'sqlite:///{}'.format(
        path_join(environ['HOME'], 'agents.db')
    )       # sqlite3 path:  `/home/xxx_user/agents.db`

    custom_settings = {             # overwrite the Global Settings
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html',
            'Content-Type': 'text/html'
        },
        'ITEM_PIPELINES': {
            'estate.spiders.propertyguru_agents.pipelines'
            '.AgentsPipeline': 300,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 100,
            'estate.middlewares.ExclusiveCDPDownloaderMiddleware': 800
        },
        'ROBOTSTXT_OBEY': False,
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': 5,
        'HTTPCACHE_ENABLED': True,
        'HTTPCACHE_EXPIRATION_SECS': 60 * 60 * 24 * 7,  # 7 Days'
        'HTTPCACHE_STORAGE': 'scrapy.extensions.httpcache.'
                             'FilesystemCacheStorage',
        'COOKIES_ENABLED': False,
        'FILTER_METHOD_OBJ': _valid_page_filter
    }
    allowed_domains = ['propertyguru.com.sg']
    # Data Source URLs as follow:
    start_urls = (
        'https://www.propertyguru.com.sg/property-agent-directory/balestier-geylang',   # noqa TAG: D12 - D14
        'https://www.propertyguru.com.sg/property-agent-directory/east-coast',          # noqa TAG: D15 - D16
        'https://www.propertyguru.com.sg/property-agent-directory/changi-pasir-ris',    # noqa TAG: D17 - D18
        'https://www.propertyguru.com.sg/property-agent-directory/serangoon-thomson',   # noqa TAG: D19 - D20
        'https://www.propertyguru.com.sg/property-agent-directory/west',                # noqa TAG: D22 - D24
        'https://www.propertyguru.com.sg/property-agent-directory/north'                # noqa TAG: D25 - D28
    )

    def __get_next_page_url(self, response):
        """Return 'Next Page's Url'"""
        next_urls = response.xpath(
            '//li[@class="pagination-next"]/a/@href'
        ).getall()

        return next_urls[0] if next_urls else None

    def __parse_page_for_rent(self, response):
        """Parse agent profile page for field `number of rent` only"""
        main_profile_page_url = response.url[:response.url.find('?')]

        profile_for_rent = AgentContactLoader(
            item=AgentContact(
                profile_page=main_profile_page_url
            ),
            selector=response
        )
        profile_for_rent.add_xpath(
            'number_of_rent',
            '//div[@class="agent-listings-block clearfix"]/h4/text()'
        )

        yield profile_for_rent.load_item()

    def __parse_profile(self, response):
        """Parse agent profile page for basic field of contact"""
        self._enter_debug_shell_by_url(response)

        profile = AgentContactLoader(
            item=AgentContact(profile_page=response.url),
            selector=response
        )
        profile.add_xpath(
            'agent_name', '//div[@class="agent-description"]/h3/text()'
        )
        profile.add_xpath(
            'agent_title', '//div[@class="agent-job-title"]/text()'
        )
        profile.add_xpath(
            'agency_name',
            '//div[@class="agent-description"]/div[@class="agent-agency"]/text()'  # noqa
        )
        profile.add_xpath(
            'agent_call',
            '//span[@class="agent-details-phone-number hide"]/text()'
        )
        profile.add_xpath(
            'license_company', '//div[@class="agent-license"]/a/text()'
        )
        profile.add_xpath(
            'license_individual', '//div[@class="agent-license"]/a/text()'
        )
        profile.add_xpath(
            'agent_website', '//div[@class="agent-website"]/a/@href'
        )
        profile.add_xpath(
            'agent_email',
            '//div[@class="agent-details-description compacted"]/text()'
        )
        profile.add_xpath(
            'number_of_sale',
            '//div[@class="agent-listings-block clearfix"]/h4/text()'
        )

        # Count agents pages number
        self.add_ref_count_by_tag(
            response.request.headers['Referer']
        )

        yield profile.load_item()

        # Parse url of field `number of rent`
        sale_and_rent = response.selector.xpath(
            '//div[@class="trans-types btn-group"]/a/@href'
        ).extract()

        if len(sale_and_rent):
            rent_url = urljoin(
                'https://www.propertyguru.com.sg/',
                sale_and_rent[1]
            )
            yield Request(
                url=rent_url, callback=self.__parse_page_for_rent
            )

    def parse(self, response):
        """Parse agents list page for agents list"""
        self._enter_debug_shell_by_url(response)

        agents_profiles_table = response.xpath(
            '//div[@class="agent-info-name"]/a/@href'
        )

        for agent_profile in agents_profiles_table:
            # Count list pages number
            self.add_ref_count_by_tag(response.url)

            profile_url = urljoin(
                'https://www.propertyguru.com.sg/', agent_profile.extract()
            )

            yield Request(
                url=profile_url, callback=self.__parse_profile
            )

        next_page_url = self.__get_next_page_url(response)
        if not next_page_url:
            return

        yield response.follow(
            next_page_url, callback=self.parse
        )

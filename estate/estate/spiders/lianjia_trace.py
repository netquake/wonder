from scrapy import Spider

from ..items import Property
from ..items import PropertyLoader


class _VillageTable(object):
    """Define the urls which need to be crawled
    """
    URL_MAPPING = {
        'https://sh.lianjia.com/ershoufang/c5011000014093/?sug=%E4%B9%9D%E5%9F%8E%E6%B9%96%E6%BB%A8%E5%9B%BD%E9%99%85': '九城湖滨',
        'https://sh.lianjia.com/ershoufang/rs%E5%A5%A5%E6%9E%97%E5%8C%B9%E5%85%8B%E8%8A%B1%E5%9B%AD/': '奥林匹克花园',
        'https://sh.lianjia.com/ershoufang/rs%E8%B4%9D%E5%B0%9A%E6%B9%BE(%E5%85%AC%E5%AF%93)/': '贝尚湾公寓',
        'https://sh.lianjia.com/ershoufang/c5011000017946/?sug=%E9%98%B3%E6%98%8E%E5%9B%BD%E9%99%85%E8%8A%B1%E8%8B%91': '阳明国际花苑'
    }

    def __init__(self):
        self.__handling_url = None

    def get_urls(self):
        return self.URL_MAPPING.keys()

    def get_handling_village_name_by_url(self, url):
        v_name = self.URL_MAPPING.get(url)

        if v_name:
            self.__handling_url = v_name

        return self.__handling_url


class PropertySummarySpider(Spider):
    """Crawl the property summary list in `Search Pages`
    """
    name = 'property'
    allowed_domains = ['sh.lianjia.com']

    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en'
        },
        'DOWNLOADER_MIDDLEWARES': {
            'estate.middlewares.RandomUserAgent': 1
        },
        'ITEM_PIPELINES': {
            'estate.pipelines.PropertyInfoPipeline': 300
        },
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 2,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'COOKIES_ENABLED': False,
        'TELNETCONSOLE_ENABLED': False,
        'COMMANDS_MODULE': 'estate.commands'
    }

    village_table = _VillageTable()
    start_urls = village_table.get_urls()

    def parse(self, response):
        for property_summary in response.xpath('//div[@class="item"]'):
            property_loader = PropertyLoader(
                item=Property(
                    source_type=1,
                    village_name=self.village_table.get_handling_village_name_by_url(response.url)
                ),
                selector=property_summary
            )
            property_loader.add_xpath('key_id', './/a[@class="img"]/@data-housecode')
            property_loader.add_xpath('url', './/a[@class="img"]/@href')
            property_loader.add_xpath('name', './/a[@class="title"]/text()')
            property_loader.add_xpath('region', './/div[@class="info"]', re='[\u4e00-\u9fa50-9. ]+')
            property_loader.add_xpath('rooms', './/div[@class="info"]', re='[\u4e00-\u9fa50-9. ]+')
            property_loader.add_xpath('area', './/div[@class="info"]', re='[\u4e00-\u9fa50-9. ]+')
            property_loader.add_xpath('layout', './/div[@class="info"]', re='[\u4e00-\u9fa50-9. ]+')
            property_loader.add_xpath('fixtures', './/div[@class="info"]', re='[\u4e00-\u9fa50-9. ]+')
            property_loader.add_xpath('tax', './/span[@class="taxfree"]/text()')
            property_loader.add_xpath('price', './/div[@class="price"]/span/text()')

            yield property_loader.load_item()

        next_page_url = self.__get_next_page(response)
        if not next_page_url:
            return

        yield response.follow(
            next_page_url, callback=self.parse
        )

    def __get_next_page(self, response):
        navigate_urls = response.xpath(
            '//div[@class="pagination_group_a"]'
        ).xpath('.//a/@href').getall()

        over_current_url = False
        for url in navigate_urls:
            if url in response.url:
                over_current_url = True
                continue

            if over_current_url:
                return response.urljoin(
                    url
                )

        return None

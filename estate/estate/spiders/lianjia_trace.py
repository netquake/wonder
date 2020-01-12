from scrapy import Spider

from ..items import Property
from ..items import PropertyLoader


class PropertySummarySpider(Spider):
    """Crawl the property summary list in `Search Pages`
    """
    name = 'property'
    allowed_domains = ['sh.lianjia.com']

    VILLAGE_MAPPING = {
        'https://sh.lianjia.com/ershoufang/c5011000014093/?sug=%E4%B9%9D%E5%9F%8E%E6%B9%96%E6%BB%A8%E5%9B%BD%E9%99%85': '九城湖滨'
    }

    start_urls = [
        v
        for v in VILLAGE_MAPPING.keys()
    ]

    def parse(self, response):
        for property_summary in response.xpath('//div[@class="item"]'):
            property_loader = PropertyLoader(
                item=Property(source_type=1),
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

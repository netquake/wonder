from scrapy import Spider

from ..items import Property
from ..items import PropertyLoader


class PropertyInfoSpider(Spider):
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
            property_loader = PropertyLoader(item=Property(), selector=property_summary)
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


        # for quote in response.css('div.quote'):
        #     yield {
        #         'text': quote.css('span.text::text').get(),
        #         'author': quote.css('small.author::text').get(),
        #         'tags': quote.css('div.tags a.tag::text').getall(),
        #     }
        #
        # next_page = response.css('li.next a::attr(href)').get()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield response.follow(next_page, callback=self.parse)

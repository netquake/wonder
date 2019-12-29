from scrapy import Spider
from scrapy.loader import ItemLoader

from ..items import Property


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
        property_loader = ItemLoader(item=Property(), response=response)
        sumary_loader = property_loader.nested_xpath('//div[@class="item"]')
        sumary_loader.add_xpath('url', '//a[@class="img"]/@href')
        sumary_loader.add_xpath('name', '//a[@class="title"]/text()')
        # sumary_loader.add_xpath('region', '//div[@class="info"]')[0].re('[\u4e00-\u9fa50-9. ]+')
        # sumary_loader.add_xpath('rooms', '//div[@class="info"]')[0].re('[\u4e00-\u9fa50-9. ]+')
        # sumary_loader.add_xpath('area', '//div[@class="info"]')[0].re('[\u4e00-\u9fa50-9. ]+')
        # sumary_loader.add_xpath('layout', '//div[@class="info"]')[0].re('[\u4e00-\u9fa50-9. ]+')
        # sumary_loader.add_xpath('fixtures', '//div[@class="info"]')[0].re('[\u4e00-\u9fa50-9. ]+')
        sumary_loader.add_xpath('tax', '//span[@class="taxfree"]/text()')
        sumary_loader.add_xpath('price', '//div[@class="price"]/span/text()')

        yield property_loader.load_item()

        # for property_summary in response.xpath('//div[@class="item"]'):
        #     property_url = property_summary.xpath('//a[@class="img"]/@href').get()
        #     property_name = property_summary.xpath('//a[@class="title"]/text()').get()
        #     info = property_summary.xpath('//div[@class="info"]')[0].re('[\u4e00-\u9fa50-9. ]+')
        #     property_region = info[1]
        #     property_rooms = info[2]
        #     property_area = info[3]
        #     property_layout = info[4]
        #     property_fixtures = info[5]
        #     property_tax = property_summary.xpath('//span[@class="taxfree"]/text()').get()
        #     property_price = property_summary.xpath('//div[@class="price"]/span/text()').get()
        #     if property_price:
        #         property_price = int(property_price) \
        #             if property_price.isdecimal() else 0
        #     else:
        #         property_price = 0


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

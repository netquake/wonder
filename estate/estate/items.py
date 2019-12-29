# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Field
from scrapy import Item


class Property(Item):
    url = Field()
    name = Field()
    region = Field()
    rooms = Field()
    area = Field()
    layout = Field()
    fixtures = Field()
    tax = Field()
    price = Field()
    # https://blog.csdn.net/zwq912318834/article/details/79530828

    @property
    def get_price(self):
        return self.price

    @get_price.setter
    def set_price(self, price_string):
        if price_string:
            self.price = int(price_string) \
                if price_string.isdecimal() else 0
        else:
            self.price = 0

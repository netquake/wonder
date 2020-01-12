# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Field
from scrapy import Item
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst


class PropertyLoader(ItemLoader):
    default_output_processor = TakeFirst()


def filter_region(values):
    return values[1]


def filter_rooms(values):
    return values[2]


def filter_area(values):
    return values[3]


def filter_layout(values):
    return values[4]


def filter_fixtures(values):
    return values[5]


def get_price(value):
    if len(value) > 0:
        return int(value[0]) \
            if value[0].isdecimal() else 0

    return 0


class Property(Item):
    key_id = Field()
    url = Field()
    name = Field()
    source_type = Field()
    region = Field(output_processor=filter_region)
    rooms = Field(output_processor=filter_rooms)
    area = Field(output_processor=filter_area)
    layout = Field(output_processor=filter_layout)
    fixtures = Field(output_processor=filter_fixtures)
    tax = Field()
    price = Field(output_processor=get_price)
    # https://blog.csdn.net/zwq912318834/article/details/79530828

# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst

class ScarpyseleniumItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

class ScrapyseleniumtestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection = 'products'
    image = scrapy.Field()
    price = scrapy.Field()
    deal = scrapy.Field()
    title = scrapy.Field()
    shop = scrapy.Field()
    location = scrapy.Field()


# -*- coding: utf-8 -*-
import scrapy

from ..items import NewsItem


class MydriversSpider(scrapy.Spider):
    name = 'mydrivers'
    allowed_domains = ['mydrivers.com']
    start_urls = ['http://mydrivers.com/']

    def parse(self, response):
        news = response.xpath('//ul[@class="newslist"]/li')
        # news = response.xpath('div[@class="main_left"]/div[@class="news_info news_blue"]/div[@class="news_info1"]/ul[@class="newslist"]/li')
        for cont in news:
            item = NewsItem()
            item['title'] = cont.xpath('./span/a/text()').extract_frist()
            item['url'] = cont.xpath('./span/a/@href').extract_first()

            yield item

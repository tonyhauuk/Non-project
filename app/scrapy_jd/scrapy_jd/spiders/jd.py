# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import quote
from scrapy import Request

from ..items import ScrapyJdItem

class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['jd.com']
    start_urls = ['http://jd.com/']
    baseUrl = 'https://search.jd.com/Search?keyword='

    def parse(self, response):
        products = response.xpath('')
        for product in products:
            item = ScrapyJdItem()

            item['image'] = ''.join()
            item['price'] = ''.join()
            item['deal'] = ''.join()
            item['title'] = ''.join()
            item['shop'] = ''.join()
            item['seller'] = ''.join()

            yield item


    def start_requests(self):
        for keyword in self.settings.get('KEYWORD'):
            for page in range(1, self.settings.get('MAX_PAGE') + 1):
                url = self.baseUrl + quote(keyword)

                yield Request(url=url, callback=self.parse, meta={'page': page}, dont_filter=True)

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem

class NewsPipeline(object):
    def __init__(self):
        self.limit = 50

    def process_item(self, item, spider):
        if item['title']:
            if len(item['title']) > self.limit:
                item['title'] = item['title'][0: self.limit].rstrip() + '...'
                with open('news.txt', 'a') as f:
                    f.write(item['title'] + ' -------- ' + item['utl'] + '\n')

            return item
        else:
            return DropItem('Missing Title')

import pymongo

class MongoPipeline(object):
    def __init__(self, mongoUri, mongoDB):
        self.mongoUri = mongoUri
        self.mongoDB = mongoDB

    @classmethod
    def fromCrawler(cls, crawler):
        return cls(
            mongoUri=crawler.settings.get('MONGO_URI'),
            mongoDB= crawler.settings.get('MONGO_DB')
        )

    def openSpider(self, spider):
        self.client = pymongo.MongoClient(self.mongoUri)
        self.db = self.client[self.mongoDB]

    def processItem(self, item, spider):
        name = item.__class__.name
        self.db[name].insert(dict(item))

        return item

    def close(self, spider):
        self.client.close()

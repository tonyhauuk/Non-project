import crawler
from db import RedisClient

POOL_UPPER_THRESHOLD = 10000

class Getter():
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()

    def isOverThreshold(self):
        if self.redis.count >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False


    def run(self):
        print('getter start: ')
        if not self.isOverThreshold():
            for callbackLabel in range(self.crawler__CrawlFuncCount__):
                callback = self.crawler.__CrawlFunc__[callbackLabel]
                proxies = self.crawler.getProxies(callback)

                for proxy in proxies:
                    self.redis.add(proxy)
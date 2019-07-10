import json
from pyquery import PyQuery as pq

class ProxyMetaClass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'cralw' in k:
                attrs['__CrawlFunc__'] = count
                count += 1

        attrs['__CrawlFunc__'] = count

        return type.__new__(cls, name, bases, attrs)

class Crawler(object, metaclass=ProxyMetaClass):
    def getProxies(self, callback):
        proxies = []
        for proxy in  eval('self.{}()'.format(callback)):
            print('success obtain proxy')
            proxies.append(proxy)

        return proxies

    def crawlProxy360(self):
        url = 'c'
        html = ''
        if html:
            doc = pq(html)
            lines = doc('div[name="list_proxy_ip"]').items()
            for line in lines:
                ip = line.find('tbButtomLine:nth-child(1)').text()
                port = line.find('tbButtomLine:nth-child(2)').text()
                yield ':'.join([ip, port])
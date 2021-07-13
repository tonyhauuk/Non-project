# -*- coding: utf-8 -*-

import time, hashlib, os, datetime
from time import sleep
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Sznews:
    def __init__(self):
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        self.date = time.strftime('%Y-%m-%d', timeArray)
        self.d = {}
        self.dir = self._dir = ''
        self.debug = True
        self.browser = webdriver.Firefox()
        self.browser.set_window_position(x = 620, y = 0)


    def crawl(self):
        webLst = ['http://sztqb.sznews.com/',
                  'http://szsb.sznews.com/',
                  'http://wb.sznews.com/PC/layout/index.html',
                  'http://jb.sznews.com/PC/layout/index.html',
                  'http://szjy.sznews.com/',
                  'http://barb.sznews.com/',]

        for url in webLst:
            self.i = 0
            try:
                self.browser.get(url)
                sleep(2)
            except TimeoutException:
                return

            loop = self.browser.find_elements_by_css_selector('div.Therestlist > ul > li')  # 计算翻页的次数
            length = len(loop)
            sleep(1)

            for i in range(length):
                newsList = self.browser.find_elements_by_css_selector('div.newslist> ul > li')
                for j in range(len(newsList)):
                    item = self.browser.find_elements_by_css_selector('div.newslist> ul > li')[j]
                    titleInfo = item.find_element_by_css_selector('h3 > a')
                    link = titleInfo.get_attribute('href')

                    md5 = self.makeMD5(link)
                    if md5 in self.d:
                        break
                    else:
                        self.d[md5] = self.date.split(' ')[0]  # 往dict里插入记录
                        self.i += 1
                        self.extract(item, link)

                if i == length:
                    break
                else:
                    try:
                        self.browser.find_element_by_css_selector('div.newscon.clearfix > div.newsnextright > a').click()
                        self.i = 0
                        sleep(3)
                    except Exception as e:
                        break



    # 提取信息，一条的
    def extract(self, info, link):
        title = info.text
        info.find_element_by_tag_name('a').click()

        sleep(2)                            # 等个几秒钟
        self.source = self.getPageText()    # 拿到网页源码
        print(link, title)
        # self.write_new_file(url, title, self.source, self.i, self.date, 414707)
        self.browser.find_element_by_css_selector('div.newscon.clearfix > div.\+div > a').click()


    # 生成md5信息
    def makeMD5(self, title):
        m = hashlib.md5()
        b = title.encode(encoding = 'utf-8')
        m.update(b)
        enc = m.hexdigest()

        return enc


    def getPageText(self):
        url = self.browser.current_url
        try:
            content = self.browser.find_element_by_css_selector('div.newsdetatext').get_attribute('innerHTML')
        except NoSuchElementException:
            content = self.browser.page_source

        return content, url


if __name__ == '__main__':
    c = Sznews()
    c.crawl()

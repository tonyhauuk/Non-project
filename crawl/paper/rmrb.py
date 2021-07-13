# -*- coding: utf-8 -*-

import time, hashlib, os
from time import sleep
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Rmrb:
    def __init__(self):
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        self.date = time.strftime('%Y-%m-%d', timeArray)
        self.d = {}
        self.dir = self._dir = ''
        self.debug = True
        self.browser = webdriver.Firefox()
        self.browser.set_window_position(x = 600, y = 0)


    def crawl(self):
        self.i = 0
        try:
            self.browser.get('http://paper.people.com.cn/rmrb/')
            sleep(2)
        except TimeoutException:
            return 'interrupt', 'none', 'error'


        chapters = self.browser.find_elements_by_css_selector('div.swiper-box > div.swiper-container > div.swiper-slide')
        for i in range(len(chapters)):
            chapter = self.browser.find_elements_by_css_selector('div.swiper-box > div.swiper-container > div.swiper-slide')[i]
            info = chapter.find_element_by_tag_name('a')
            if i > 0:
                info.click()

            newsList = self.browser.find_elements_by_css_selector('div.news > ul.news-list > li')

            for j in range(len(newsList)):
                item = self.browser.find_elements_by_css_selector('div.news > ul.news-list > li')[j]
                self.extract(item)


        if self.i > 0:
            # self.rename()
            # self.expire()
            # self.deleteFiles()
            self.source = ''

            return 'complete', self.source, 'ok'
        else:
            return 'complete', 'none', 'ok'


    # 提取信息，一条的
    def extract(self, info):
        a = info.find_element_by_tag_name('a')
        href = a.get_attribute('href')
        title = a.text.strip()
        md5 = self.makeMD5(title)

        # dict filter
        if md5 in self.d:
            return
        else:
            self.d[md5] = self.date  # 往dict里插入记录
            self.i += 1

        a.click()
        self.source = self.getPageText()    # 拿到网页源码
        sleep(1)                            # 等个几秒钟
        print(href, title)
        self.browser.back()                 # 关闭当前标签页
        sleep(1)

        # try:
        #     self.write_new_file(href, title, self.source, self.i, self.date, 896975)
        # except (NoSuchElementException, NoSuchAttributeException) as e:
        #     print('Element error:', e)
        # except Exception:
        #     return

    # 生成md5信息
    def makeMD5(self, title):
        m = hashlib.md5()
        b = title.encode(encoding = 'utf-8')
        m.update(b)
        enc = m.hexdigest()

        return enc

    def getPageText(self):
        try:
            html = self.browser.find_element_by_css_selector('div#ozoom').text
        except NoSuchElementException:
            html = self.browser.page_source

        return html

if __name__ == '__main__':
    r = Rmrb()
    r.crawl()
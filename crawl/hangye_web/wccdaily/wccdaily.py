# -*- coding: utf-8 -*-

import time, hashlib, os
from time import sleep
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Wccdaily:
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
        webList = ['http://www.wccdaily.com.cn/shtml/index_hxdsb.shtml', 'http://www.wccdaily.com.cn/shtml/index_hxdsbsq.shtml']
        for url in webList:
            try:
                self.browser.get(url)
                sleep(5)
            except TimeoutException:
                return

            newsList = self.browser.find_elements_by_css_selector('div.page-title-item > ul > li')

            for i in range(len(newsList)):
                item = self.browser.find_elements_by_css_selector('div.page-title-item > ul > li')[i]
                titleInfo = item.find_element_by_css_selector('a')
                title = titleInfo.text
                if title in '广告':
                    continue

                status = self.extract(titleInfo, title, url)
                if status:
                    break

            if self.i > 0:
                pass
                # self.rename()
                # self.expire()




    # 提取信息，一条的
    def extract(self, info, title, url):
        link = info.get_attribute('href')
        md5 = self.makeMD5(link)

        # dict filter
        if md5 in self.d:
            return True
        else:
            self.d[md5] = self.date  # 往dict里插入记录
            self.i += 1
        try:
            info.click()
            sleep(2)
            self.source = self.getPageText()    # 拿到网页源码
            self.browser.back()                 # 关闭当前标签页
            sleep(1)

            if 'index_hxdsb' in url:
                pass
                # self.write_new_file(link, title, self.source, self.i, self.date, 1171868)
            elif 'index_hxdsbsq' in url:
                pass
                # self.write_new_file(link, title, self.source, self.i, self.date, 1171869)
            return False
        except Exception:
            return True

    # 生成md5信息
    def makeMD5(self, link):
        m = hashlib.md5()
        b = link.encode(encoding = 'utf-8')
        m.update(b)
        enc = m.hexdigest()

        return enc

    def getPageText(self):
        try:
            html = self.browser.find_element_by_css_selector('div.detail-box:not(.detail-title-box)').text
        except Exception as e:
            html = self.browser.page_source

        return html

if __name__ == '__main__':
    r = Wccdaily()
    r.crawl()
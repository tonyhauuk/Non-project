# -*- coding: utf-8 -*-

import time, hashlib, os
from time import sleep
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SouthernGrid:
    def __init__(self):
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        self.date = time.strftime('%Y-%m-%d %H:%M:%S', timeArray)
        self.d = {}
        self.dir = self._dir = self.source = ''
        self.debug = True
        self.browser = webdriver.Firefox()
        self.browser.set_window_position(x = 600, y = 0)


    def crawl(self):
        self.i = self.total = 0
        page = 1
        try:
            self.browser.get('http://www.bidding.csg.cn/zbcg/index_1.jhtml')
        except TimeoutException:
            return 'interrupt', 'none', 'error'

        while True:     # 翻页循环
            newsList = self.browser.find_elements_by_css_selector('div.List2 > ul > li')

            for i in range(len(newsList)):
                item = self.browser.find_elements_by_css_selector('div.List2 > ul > li')[i]
                dateTime = item.find_element_by_css_selector('span.Right > span').text
                if dateTime in self.date:
                    self.extract(item)
                else:
                    if page == 1:
                        continue        # 南方电网第一页会有老的信息，所以遇到时间不匹配直接跳过，继续往下采
                    else:
                        break

            if self.i < len(newsList) and page > 1:     # 如果当前页抓取的条数小于看到的条数，并且不在第一页，直接跳出
                break
            else:
                try:
                    self.browser.find_elements_by_css_selector('div.fenye.TxtCenter > div > a')[2].click()  # 翻页
                    self.i = 0
                    page += 1
                except NoSuchElementException:
                    break



        if self.i > 0:
            # self.rename()
            # self.expire()
            # self.deleteFiles()
            return 'complete', self.source, 'ok'
        else:
            return 'complete', 'none', 'ok'


    # 提取信息，一条的
    def extract(self, item):
        titleInfo = item.find_elements_by_tag_name('a')[2]

        try:
            href = titleInfo.get_attribute('href')
            md5 = self.makeMD5(href)
            print('link:',href)
            # dict filter
            if md5 in self.d:
                return
            else:
                self.d[md5] = self.date.split(' ')[0]       # 往dict里插入记录
                self.i += 1
                self.total += 1

            titleInfo.click()

            self.source, self.title = self.getPageText()  # 拿到网页源码
            self.browser.back()
            sleep(2)

            # self.write_new_file(href, title, self.source, self.total, self.date, 1096244)
        except Exception:
            self.i -= 1
            self.total -= 1
            return




    # 生成md5信息
    def makeMD5(self, title):
        m = hashlib.md5()
        b = title.encode(encoding = 'utf-8')
        m.update(b)
        enc = m.hexdigest()

        return enc

    def getPageText(self):
        try:
            content = self.browser.find_element_by_css_selector('div.Content').get_attribute('innerHTML')
        except NoSuchElementException:
            content = self.browser.page_source

        title = self.browser.find_element_by_css_selector('h1.s-title').text

        return content, title




if __name__ == '__main__':
    sg = SouthernGrid()
    sg.crawl()
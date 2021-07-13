# -*- coding: utf-8 -*-

import time, hashlib, os
from time import sleep
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Hubeidaily:
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
        webList = ['https://epaper.hubeidaily.net',
                   'https://ctdsbepaper.hubeidaily.net',
                   'https://ncxbepaper.hubeidaily.net',
                   'https://sxwbepaper.hubeidaily.net',
                   'https://ctkbepaper.hubeidaily.net']

        for x in range(len(webList)):
            try:
                self.browser.get(webList[x])
                sleep(5)
            except TimeoutException:
                return

            blockList = self.browser.find_elements_by_css_selector('div.nav-list > ul > li')
            for i in range(len(blockList)):
                newsList = self.browser.find_elements_by_css_selector('div.news-list > ul > li.resultList')
                for j in range(len(newsList)):
                    item = self.browser.find_elements_by_css_selector('div.news-list > ul > li.resultList')[j]
                    status = self.extract(item, x)
                    if status:
                        break

                try:
                    self.browser.find_element_by_css_selector('div.right-btn > ul > li > a.b-btn').click()
                    self.i = 0
                except:
                    break

            if self.i > 0:
                pass
                # self.rename()
                # self.expire()


    # 提取信息，一条的
    def extract(self, info, webID):
        link = info.find_element_by_css_selector('a').get_attribute('href')
        md5 = self.makeMD5(link)

        title = info.find_element_by_css_selector('a > h4').text
        if title == '广告':
            return False

        # dict filter
        if md5 in self.d:
            return True
        else:
            self.d[md5] = self.date.split(' ')[0]  # 往dict里插入记录
            self.i += 1
        try:
            info.click()
            sleep(2)
            self.source = self.getPageText()  # 拿到网页源码
            self.browser.back()  # 关闭当前标签页
            sleep(1)

            if webID == 0:
                rid = 51760
            elif webID == 1:
                rid = 58049
            elif webID == 2:
                rid = 59730
            elif webID == 3:
                rid = 416076
            elif webID == 4:
                rid = 501995

            print(link, title, rid)
            # self.write_new_file(link, title, self.source, self.i, self.date, rid)
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
            html = self.browser.find_element_by_id('ozoom').text
        except Exception as e:
            html = self.browser.page_source

        return html


if __name__ == '__main__':
    r = Hubeidaily()
    r.crawl()

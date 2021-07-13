# -*- coding: utf-8 -*-

import time, hashlib, os
from time import sleep
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Gzdaily:
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
        print('\n', '-' * 10, 'https://gzdaily.dayoo.com/', '-' * 10)

        self.i = 0
        try:
            self.browser.get('https://gzdaily.dayoo.com/')
            sleep(5)
        except:
            return

        page = self.browser.find_elements_by_css_selector('table#bmdhTable > tbody > tr')
        for i in range(len(page)):
            newsList = self.browser.find_elements_by_css_selector('div#main-ed-articlenav-list > table > tbody > tr')
            for j in range(len(newsList)):
                item = self.browser.find_elements_by_css_selector('div#main-ed-articlenav-list > table > tbody > tr')[j]
                try:
                    titleInfo = item.find_element_by_css_selector('td.default > div > a')
                except:
                    continue

                status = self.extract(titleInfo)
                if status:
                    break

            try:
                if i < len(page):
                    self.browser.find_element_by_css_selector('a#ed_next').click()

                else:
                    break
            except:
                break


        if self.i > 0:
            # self.rename()
            # self.expire()

            return 'complete', self.source, 'ok'
        else:
            return 'complete', 'none', 'ok'


    # 提取信息，一条的
    def extract(self, info):
        link = info.get_attribute('href')
        md5 = self.makeMD5(link)

        # dict filter
        if md5 in self.d:
            return True
        else:
            self.d[md5] = self.date.split(' ')[0]   # 往dict里插入记录
            self.i += 1

        try:
            title = info.text
            info.click()
            sleep(2)
            self.source = self.getPageText()    # 拿到网页源码
            print(link, title)
            self.browser.back()                 # 关闭当前标签页
            sleep(1)

            # self.write_new_file(link, title, self.source, self.i, self.date, 17550)
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
            html = self.browser.find_element_by_css_selector('div#ozoom').text
        except:
            html = self.browser.page_source

        return html

if __name__ == '__main__':
    r = Gzdaily()
    r.crawl()

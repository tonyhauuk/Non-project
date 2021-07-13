# -*- coding: utf-8 -*-

import time, hashlib, os
from time import sleep
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Qnck:
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
        print('\n' ,'-' * 10, 'http://qnck.cyol.com/', '-' * 10)
        self.i = 0

        try:
            self.browser.get('http://qnck.cyol.com/')
            sleep(5)
        except TimeoutException:
            return

        while True:
            newsList = self.browser.find_elements_by_css_selector('#titleList > ul > li')

            for i in range(len(newsList)):
                item = self.browser.find_elements_by_css_selector('#titleList > ul > li')[i]

                status = self.extract(item)
                if status:
                    break

            try:
                self.browser.find_element_by_partial_link_text('下一版').click()
                sleep(2)
                self.i = 0
            except:
                break

        if self.i > 0:
            pass
            # self.rename()
            # self.expire()




    # 提取信息，一条的
    def extract(self, info):
        link = info.find_element_by_css_selector('a').get_attribute('href')
        md5 = self.makeMD5(link)

        # dict filter
        if md5 in self.d:
            return True
        else:
            self.d[md5] = self.date.split(' ')[0]  # 往dict里插入记录
            self.i += 1

        try:
            title = info.find_element_by_css_selector('a').text
            info.click()
            sleep(2)
            self.source = self.getPageText()    # 拿到网页源码
            self.browser.back()                 # 关闭当前标签页
            sleep(1)
            print(link, title)
            # self.write_new_file(link, title, self.source, self.i, self.date, 1171634)
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
        except Exception as e:
            html = self.browser.page_source

        return html

if __name__ == '__main__':
    r = Qnck()
    r.crawl()
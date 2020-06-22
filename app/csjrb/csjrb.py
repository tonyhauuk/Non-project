# -*- coding: utf-8 -*-

import time, hashlib, os
from time import sleep
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Csjrb:
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
            self.browser.get('http://epaper.csjrw.cn/tbpaper.do?epaper=daoduList')
        except TimeoutException:
            return 'interrupt', 'none', 'error'

        newsList = self.browser.find_elements_by_css_selector('div.guowang_con > div')
        for item in newsList:
            info = item.find_elements_by_css_selector('span.daodu_bt > a')
            href = info.get_attribute('href')

            md5 = self.makeMD5(href)
            # dict filter
            if md5 in self.d:
                return
            else:
                self.d[md5] = self.date  # 往dict里插入记录
                self.i += 1
                self.extract(info, href)

        if self.i > 0:
            # self.rename()
            # self.expire()
            # self.deleteFiles()

            return 'complete', self.source, 'ok'
        else:
            return 'complete', 'none', 'ok'


    # 提取信息，一条的
    def extract(self, info, href):
        try:
            title = info.text
            print(href, title)
            return

            info.click()

            self.source = self.browser.find_element_by_css_selector('div#zoom').text
            self.write_new_file(href, title, self.source, self.i, self.date, 414705)


        except (NoSuchElementException, NoSuchAttributeException) as e:
            print('Element error:', e)

        except Exception:
            return

    # 生成md5信息
    def makeMD5(self, title):
        m = hashlib.md5()
        b = title.encode(encoding = 'utf-8')
        m.update(b)
        enc = m.hexdigest()

        return enc
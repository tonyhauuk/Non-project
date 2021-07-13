# -*- coding: utf-8 -*-

import time, hashlib, os
from time import sleep
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Jj831:
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
            self.browser.get('http://np.jj831.com/')
            sleep(5)
        except TimeoutException:
            return 'interrupt', 'none', 'error'


        newsList = self.browser.find_elements_by_css_selector('tr.default1')
        for i in range(len(newsList))[1:]:
            item = self.browser.find_elements_by_css_selector('tr.default1')[i]
            try:
                titleInfo = item.find_element_by_css_selector('td > a')
            except NoSuchElementException:
                continue


            title = titleInfo.text
            if '责任编辑' in title or title in '广告' or '微信、APP' in title:
                continue

            status = self.extract(titleInfo, title)
            if status:
                break





        if self.i > 0:
            # self.rename()
            # self.expire()
            # self.deleteFiles()

            return 'complete', self.source, 'ok'
        else:
            return 'complete', 'none', 'ok'


    # 提取信息，一条的
    def extract(self, info, title):
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
            print(link, title)


            self.browser.back()                 # 关闭当前标签页
            sleep(1)

            # self.write_new_file(link, title, self.source, self.i, self.date, 416234)
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
    r = Jj831()
    r.crawl()
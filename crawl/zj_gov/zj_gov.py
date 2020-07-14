# -*- coding: utf-8 -*-

import time, hashlib, os
from time import sleep
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ZJ_gov:
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
        try:
            self.browser.get('http://zjamr.zj.gov.cn/col/col1228969890/index.html')
        except TimeoutException:
            return 'interrupt', 'none', 'error'

        while True:     # 翻页循环
            newsList = self.browser.find_elements_by_css_selector('div.list_right_text > table > tbody > tr')
            for item in newsList:
                dateTime = item.find_element_by_css_selector('td:nth-child(2)').text
                if self.date.split(' ')[0] in dateTime:
                    self.extract(item)
                else:
                    break

            if self.i < len(newsList):
                break
            else:
                try:
                    self.browser.find_element_by_name('下页').click()  # 翻页
                    self.i = 0
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
        titleInfo = item.find_element_by_css_selector('td:nth-child(1) > a')

        try:
            href = titleInfo.get_attribute('href')
            md5 = self.makeMD5(href)

            # dict filter
            if md5 in self.d:
                return
            else:
                self.d[md5] = self.date.split(' ')[0]       # 往dict里插入记录
                self.i += 1
                self.total += 1

            title = titleInfo.text

            handle = self.browser.current_window_handle     # 拿到当前页面的handle
            titleInfo.click()

            # switch tab window
            WebDriverWait(self.browser, 10).until(EC.number_of_windows_to_be(2))
            handles = self.browser.window_handles
            for newHandle in handles:
                if newHandle != handle:
                    self.browser.switch_to.window(newHandle)        # 切换到新标签
                    sleep(2)                                        # 等个几秒钟
                    self.source = self.getPageText()                # 拿到网页源码
                    self.browser.close()                            # 关闭当前标签页
                    self.browser.switch_to.window(handle)           # 切换到之前的标签页
                    break
            print(href, title)
            # self.write_new_file(href, title, self.source, self.total, self.date, 1167612)
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
            content = self.browser.find_element_by_css_selector('div.nr_text').get_attribute('innerHTML')
        except NoSuchElementException:
            content = self.browser.page_source

        return content




if __name__ == '__main__':
    zj = ZJ_gov()
    zj.crawl()
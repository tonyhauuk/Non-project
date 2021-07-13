# -*- coding: utf-8 -*-

import time, hashlib, os, datetime
from time import sleep
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Bjd:
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
            self.browser.get('http://chinafund.stcn.com/paper/zgjjb/')
            sleep(1)
        except:
            return

        newsList = self.browser.find_elements_by_css_selector('div#listWrap > div.area > ul > li')

        for item in newsList:
            try:
                link = item.find_element_by_tag_name('a').get_attribute('href')
                md5 = self.makeMD5(link)

                if md5 in self.d:
                    break
                else:
                    self.d[md5] = self.date.split(' ')[0]  # 往dict里插入记录
                    self.i += 1
                    self.extract(item, link)
            except Exception as e:
                print('loop: ',e)


    # 提取信息，一条的
    def extract(self, titleInfo, link):
        try:
            title = titleInfo.find_element_by_tag_name('a').text

            handle = self.browser.current_window_handle  # 拿到当前页面的handle
            titleInfo.click()

            # switch tab window
            WebDriverWait(self.browser, 10).until(EC.number_of_windows_to_be(2))
            handles = self.browser.window_handles
            for newHandle in handles:
                if newHandle != handle:
                    self.browser.switch_to.window(newHandle)                # 切换到新标签
                    sleep(2)                                                # 等个几秒钟
                    self.source = self.getPageText()                        # 拿到网页源码
                    self.browser.close()                                    # 关闭当前标签页
                    self.browser.switch_to.window(handle)                   # 切换到之前的标签页
                    break
            print(link, title)
            # self.write_new_file(link, title, self.source, self.i, self.date, 1161124)
        except Exception as e:
            print(e)


    # 生成md5信息
    def makeMD5(self, title):
        m = hashlib.md5()
        b = title.encode(encoding = 'utf-8')
        m.update(b)
        enc = m.hexdigest()

        return enc

    def getPageText(self):
        try:
            content = self.browser.find_element_by_css_selector('div.txtWrap').get_attribute('innerHTML')
        except NoSuchElementException:
            content = self.browser.page_source

        return content

if __name__ == '__main__':
    c = Bjd()
    c.crawl()
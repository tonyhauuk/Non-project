# -*- coding: utf-8 -*-

import time, hashlib, os
from time import sleep
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# import cralwerfun

class Liuyan_people:
    def __init__(self, d):
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        self.date = time.strftime('%Y-%m-%d %H:%M:%S', timeArray)
        self.d = d
        self.dir = self._dir = ''
        self.debug = True


    def crawl(self):
        print('\n', '-' * 10, 'http://liuyan.people.com.cn/', '-' * 10, '\n')

        self.browser = webdriver.Firefox()
        self.browser.set_window_position(x = 630, y = 0)

        self.total = 0
        i = 0
        status = True
        file = './liuyan_people_weblist.txt'
        with open(file, mode = 'r') as f:
            url = f.readlines()
            for x in url:
                channel = ['建言', '投诉', '咨询']
                for key in channel:
                    n = self.doCrawl(x, key)
                    if n == -1:
                        status = False
                        break
                    else:
                        i += n

        if status:
            if i > 0:
                return 'complete', self.source, 'ok'
            else:
                return 'complete', 'none', 'ok'
        else:
            return 'interrupt', 'none', 'error'


    def doCrawl(self, url, key):
        self.i = 0
        try:
            self.browser.get(url)
            sleep(3)
        except TimeoutException:
            return -1

        if key == '投诉':
            self.browser.find_element(by = By.CSS_SELECTOR, value = 'div#tab-second').click()
            sleep(3)
        elif key == '咨询':
            self.browser.find_element(by = By.CSS_SELECTOR, value = 'div#tab-third').click()
            sleep(3)

        start = 0
        while True:
            newsList = self.browser.find_elements(By.CSS_SELECTOR, 'ul.replyList > li')
            end = len(newsList)
            for item in newsList[start:end]:
                dateTime = item.find_element(By.CSS_SELECTOR, 'div.headMainS.fl > p').text.strip()
                # print('date time:',dateTime)
                if self.date.split(' ')[0] in dateTime:
                    status = self.extract(item)
                    if status:
                        break
                else:
                    break

            if self.i < len(newsList):
                break
            else:
                try:
                    start = end + 1
                    self.browser.find_element(By.CSS_SELECTOR, 'div.mordList').click()
                    sleep(1)
                except:
                    break


        if self.total > 0:
            # self.rename()
            # self.expire()

            return self.total
        else:
            return 0


    # 提取信息，一条的
    def extract(self, item):
        url = ''
        titleInfo = item.find_element(By.CSS_SELECTOR, 'div.tabList.fl > h1')
        title = titleInfo.text
        try:
            md5 = self.makeMD5(title)

            # dict filter
            if md5 in self.d:
                return True
            else:
                self.d[md5] = self.date.split(' ')[0]  # 往dict里插入记录
                self.i += 1
                self.total += 1

            handle = self.browser.current_window_handle  # 拿到当前页面的handle
            titleInfo.click()

            # switch tab window
            WebDriverWait(self.browser, 10).until(EC.number_of_windows_to_be(2))
            handles = self.browser.window_handles
            for newHandle in handles:
                if newHandle != handle:
                    self.browser.switch_to.window(newHandle)        # 切换到新标签
                    sleep(5)                                        # 等个几秒钟
                    self.source, url = self.getPageText()           # 拿到网页源码
                    self.browser.close()                            # 关闭当前标签页
                    self.browser.switch_to.window(handle)           # 切换到之前的标签页
                    break
            print(self.i, url, title)
            # self.write_new_file(href, title, self.source, self.i, self.date, 92816)
        except Exception:
            return False


    def getPageText(self):  # 获取网页正文
        try:
            html = self.browser.find_element(By.CSS_SELECTOR, 'p#replyContentMain').get_attribute('innerHTML')
        except NoSuchElementException:
            html = self.browser.page_source

        return html, self.browser.current_url


    # 生成md5信息
    def makeMD5(self, link):
        m = hashlib.md5()
        b = link.encode(encoding = 'utf-8')
        m.update(b)
        enc = m.hexdigest()

        return enc


if __name__ == '__main__':
    sc = Liuyan_people({})
    sc.crawl()

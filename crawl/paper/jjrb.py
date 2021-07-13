# -*- coding: utf-8 -*-

import time, hashlib, os
from time import sleep
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Jjrb:
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
            self.browser.get('http://paper.ce.cn/')
            sleep(2)
        except TimeoutException:
            return 'interrupt', 'none', 'error'

        while True:
            # 第一篇文章，必须要点开一次
            first = self.browser.find_element_by_xpath('/html/body/table/tbody/tr[1]/td[2]/table[2]/tbody/tr/td[3]/table[4]/tbody/tr/td/div/table/tbody/tr[1]/td[2]/a')
            self.extract(first, 1)

            otherList = self.browser.find_elements_by_xpath('//*[@id="content"]/table/tbody/tr[1]/td[1]/table/tbody/tr[1]/td/table[3]/tbody/tr/td[2]/table/tbody/tr[4]/td/div/table/tbody/tr')
            for i in range(1, len(otherList)):
                item = self.browser.find_elements_by_xpath('//*[@id="content"]/table/tbody/tr[1]/td[1]/table/tbody/tr[1]/td/table[3]/tbody/tr/td[2]/table/tbody/tr[4]/td/div/table/tbody/tr')[i]
                self.extract(item, 2)

            try:
                self.browser.find_element_by_partial_link_text('下一版').click()
                sleep(2)
            except NoSuchElementException:
                break




        if self.i > 0:
            # self.rename()
            # self.expire()
            # self.deleteFiles()
            self.source = ''

            return 'complete', self.source, 'ok'
        else:
            return 'complete', 'none', 'ok'


    # 提取信息，一条的
    def extract(self, info, count):
        title = info.find_element_by_tag_name('div').text.strip()
        if title == '责编' or title == '本版责编':    # 如果标题是这两个，直接跳过不采集没用的信息
            return

        if count == 1:
            href = info.get_attribute('href')
        elif count == 2:
            href = info.find_element_by_xpath('td[2]/a').get_attribute('href')

        md5 = self.makeMD5(href)

        # dict filter
        if md5 in self.d:
            return
        else:
            self.d[md5] = self.date  # 往dict里插入记录
            self.i += 1


        if count == 1:
            info.click()
        else:
            info.find_element_by_xpath('td[2]/a/div').click()

        self.source = self.getPageText()    # 拿到网页源码
        sleep(1)                            # 等个几秒钟
        print(href, title)


        # self.browser.back()                 # 关闭当前标签页
        # sleep(1)

        # try:
        #     self.write_new_file(href, title, self.source, self.i, self.date, 392517)
        # except (NoSuchElementException, NoSuchAttributeException) as e:
        #     print('Element error:', e)
        # except Exception:
        #     return

    # 生成md5信息
    def makeMD5(self, link):
        m = hashlib.md5()
        b = link.encode(encoding = 'utf-8')
        m.update(b)
        enc = m.hexdigest()

        return enc

    def getPageText(self):
        try:
            html = self.browser.find_element_by_xpath('//*[@id="content"]/table/tbody/tr[1]/td[2]/table[2]/tbody/tr/td/table/tbody/tr[2]/td/div').text
        except:
            html = self.browser.find_element_by_css_selector('div#ozoom').text

        return html

if __name__ == '__main__':
    r = Jjrb()
    r.crawl()
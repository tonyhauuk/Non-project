# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By
import time, hashlib, os
from time import sleep
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class StateGrid:
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
            self.browser.get('https://ecp.sgcc.com.cn/ecp2.0/portal/#/list/list-spe/2018032600000014_5_2018032700291334')
        except TimeoutException:
            return 'interrupt', 'none', 'error'

        while True:     # 翻页循环
            newsList = self.browser.find_elements_by_css_selector('table.table.table-striped > tbody > tr')
            length = len(newsList)

            for i in range(length):
                items = self.browser.find_elements_by_css_selector('table.table.table-striped > tbody > tr')
                item = items[i]

                dateTime = item.find_element_by_css_selector('tr.time').text

                if dateTime in self.date:
                    print('date time:', dateTime)
                    self.extract(item)
                else:
                    try:
                        item.find_element_by_css_selector('td.title > span > img')  # 判断是否有top的img标签
                        continue
                    except NoSuchElementException:
                        break

            if self.i < length:
                break
            else:
                try:
                    self.browser.find_element_by_css_selector('div.page > a > b.next').click()  # 翻页
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
        try:
            href = titleInfo.get_attribute('onclick')
            md5 = self.makeMD5(href)

            # dict filter
            if md5 in self.d:
                return
            else:
                self.d[md5] = self.date.split(' ')[0]       # 往dict里插入记录
                self.i += 1
                self.total += 1

            title = titleInfo.get_attribute('title')

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
            content = self.browser.find_element_by_css_selector('div.bot_list').get_attribute('innerHTML')
        except NoSuchElementException:
            content = self.browser.find_element_by_css_selector('div.article_infor').get_attribute('innerHTML')

        href = self.browser.current_url

        return content




if __name__ == '__main__':
    sg = StateGrid()
    sg.crawl()
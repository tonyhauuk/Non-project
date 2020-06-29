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

        while True:
            newsList = self.browser.find_elements_by_css_selector('div.guowang_con > div > span.daodu_bt')
            for item in newsList:
                info = item.find_element_by_tag_name('a')
                self.extract(info)

            try:
                next = self.browser.find_elements_by_css_selector('td > a > img')
                for btn in next:
                    if 'next' in btn.get_attribute('src'):
                        btn.click()
                        break
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
    def extract(self, info):
        href = info.get_attribute('href')
        title = info.text
        md5 = self.makeMD5(href)

        # dict filter
        if md5 in self.d:
            return
        else:
            self.d[md5] = self.date  # 往dict里插入记录
            self.i += 1

        print(href, '====', title)
        handle = self.browser.current_window_handle  # 拿到当前页面的handle
        info.click()

        # switch tab window
        WebDriverWait(self.browser, 10).until(EC.number_of_windows_to_be(2))
        handles = self.browser.window_handles
        for newHandle in handles:
            if newHandle != handle:
                self.browser.switch_to.window(newHandle)  # 切换到新标签
                sleep(1)  # 等个几秒钟
                self.source = self.getPageText()  # 拿到网页源码
                self.browser.close()  # 关闭当前标签页
                self.browser.switch_to.window(handle)  # 切换到之前的标签页
                break

        # try:
        #     self.write_new_file(href, title, self.source, self.i, self.date, 414705)
        # except (NoSuchElementException, NoSuchAttributeException) as e:
        #     print('Element error:', e)
        # except Exception:
        #     return

    # 生成md5信息
    def makeMD5(self, title):
        m = hashlib.md5()
        b = title.encode(encoding = 'utf-8')
        m.update(b)
        enc = m.hexdigest()

        return enc

    def getPageText(self):
        try:
            imgHtml = self.browser.find_element_by_css_selector('body > div.main > table > tbody > tr:nth-child(2) > td > div:nth-child(5)').get_attribute('innerHTML')
            img = imgHtml.replace('src="csjrb', 'src="http://epaper.csjrw.cn/csjrb')
        except NoSuchElementException:
            img = ''

        content = img + self.browser.find_element_by_css_selector('div#zoom').text

        return content

if __name__ == '__main__':
    c = Csjrb()
    c.crawl()
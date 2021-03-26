# -*- coding: utf-8 -*-

import time, hashlib, os, json
from time import sleep
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Common_epaper:
    def __init__(self, d):
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        self.date = time.strftime('%Y-%m-%d %H:%M:%S', timeArray)
        self.d = d
        self.dir = self._dir = ''
        self.debug = True

    def analysis(self):
        jsonFile = './weblist.json'
        with open(mode = 'r', file = jsonFile, encoding = 'utf-8') as f:
            jsonStr = json.load(f)

        webKeyword = './web_kw.txt'
        with open(mode = 'r', file = webKeyword, encoding = 'utf-8') as f:
            keywords = f.read().splitlines()

        for keyword in keywords:
            try:
                key = jsonStr[keyword]
                tag = key[0]
                if '中国经营报' == keyword:
                    if '1' == tag:
                        self.normalCrawl(key)
                    elif '2' == tag:
                        self.specific(key)
            except KeyError:
                continue


    def normalCrawl(self, key):
        self.browser = webdriver.Firefox()
        self.browser.set_window_position(x = 630, y = 0)
        self.i = 0
        status = False

        try:
            self.browser.get(key[1])
            sleep(2)
        except TimeoutException:
            return 'interrupt', 'none', 'error'

        loop = self.browser.find_elements_by_css_selector(key[2])   # 版面的循环
        nextLen = len(loop)

        if nextLen == 0:
            nextLen = 1

        for i in range(nextLen):
            newsList = self.browser.find_elements_by_css_selector(key[3])   # 当前一版内的循环
            for item in newsList:
                href = item.find_element_by_css_selector(key[4]).get_attribute('href')
                md5 = self.makeMD5(href)
                # dict filter
                if md5 in self.d:
                    status = True
                    break
                else:
                    self.d[md5] = self.date.split(' ')[0]  # 往dict里插入记录
                    self.i += 1
                    self.extract(item, href, key)

            if status:
                break

            try:
                self.i = 0
                self.browser.find_element_by_partial_link_text('下一版').click()
                sleep(1)
            except NoSuchElementException:
                break


        if self.i > 0:
            self.browser.quit()
            # self.rename()
            # self.expire()

            return 'complete', self.source, 'ok'
        else:
            self.browser.quit()
            return 'complete', 'none', 'ok'


    # 提取信息，一条的
    def extract(self, item, href, key):
        try:
            title = item.text
            self.browser.get(href)
            sleep(2)
            self.source = self.getPageText(key)         # 拿到网页源码
            print(href, title)
            # self.write_new_file(href, title, self.source, self.i, self.date, key[6])
            self.browser.back()

            return

            handle = self.browser.current_window_handle  # 拿到当前页面的handle
            item.click()

            # switch tab window
            WebDriverWait(self.browser, 10).until(EC.number_of_windows_to_be(2))
            handles = self.browser.window_handles
            for newHandle in handles:
                if newHandle != handle:
                    self.browser.switch_to.window(newHandle)    # 切换到新标签
                    sleep(2)                                    # 等个几秒钟
                    self.source = self.getPageText(key)         # 拿到网页源码
                    self.browser.close()                        # 关闭当前标签页
                    self.browser.switch_to.window(handle)       # 切换到之前的标签页
                    break
            print(href, title)
            # self.write_new_file(href, title, self.source, self.i, self.date, key[6])
        except (NoSuchElementException, NoSuchAttributeException) as e:
            print('Element error:', e)
        except Exception:
            return


    def specific(self, key):
        chapters = self.browser.find_elements_by_css_selector(key[1])
        for i in range(len(chapters)):
            chapter = self.browser.find_elements_by_css_selector(key[1])[i]
            info = chapter.find_element_by_tag_name('a')
            if i > 0:
                info.click()

            newsList = self.browser.find_elements_by_css_selector(key[2])

            for j in range(len(newsList)):
                item = self.browser.find_elements_by_css_selector(key[3])[j]
                self.extractSpec(item, key)

    # 特殊抓取一例
    def extractSpec(self, info, key):
        a = info.find_element_by_tag_name('a')
        href = a.get_attribute('href')
        title = a.text.strip()
        md5 = self.makeMD5(title)

        # dict filter
        if md5 in self.d:
            return
        else:
            self.d[md5] = self.date  # 往dict里插入记录
            self.i += 1

        a.click()
        self.source = self.getPageText(key)         # 拿到网页源码
        sleep(1)  # 等个几秒钟
        print(href, title)
        self.browser.back()  # 关闭当前标签页
        sleep(1)


    # 生成md5信息
    def makeMD5(self, title):
        m = hashlib.md5()
        b = title.encode(encoding = 'utf-8')
        m.update(b)
        enc = m.hexdigest()

        return enc


    def getPageText(self, key):  # 获取网页正文，可以使用通用模版
        try:
            html = self.browser.find_element_by_css_selector(key[5]).get_attribute('innerHTML')
        except NoSuchElementException:
            html = self.browser.page_source

        return html




if __name__ == '__main__':
    c = Common_epaper({})
    c.analysis()
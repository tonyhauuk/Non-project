# -*- coding: utf-8 -*-

import time, datetime, re, hashlib, os, sys
from time import sleep
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# import crawlerfun

class Cyol:
    def __init__(self, d):
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        self.date = time.strftime('%Y-%m-%d %H:%M:%S', timeArray)
        self.projectName = 'food'
        self.d = d
        self.dir = self._dir = self.source = ''
        self.debug = True


    def crawl(self):
        print('\n', '-' * 10, 'http://cyol.com/', '-' * 10, '\n')
        self.i = self.total = 0
        self.browser = webdriver.Firefox()
        self.browser.set_window_position(x = 630, y = 0)
        n = 0

        webLst = [
            'http://qnck.cyol.com/',
            'http://zqb.cyol.com/',
            'http://qnzj.cyol.com/',
            'http://qnsx.cyol.com/']

        for url in webLst:
            self.i = 0
            try:
                self.browser.get(url)
                sleep(5)
            except TimeoutException:
                return


            pageList = self.browser.find_elements(by = By.CSS_SELECTOR, value = 'div#pageList > ul > li')
            print(len(pageList))
            for i in range(len(pageList)):
                item = self.browser.find_elements(by = By.CSS_SELECTOR, value = 'div#pageList > ul > li')[i]
                listName = item.find_element(by = By.TAG_NAME, value = 'a').text

                itemList = self.browser.find_elements(by = By.CSS_SELECTOR, value = '#titleList > ul > li')
                for j in range(len(itemList) - 1):
                    if self.i == 0:
                        self.browser.find_element(by = By.CSS_SELECTOR, value = '#titleList > ul > li:nth-child(1)').click()

                    self.extract()
                    try:
                        self.browser.find_element(by = By.PARTIAL_LINK_TEXT, value = '下一篇').click()
                    except NoSuchElementExccomnewseption:
                        print('click return')
                        self.i = 0
                        self.browser.find_element(by = By.PARTIAL_LINK_TEXT, value = '返回目录').click()

                continue
                if '01版' in listName:
                    if self.i == 0:
                        self.browser.find_element(by = By.CSS_SELECTOR, value = '#titleList > ul > li:nth-child(1)').click()

                    self.extract()
                    try:
                        self.browser.find_element(by = By.PARTIAL_LINK_TEXT, value = '下一篇').click()
                    except NoSuchElementException:
                        self.i = 0
                        self.browser.find_element(by = By.PARTIAL_LINK_TEXT, value = '返回目录').click()
                else:
                    item.find_element(by = By.TAG_NAME, value = 'a').click()
                    if self.i == 0:
                        self.browser.find_element(by = By.CSS_SELECTOR, value = '#titleList > ul > li:nth-child(1)').click()

                    self.extract()
                    try:
                        self.browser.find_element(by = By.PARTIAL_LINK_TEXT, value = '下一篇').click()
                    except NoSuchElementException:
                        self.i = 0
                        self.browser.find_element(by = By.PARTIAL_LINK_TEXT, value = '返回目录').click()



            if self.total > 0:
                # self.rename()
                # self.expire()

                return self.total
            else:
                return 0


    # 提取信息，一条的
    def extract(self):
        try:
            link = self.browser.current_url
            md5 = self.makeMD5(link)

            # dict filter
            if md5 in self.d:
                return
            else:
                self.d[md5] = self.date.split(' ')[0]  # 往dict里插入记录
                self.i += 1
                self.total += 1

            title = self.browser.find_element(By.CSS_SELECTOR, value = 'div.list_t > div > h1').text

            self.source = self.getPageText()

            print(link, title)
            sleep(1)
            # self.write_new_file(link, title, self.source, self.i, self.date, 855436)
        except (NoSuchElementException, NoSuchAttributeException) as e:
            print('Element error:', e)
        except Exception:
            return


    def getPageText(self, ):  # 获取网页正文
        try:
            html = self.browser.find_element(By.CSS_SELECTOR, value = 'div#ozoom').get_attribute('innerHTML')
        except NoSuchElementException:
            html = self.browser.page_source

        return html


    # 生成md5信息
    def makeMD5(self, link):
        m = hashlib.md5()
        b = link.encode(encoding = 'utf-8')
        m.update(b)
        enc = m.hexdigest()

        return enc


if __name__ == '__main__':
    chanye = Cyol({})
    chanye.crawl()

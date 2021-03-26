# -*- coding: utf-8 -*-

import time, datetime, re, hashlib, os, sys
from time import sleep
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#import crawlerfun

class BjNews:
    def __init__(self, d):
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        self.date = time.strftime('%Y-%m-%d %H:%M:%S', timeArray)
        self.projectName = 'food'
        self.d = d
        self.dir = self._dir = self.source = ''
        self.debug = True


    def crawl(self):
        print('\n', '-' * 10, 'https://www.bjnews.com.cn/', '-' * 10, '\n')
        self.i = self.total = 0
        self.browser = webdriver.Firefox()
        self.browser.set_window_position(x = 630, y = 0)
        n = 0

        keywords = ['jiandangbainian', 'video', 'depth', 'news', 'beijing', 'guoji', 'point', 'financial', 'industrial', 'entertainment', 'culture', 'spotrs', 'car', 'estate', 'wine', 'education', 'life', 'photo', 'technology', 'country', 'thinktank']

        for keyword in keywords:
            try:
                url = 'https://www.bjnews.com.cn/' + keyword
                self.browser.get(url)
            except TimeoutException:
                n = -1
                break

            while True:
                newsList = self.browser.find_elements_by_css_selector('div#waterfall-container > div.hotlist')
                for item in newsList:
                    ifZT = False
                    link = item.find_element_by_css_selector('div.pin_demo > a').get_attribute('href')

                    try:
                        item.find_element_by_css_selector('span.zt_tit')
                        ifZT = True
                    except NoSuchElementException:
                        pass

                    current = int(time.time())
                    if ifZT:
                        try:
                            dateTime = link.split('newSubject/')[1][0:10]
                        except IndexError:
                            dateTime = link.split('subject/1/')[1][0:10]

                        dateTime = int(dateTime)
                        if dateTime < current - 86400:
                            self.extract(item, link, 1)
                        else:
                            self.i += 1
                            continue
                    else:
                        dateTime = link.split('detail/')[1].replace('.html', '')[0:10]
                        dateTime = int(dateTime)
                        if dateTime < current - 86400:
                            self.extract(item, link, 2)
                        else:
                            break

                if self.i < len(newsList):
                    break
                else:
                    try:
                        self.browser.find_element_by_partial_link_text('下一页').click()
                        self.i = 0
                    except:
                        break


        print('quantity:', self.total, '\n')
        if n == 0:
            if self.total > 0:
                # self.rename()
                # self.expire()
                # self.deleteFiles()

                return 'complete', self.source, 'ok'
            else:
                return 'complete', 'none', 'ok'
        else:
            return 'interrupt', 'none', 'error'


    # 提取信息，一条的
    def extract(self, item, link, tag):
        try:
            if tag == 1:
                titleInfo = item.find_element_by_css_selector('div.pin_tit').replace('专题', '')
            elif tag == 2:
                titleInfo = item.find_element_by_css_selector('div.pin_tit')


            md5 = self.makeMD5(link)

            # dict filter
            if md5 in self.d:
                return
            else:
                self.d[md5] = self.date.split(' ')[0]  # 往dict里插入记录
                self.i += 1
                self.total += 1


            title = titleInfo.text

            handle = self.browser.current_window_handle  # 拿到当前页面的handle
            titleInfo.click()

            # switch tab window
            WebDriverWait(self.browser, 10).until(EC.number_of_windows_to_be(2))
            handles = self.browser.window_handles
            for newHandle in handles:
                if newHandle != handle:
                    self.browser.switch_to.window(newHandle)        # 切换到新标签
                    sleep(2)                                        # 等个几秒钟
                    self.source = self.getPageText(tag)             # 拿到网页源码
                    self.browser.close()                            # 关闭当前标签页
                    self.browser.switch_to.window(handle)           # 切换到之前的标签页
                    break

            print(link, title)
            # self.write_new_file(link, title, self.source, self.i, self.date, 855436)
        except (NoSuchElementException, NoSuchAttributeException) as e:
            print('Element error:', e)
        except Exception:
            return


    def getPageText(self, tag):  # 获取网页正文
        try:
            if tag == 1:
                try:
                    self.browser.find_element_by_css_selector('span.descBtn').click()
                except:
                    pass
                html = self.browser.find_element_by_css_selector('div.newsubject-desc').get_attribute('innerHTML').replace('收起', '')
            elif tag == 2:
                html = self.browser.find_element_by_css_selector('div#contentStr').get_attribute('innerHTML')
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
    chanye = BjNews({})
    chanye.crawl()
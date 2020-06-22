# -*- coding: utf-8 -*-

import time, hashlib, os
from time import sleep
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Hbxw:
    def __init__(self, d):
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        self.date = time.strftime('%Y-%m-%d %H:%M:%S', timeArray)
        self.d = d
        self.dir = self._dir = ''
        self.debug = True


    def crawl(self):
        self.browser = webdriver.Firefox()
        self.browser.set_window_position(x = 600, y = 0)

        file = 'weblist.txt'
        with open(file, mode = 'r') as f:
            url = f.readlines()
            for x in url:
                self.doCrawl(x)



    def doCrawl(self, url):
        self.total = 0
        try:
            self.browser.get(url)
        except TimeoutException:
            return 'interrupt', 'none', 'error'

        # self.browser.find_element_by_xpath('/html/body').send_keys(Keys.END)
        # sleep(1)
        # self.browser.find_element_by_xpath('/html/body').send_keys(Keys.HOME)

        for i in range(1):
            newsList = self.browser.find_elements_by_css_selector('div.list > ul > li')
            for item in newsList:
                dateTime = item.find_elements_by_css_selector('p > span')[1].text
                if '前' in dateTime or '刚' in dateTime:
                    self.extract(item)
                else:
                    if i == 0:  # 第一页有可能会有不是按时间排序的文章，所以在第一页直接略过，不跳出大循环
                        continue
                    else:
                        break

            if self.total < len(newsList) and i > 1:  # 如果当前抓取的数量小于页面展示的数量并且在第一页，就不翻页了
                break
            else:
                self.browser.find_element_by_css_selector('div#pagination > ul > li.next > a').click()  # 点击下一页
                sleep(2)


    # 提取信息，一条的
    def extract(self, item):
        titleInfo = item.find_element_by_tag_name('h3')
        title = titleInfo.text
        try:
            md5 = self.makeMD5(title)
            # dict filter
            if md5 in self.d:
                return
            else:
                self.d[md5] = self.date.split(' ')[0]  # 往dict里插入记录
                self.total += 1

            handle = self.browser.current_window_handle  # 拿到当前页面的handle
            titleInfo.click()

            # switch tab window
            WebDriverWait(self.browser, 10).until(EC.number_of_windows_to_be(2))
            handles = self.browser.window_handles
            for newHandle in handles:
                if newHandle != handle:
                    self.browser.switch_to.window(newHandle)                # 切换到新标签
                    sleep(2)                                                # 等个几秒
                    self.href = self.browser.current_url                    # 获取当前链接
                    self.source, self.time = self.getPageText()             # 拿到网页源码
                    self.browser.close()                                    # 关闭当前标签页
                    self.browser.switch_to.window(handle)                   # 切换到之前的标签页
                    break

            # self.write_new_file(href, title, self.source, self.i, self.time)
        except (NoSuchElementException, NoSuchAttributeException) as e:
            print('Element error:', e)
        except Exception:
            pass


    def getPageText(self):  # 获取网页正文
        html = self.browser.find_element_by_css_selector('div.con').get_attribute('innerHTML')
        publishTime = self.browser.find_element_by_css_selector('div.xilan > div.head > p > span').text

        return html, publishTime.replace('发布', '')


    # 生成md5信息
    def makeMD5(self, title):
        m = hashlib.md5()
        b = title.encode(encoding = 'utf-8')
        m.update(b)
        enc = m.hexdigest()

        return enc


if __name__ == '__main__':
    h = Hbxw({})
    h.crawl()
# -*- coding: utf-8 -*-

import time, hashlib, os, re
from time import sleep
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class Investorscn:
    def __init__(self, d):
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        self.date = time.strftime('%Y-%m-%d %H:%M:%S', timeArray)
        self.d = d
        self.dir = self._dir = ''
        self.debug = True


    def crawl(self):
        print('\n', '-' * 10, 'http://www.investorscn.com/', '-' * 10, '\n')

        status = True
        self.browser = webdriver.Firefox()
        self.browser.set_window_position(x = 620, y = 0)
        self.total = 0
        i = 0
        status = True
        file = 'investorscn_weblist.txt'
        with open(file, mode = 'r') as f:
            url = f.readlines()
            for x in url:
                n = self.doCrawl(x)
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



    def doCrawl(self, url):
        self.i = 0
        try:
            self.browser.get(url)
            sleep(2)
        except TimeoutException:
            return -1

        while True:
            newsList = self.browser.find_elements(by = By.CSS_SELECTOR, value = 'div.tcft_left > div.rwbox')
            for item in newsList:
                dateTime = item.find_element(by = By.CSS_SELECTOR, value = 'h4.date-time > span').text

                if dateTime in self.date:
                    self.extract(item)
                else:
                    break

            if self.i < len(newsList):  # 如果当前采集的数量小于当前页的条数，就不翻页了
                break
            else:
                try:
                    self.browser.find_element(by = By.PARTIAL_LINK_TEXT, value = '下一页').click()  # 点击下一页
                    self.i = 0
                except:
                    break

        if self.total > 0:
            # crawlerfun.renameNew()
            # crawlerfun.expire(self.date, self.d, self.projectName)

            return self.total
        else:
            return 0


    # 提取信息，一条的
    def extract(self, item):
        try:
            titleInfo = item.find_element(by = By.CSS_SELECTOR, value = 'h2 > a')
            title = titleInfo.text
            md5 = self.makeMD5(title)

            # dict filter
            if md5 in self.d:
                return
            else:
                self.d[md5] = self.date.split(' ')[0]  # 往dict里插入记录
                self.i += 1

            handle = self.browser.current_window_handle  # 拿到当前页面的handle
            titleInfo.click()

            # switch tab window
            WebDriverWait(self.browser, 10).until(EC.number_of_windows_to_be(2))
            handles = self.browser.window_handles
            for newHandle in handles:
                if newHandle != handle:
                    self.browser.switch_to.window(newHandle)    # 切换到新标签
                    sleep(2)                                    # 等个几秒钟
                    self.source, url = self.getPageText()       # 拿到网页源码
                    self.browser.close()                        # 关闭当前标签页
                    self.browser.switch_to.window(handle)       # 切换到之前的标签页
                    break

            print('count:', self.i, ' --- ', title)

            # self.write_new_file(url, title, self.source, self.i, 1159081)
        except Exception:
            return


    def getPageText(self):  # 获取网页正文
        url = self.browser.current_url
        try:
            html = self.browser.find_element(by = By.CSS_SELECTOR, value = 'div.content').get_attribute('innerHTML')
        except NoSuchElementException:
            html = self.browser.page_source

        return html, url


    # 生成md5信息
    def makeMD5(self, link):
        m = hashlib.md5()
        b = link.encode(encoding = 'utf-8')
        m.update(b)
        enc = m.hexdigest()

        return enc


    # 删除过期的记录
    def expire(self):
        # 检查过期数据
        li = []
        current = self.date.split(' ')[0]
        for k, v in self.d.items():
            if current != v:
                li.append(k)

        # 删除字典里过期的数据
        for i in li:
            self.d.pop(i)

        # 更新txt文件
        try:
            fileName = '/home/zran/src/crawler/33/manzhua/crawlpy3/record/hbxw_md5.txt'
            os.remove(fileName)
            with open(fileName, 'a+') as f:
                f.write(str(self.d))
        except Exception as e:
            print(e)


    # 重新修改文件夹名称
    def rename(self):
        try:
            root = '/estar/newhuike2/1/'
            lst = os.listdir(root)
            for l in lst:
                if '_' in l:
                    os.rename(root + l, root + l.strip('_'))
        except:
            pass


    def initDict(self):
        d = {}
        file = '/home/zran/src/crawler/33/manzhua/crawlpy3/record/hbxw_md5.txt'
        try:
            with open(file, mode = 'r') as f:
                line = f.readline()
                if line != '':
                    d = eval(str(line))  # 直接把字符串转成字典格式

            return d
        except:
            # 如果没有文件，则直接创建文件
            fd = open(file, mode = 'a+', encoding = 'utf-8')
            fd.close()

            return d


if __name__ == '__main__':
    i = Investorscn({})
    i.crawl()

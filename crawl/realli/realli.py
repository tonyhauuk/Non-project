# -*- coding: utf-8 -*-

import time, datetime, re, hashlib, os, sys
from time import sleep
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#import crawlerfun

class Realli:
    def __init__(self, d):
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        self.date = time.strftime('%Y-%m-%d %H:%M:%S', timeArray)
        self.d = d
        self.dir = self._dir = self.source = ''
        # self.ipnum = crawlerfun.ip2num('61.130.181.229')
        self.debug = True


    def crawl(self):
        print('\n', '-' * 10, 'https://realli.org/#/', '-' * 10, '\n')
        self.i = 0
        self.browser = webdriver.Firefox()
        self.browser.set_window_position(x = 680, y = 0)
        n = 0

        keywords = ['', 'report']

        for keyword in keywords:
            self.keyword = keyword
            try:
                url = 'https://realli.org/#/' + keyword
                self.browser.get(url)
            except TimeoutException:
                n = -1
                break

            for i in range(5):
                if keyword == '':
                    newsList = self.browser.find_elements_by_css_selector('div.posts > div.post.multi')
                    length = len(newsList)

                    for i in range(length):
                        item = self.browser.find_elements_by_css_selector('div.posts > div.post.multi')[i]
                        dateTime = item.find_element_by_css_selector('div.post__oper > span:nth-child(3)').text
                        if '前' in dateTime:
                            self.extract(item)
                        else:
                            break
                elif keyword == 'report':
                    newsList = self.browser.find_elements_by_css_selector('ul.list > li')
                    length = len(newsList)

                    for i in range(length):
                        item = self.browser.find_elements_by_css_selector('ul.list > li')[i]
                        pubTime = item.find_element_by_css_selector('div.info > div.oper > span:nth-child(4)').text
                        dateTime = pubTime.replace('发布', '')
                        if dateTime in self.date:
                            self.extract(item)
                        else:
                            break


                # if self.i < length:
                #     break
                # else:
                #     try:
                #         self.browser.find_element_by_css_selector('div.more_con > a').click()
                #     except NoSuchElementException:
                #         break


        print('quantity:', self.i)
        if n == 0:
            if self.i > 0:
                # self.rename()
                # self.expire()
                # self.deleteFiles()

                return 'complete', self.source, 'ok'
            else:
                return 'complete', 'none', 'ok'
        else:
            return 'interrupt', 'none', 'error'


    # 提取信息，一条的
    def extract(self, item):
        titleInfo = item.find_element_by_css_selector('div.post__title')
        title = titleInfo.text
        try:
            md5 = self.makeMD5(title)

            # dict filter
            if md5 in self.d:
                return
            else:
                self.d[md5] = self.date.split(' ')[0]  # 往dict里插入记录
                self.i += 1


            titleInfo.click()
            self.source, href = self.getPageText()

            # self.write_new_file(href, title, self.source, self.i, self.date, 1161565)
            self.browser.back()
            sleep(2)
        except Exception:
            self.i -= 1
            return


    def getPageText(self):  # 获取网页正文
        try:
            pageHTML = self.browser.find_element_by_css_selector('div.detail').get_attribute('innerHTML')
        except NoSuchElementException:
            pageHTML = self.browser.page_source

        link = self.browser.current_url

        return pageHTML, link


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
            fileName = '/home/zran/src/crawler/33/manzhua/crawlpy3/record/cnstock_md5.txt'
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

    def deleteFiles(self):
        filePath = '/root/estar_save/cnstock/'
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        current = time.strftime("%Y-%m-%d", timeArray)
        name = os.listdir(filePath)

        for i in name:
            try:
                fileName = filePath + i
                fileInfo = os.stat(fileName)
            except FileNotFoundError:
                continue
            ts = fileInfo.st_mtime
            timeArr = time.localtime(ts)
            date = time.strftime("%Y-%m-%d", timeArr)
            if current != date:
                os.remove(fileName)


if __name__ == '__main__':
    r = Realli({})
    r.crawl()
# -*- coding: utf-8 -*-

import time, hashlib, os
from time import sleep
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import crawlerfun

class Liuyan_people:
    def __init__(self, browser):
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        self.date = time.strftime('%Y-%m-%d %H:%M:%S', timeArray)
        self.projectName = 'liuyan_people'
        self.d = crawlerfun.initDict(self.projectName)
        self.browser = browser
        self.dir = self._dir = self.source = ''
        self.ipnum = crawlerfun.ip2num('205.185.126.45')
        self.debug = True


    def crawl(self):
        print('\n', '-' * 10, 'http://liuyan.people.com.cn/', '-' * 10, '\n')
        self.total = 0
        i = 0
        status = True
        file = './record/liuyan_people_weblist.txt'
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
            sleep(5)
        except TimeoutException:
            return -1

        start = 0
        while True:
            newsList = self.browser.find_elements_by_css_selector('ul.replyList > li')
            end = len(newsList)
            for item in newsList[start:end]:
                dateTime = self.addhours(item.find_element_by_css_selector('div.headMainS.fl > p').text.strip())

                if dateTime.split(' ')[0] in self.date:
                    status = self.extract(item)
                    if status:
                        break
                else:
                    break


            if self.i == 0:
                break

            try:
                start = end + 1
                self.browser.find_element_by_css_selector('div.mordList').click()
                sleep(1)
                self.i = 0
            except:
                break


        if self.total > 0:
            crawlerfun.renameNew()
            crawlerfun.expire(self.date, self.d, self.projectName)

            return self.total
        else:
            return 0


    # 提取信息，一条的
    def extract(self, item):
        url = ''
        titleInfo = item.find_element_by_css_selector('div.tabList.fl > h1')
        title = titleInfo.text
        try:
            md5 = crawlerfun.makeMD5(title)

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
                    self.source, url = self.getPageText()                # 拿到网页源码
                    self.browser.close()                            # 关闭当前标签页
                    self.browser.switch_to.window(handle)           # 切换到之前的标签页
                    break

            if url == '':
                return True
            else:
                self.write_new_file(url, title, self.source, self.i, self.date, 92816)
                return False
        except Exception:
            return False


    def getPageText(self):  # 获取网页正文
        try:
            html = self.browser.find_element_by_css_selector('p#replyContentMain').get_attribute('innerHTML')
        except NoSuchElementException:
            html = self.browser.page_source

        return html, self.browser.current_url


    def write_new_file(self, url, title, source, i, time, id):
        content = '''
                <html>
                    <head> 
                       <meta charset="utf-8">
                       <meta name="keywords" content="estarinfo">
                       <title>''' + title + '''</title>
                    </head> 
                    <body>
                        <h1 class="title">''' + title + '''</h1>
                        <span class="time">''' + time + '''</span>
                        <span class="source">''' + str(id) + '''</span>
                        <div class="article">''' + source + '''</div>
                    </body>
                </html>
                '''
        page_text = url + '\n' + title + '\n' + str(id) + '\n\n\n\n' + content

        if self.debug:
            print('count:', self.i, ' --- ', title)

        if '' == self._dir:
            self.crawl_mkdir()

        filename = self._dir + 'iask_' + str(i) + '_' + str(len(self.d)) + '.htm-2'
        for num in range(2):
            if 1 == crawlerfun.write_file(filename, page_text, ifdisplay = 0):
                break
            else:  # 有时目录会被c程序删掉
                crawlerfun.mkdir(self._dir)


    def crawl_mkdir(self):
        dirroot = '/estar/newhuike2/1/'
        tm_s, tm_millisecond = crawlerfun.get_timestamp(ifmillisecond = 1)
        dirsmall = 'iask' + str(self.ipnum) + '.' + str(1) + '.' + str(tm_s) + '.' + str(tm_millisecond) + '/'
        self._dir = dirroot + '_' + dirsmall
        self.dir = dirroot + dirsmall

        return self._dir, self.dir


    def addhours(self, datetime):
        timezone = 15 * 60 * 60
        datetime = datetime.replace('&nbsp;', ' ')
        timeArray = time.strptime(datetime, '%Y-%m-%d %H:%M')
        timeStamp = int(time.mktime(timeArray)) + timezone
        timeArray = time.localtime(timeStamp)
        dateTime = time.strftime('%Y-%m-%d %H:%M', timeArray)

        return dateTime



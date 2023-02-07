# -*- coding: utf-8 -*-

import time, hashlib, os
from time import sleep
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import crawlerfun


class SouthernGrid:
    def __init__(self, browser):
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        self.projectName = 'south_grid'
        self.date = time.strftime('%Y-%m-%d %H:%M:%S', timeArray)
        self.d = crawlerfun.initDict(self.projectName)
        self.browser = browser.driver
        self.dir = self._dir = self.source = ''
        self.ipnum = crawlerfun.ip2num(browser.ip)
        self.debug = True


    def crawl(self):
        print('\n' ,'-' * 10, 'http://www.bidding.csg.cn/zbcg/index.jhtml', '-' * 10, '\n')
        self.i = self.total = 0
        page = 1
        self.browser.get('http://www.bidding.csg.cn/zbcg/index.jhtml')
        sleep(5)

        while True:     # 翻页循环
            newsList = self.browser.find_elements_by_css_selector('div.List2 > ul > li')
            for i in range(len(newsList)):
                item = self.browser.find_elements_by_css_selector('div.List2 > ul > li')[i]
                dateTime = item.find_element_by_css_selector('span.Black14.Gray').text
                if dateTime in self.date:
                    self.extract(item)
                else:
                    if page == 1:
                        continue        # 南方电网第一页会有老的信息，所以遇到时间不匹配直接跳过，继续往下采
                    else:
                        break

            if self.i < len(newsList) and page > 1:     # 如果当前页抓取的条数小于看到的条数，并且不在第一页，直接跳出
                break
            else:
                try:
                    self.browser.find_element_by_partial_link_text('下一页').click()   # 翻页
                    sleep(5)
                    self.i = 0
                    page += 1
                except NoSuchElementException:
                    break


        print('\nquantity:', self.total)
        if self.total > 0:
            crawlerfun.renameNew()
            crawlerfun.expire(self.date, self.d, self.projectName)

            return 'complete', self.source, 'ok'
        else:
            return 'complete', 'none', 'ok'


    # 提取信息，一条的
    def extract(self, item):
        titleInfo = item.find_element_by_xpath('a[2]')

        try:
            href = titleInfo.get_attribute('href')
            md5 = crawlerfun.makeMD5(href)

            # dict filter
            if md5 in self.d:
                return
            else:
                self.d[md5] = self.date.split(' ')[0]       # 往dict里插入记录
                self.i += 1
                self.total += 1

            titleInfo.click()
            sleep(5)

            self.source, self.title = self.getPageText()  # 拿到网页源码

            self.write_new_file(href, title, self.source, self.total, self.date, 1170773)
            self.browser.back()
            sleep(2)
        except Exception as e:
            self.i -= 1
            self.total -= 1
            return



    def getPageText(self):
        try:
            content = self.browser.find_element_by_css_selector('div.Section0').get_attribute('innerHTML')
        except NoSuchElementException:
            content = self.browser.page_source

        title = self.browser.find_element_by_css_selector('h1.s-title').text

        return content, title


    # 写一个新文章
    def write_new_file(self, url, title, source, i, time, id):
        if self.debug:
            print('count:', i, ' --- ', title)

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

        if '' == self._dir:
            self.zytzb_mkdir()

        filename = self._dir + 'iask_' + str(i) + '_' + str(len(self.d)) + '.htm-2'
        for num in range(2):
            if 1 == crawlerfun.write_file(filename, page_text, ifdisplay = 0):
                break
            else:  # 有时目录会被c程序删掉
                crawlerfun.mkdir(self._dir)


    # 制作电网目录，注意不创建目录，只是生成目录信息
    def zytzb_mkdir(self):
        dirroot = '/estar/newhuike2/1/'
        tm_s, tm_millisecond = crawlerfun.get_timestamp(ifmillisecond = 1)
        dirsmall = 'iask' + str(self.ipnum) + '.' + str(1) + '.' + str(tm_s) + '.' + str(tm_millisecond) + '/'
        self._dir = dirroot + '_' + dirsmall
        self.dir = dirroot + dirsmall

        return self._dir, self.dir



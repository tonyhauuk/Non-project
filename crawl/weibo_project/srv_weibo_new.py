# -*- coding: utf-8 -*-

import time, datetime, re, hashlib, os, sys
from time import sleep
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, date, timedelta
import crawlerfun

from crawlerfun import ClearCache
import time, os, datetime, subprocess
from selenium import webdriver
from selenium.webdriver.opera.options import Options as operaOptions

class Weibo:
    def __init__(self, browser):
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        self.date = time.strftime('%Y-%m-%d %H:%M:%S', timeArray)
        self.projectName = 'weibo'
        self.d = crawlerfun.initDict(self.projectName)
        self.url = browser.url
        self.browser = browser.driver
        self.dir = self._dir = self.source = ''
        self.ipnum = crawlerfun.ip2num(browser.ip)
        self.debug = True


    def crawl(self):
        self.i = 0
        yesterday = (date.today() + timedelta(days = -1)).strftime("%m月%d日")
        n = 0

        keyword = self.url.split('word=')[1]
        url = 'https://s.weibo.com/weibo/' + keyword + '?topnav=1&wvr=6&b=1'
        try:
            self.browser.get(url)
            WebDriverWait(self.browser, 10, 0.5).until(EC.presence_of_element_located((By.ID, 'pl_feedtop_top')))
            sleep(2)
        except TimeoutException:
            n = -1


        newsList = self.browser.find_elements_by_css_selector('div#pl_feedlist_index > div > div.card-wrap')
        for item in newsList:
            mid = item.get_attribute('mid')
            if mid == None:
                continue

            dateTime = item.find_element_by_css_selector('p.from > a:nth-child(1)').text
            self.dateTime = dateTime
            if '小时前' in dateTime or '分钟前' in dateTime or '秒前' in dateTime or '今天' in dateTime or dateTime in yesterday:
                status = self.extract(item)
                if not status:
                    break
            else:
                continue

        print('quantity:', self.i, '\n')
        if n == 0:
            if self.i > 0:
                crawlerfun.renameNew()
                crawlerfun.expire(self.date, self.d, self.projectName)
                return 'complete', self.source, 'ok'
            else:
                return 'complete', 'none', 'ok'
        else:
            return 'interrupt', 'none', 'error'


    # 提取信息，一条的
    def extract(self, item):
        try:
            titleInfo = item.find_element_by_css_selector('p.from > a:nth-child(1)')
            href = titleInfo.get_attribute('href')
            md5 = crawlerfun.makeMD5(href)

            # dict filter
            if md5 in self.d:
                return False
            else:
                self.d[md5] = self.date.split(' ')[0]  # 往dict里插入记录
                self.i += 1

            title = 'aaaaaaa'

            source = item.find_element_by_css_selector('p.txt').get_attribute('innerHTML')
            if '展开全文' in source:
                try:
                    item.find_element_by_css_selector('p.txt > a[action-type="fl_unfold"]').click()
                except:
                    pass
                else:
                    source = item.find_element_by_css_selector('p.txt').get_attribute('innerHTML')

            self.write_new_file(href, title, source, self.i, self.date, 1152935)
            return True
        except Exception:
            return False


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
            print('count:', self.i, '--', url, self.dateTime)

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
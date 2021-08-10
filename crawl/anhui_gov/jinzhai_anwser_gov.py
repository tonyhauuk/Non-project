# -*- coding: utf-8 -*-

import time, hashlib, os
from time import sleep
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import crawlerfun

class Xijiang:
    def __init__(self, browser):
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        self.date = time.strftime('%Y-%m-%d %H:%M:%S', timeArray)
        self.projectName = 'ahjz_gov'
        self.d = crawlerfun.initDict(self.projectName)
        self.url = browser.url
        self.browser = browser.driver
        self.dir = self._dir = self.source = ''
        self.ipnum = crawlerfun.ip2num(browser.ip)
        self.debug = True

    def crawl(self):
        print('\n' ,'-' * 10, 'http://www.ahjinzhai.gov.cn', '-' * 10, '\n')
        self.total = self.i = 0

        url = 'http://www.ahjinzhai.gov.cn/luan/site/tpl/2951?organId=6626851'
        try:
            self.browser.get(url)
        except TimeoutException:
            return -1


        newsList = self.browser.find_elements_by_css_selector('div > ul > li')
        for item in newsList:
            dateTime = item.find_element_by_css_selector('li.date').text

            if dateTime in self.date:
                self.extract(item)
            else:
                break



        print('quantity:', self.total)
        if self.total > 0:
            crawlerfun.renameNew()
            crawlerfun.expire(self.date, self.d, self.projectName)

            return 'complete', self.source, 'ok'
        else:
            return 'complete', 'none', 'ok'


    # Extract one item
    def extract(self, item):
        titleInfo = item.find_element_by_css_selector('a')

        try:
            href = titleInfo.get_attribute('href')
            md5 = crawlerfun.makeMD5(href)

            # dict filter
            if md5 in self.d:
                return
            else:
                self.d[md5] = self.date.split(' ')[0]  # Insert md5 value into the dict
                self.i += 1
                self.total += 1

            title = titleInfo.text

            handle = self.browser.current_window_handle  # Obtain current page handle
            titleInfo.click()

            # switch tab window
            WebDriverWait(self.browser, 10).until(EC.number_of_windows_to_be(2))
            handles = self.browser.window_handles
            for newHandle in handles:
                if newHandle != handle:
                    self.browser.switch_to.window(newHandle)    # Switch new tab
                    sleep(2)                                    # Wait 2 seconds
                    self.source = self.getPageText()            # Download page source
                    self.browser.close()                        # Close current new tab
                    self.browser.switch_to.window(handle)       # Switch to before tab
                    break

            self.write_new_file(href, title, self.source, self.i, self.date, 1172191)
        except Exception as e:
            print('Element error:', e)
            return


    def getPageText(self):
        try:
            html = self.browser.find_element_by_css_selector('div.content').get_attribute('innerHTML')
        except NoSuchElementException:
            html = self.browser.page_source

        return html

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
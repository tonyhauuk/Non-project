# -*- coding: utf-8 -*-

import time, hashlib, os
from time import sleep
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import crawlerfun


class StateGrid:
    def __init__(self, browser):
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        self.projectName = 'grid'
        self.date = time.strftime('%Y-%m-%d %H:%M:%S', timeArray)
        self.d = crawlerfun.initDict(self.projectName)
        self.browser = browser.driver
        self.dir = self._dir = self.source = ''
        self.ipnum = crawlerfun.ip2num(browser.ip)
        self.debug = True


    def crawl(self):
        print('\n', '-' *10, 'https://ecp.sgcc.com.cn/ecp2.0/portal/#', '-'*10, '\n')
        self.i = self.total = 0
        try:
            self.browser.get('https://ecp.sgcc.com.cn/ecp2.0/portal/#/list/list-com/2018032600000014_5_20180502001')
            sleep(5)
        except Exception as e:
            return 'interrupt', 'none', 'error'

        while True:     # 翻页循环
            newsList = self.browser.find_elements_by_css_selector('tbody > tr.cur')
            for item in newsList:
                try:
                    dateTime = item.find_element_by_css_selector('td.time').text
                    print('date time:', dateTime)
                except:
                    continue

                if dateTime in self.date:
                    self.extract(item)
                else:
                    break

            if self.i < len(newsList):
                break
            else:
                try:
                    self.browser.find_element_by_xpath('/html/body/app-root/app-main/app-list/div/app-list-com/div/div/div[2]/div[2]/page/div/div/button[8]').click()  # 翻页
                    self.i = 0
                    sleep(5)
                except NoSuchElementException as e:
                    break


        print('quantity:', self.total)
        if self.total > 0:
            crawlerfun.renameNew()
            crawlerfun.expire(self.date, self.d, self.projectName)

            return 'complete', self.source, 'ok'
        else:
            return 'complete', 'none', 'ok'


    # 提取信息，一条的
    def extract(self, item):
        titleInfo = item.find_element_by_css_selector('td.title > span > label')
        title = item.find_element_by_css_selector('span.fl').get_attribute('title')
        try:
            md5 = crawlerfun.makeMD5(title)

            # dict filter
            if md5 in self.d:
                return
            else:
                self.d[md5] = self.date.split(' ')[0]       # 往dict里插入记录
                self.i += 1
                self.total += 1

            handle = self.browser.current_window_handle     # 拿到当前页面的handle
            titleInfo.click()

            # switch tab window
            WebDriverWait(self.browser, 10).until(EC.number_of_windows_to_be(2))
            handles = self.browser.window_handles
            for newHandle in handles:
                if newHandle != handle:
                    self.browser.switch_to.window(newHandle)        # 切换到新标签
                    sleep(2)                                        # 等个几秒钟
                    self.source, self.href = self.getPageText()     # 拿到网页源码
                    self.browser.close()                            # 关闭当前标签页
                    self.browser.switch_to.window(handle)           # 切换到之前的标签页
                    break

            self.write_new_file(self.href, title, self.source, self.i, self.date, 1170771)
        except Exception:
            return


    def getPageText(self):
        try:
            content = self.browser.find_element_by_css_selector('div#md').get_attribute('innerHTML')
        except NoSuchElementException:
            content = self.browser.page_source

        href = self.browser.current_url

        return content, href



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




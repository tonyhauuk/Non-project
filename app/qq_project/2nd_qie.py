# -*- coding: utf-8 -*-
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException, NoSuchWindowException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time, json
import sys
import os
import hashlib
from os.path import join, getsize
import shutil
from datetime import datetime, date, timedelta
import datetime
# import crawlerfun
# from crawlerfun import DriverElement
# import crawlerfun
import threading


class Qie:
    def __init__(self, browser):
        self.browser = browser
        self.timeStamp = int(time.time())

        self.initDict()
        self.source = ''
        self.debug = True
        self.d = {}



    def crawl(self, url):
        limit = 'ok'
        completed = 'complete'


        try:
            self.browser.get(url)
            # self.browser.find_element_by_css_selector('input#su.bg.s_btn').click()
            # self.browser.refresh()
            # if self.debug:
            #     print(' \t##########  Flush page ########## \n')
        except:
            return 'interrupt', 'none', 'error'

        try:
            if '抱歉，没有找到' in self.browser.page_source:
                return 'complete', 'none', 'ok'
        except:
            return 'interrupt', 'none', 'error'

        try:
            # self.browser.find_element_by_xpath('/html/body').send_keys(Keys.END)
            self.i = 0
            self.total = 0
            page = 0

            while True:
                items = self.browser.find_elements_by_css_selector('div#wrapper_wrapper > div#container > div#content_left > div > div.result')
                if len(items) > 0:
                    for item in items:
                        time = item.find_element_by_css_selector('div.c-summary.c-row p').text

                        if '小时前' in time or '分钟前' in time:
                            self.extract(item)
                        else:
                            year = datetime.datetime.now().year
                            splitDate = time.split(str(year))
                            fullTime = str(year) + splitDate[1]
                            ts = self.calcDate(fullTime)
                            oneDay = 60 * 60 * 24 * 5

                            if self.timeStamp - ts < oneDay:
                                self.extract(item)
                            else:
                                break

                    if self.i == 0:
                        return '1complete', 'none', 'ok'

                    try:
                        if page == 11:
                            break

                        if self.i == 10:
                            self.browser.find_element_by_partial_link_text('下一页').click()
                            # self.browser.find_element_by_css_selector('html body div#wrapper.wrapper_l p#page > a.n').click()
                            if self.debug:
                                print('翻页...... page: ', page + 2)

                            page += 1
                        else:
                            break
                    except NoSuchElementException:
                        break

                    self.i = 0

            # if self.total > 0 and self.savetype == 'python':
            #     crawlerfun.rename(self._dir, self.dir)

            return completed, self.source, limit
        except Exception:
            return 'complete', 'none', 'ok'

    # 提取信息，一条的
    def extract(self, item):
        try:
            interval = 2
            current = int(time.time())
            content = item.find_element_by_css_selector('div.result h3.c-title a')
            href = content.get_attribute('href')

            if 'new.qq.com/rain'  in href or 'new.qq.com/omn'  in href:

                print(href)
                md5 = self.makeMD5(href)

                # dict filter
                if md5 in self.d:
                    return
                else:
                    self.d[md5] = str(current)  # 往dict里插入记录
                    self.i += 1
                    self.total += 1

                title = content.text
                handle = self.browser.current_window_handle
                content.click()

                # switch tab window
                handles = self.browser.window_handles
                for newHandle in handles:
                    if newHandle != handle:
                        self.browser.switch_to.window(newHandle)
                        if self.debug:
                            print('count: ', self.total)
                        time.sleep(interval)
                        self.source = self.browser.page_source
                        self.browser.close()
                        self.browser.switch_to.window(handles[0])

                # self.writeFile(objStr, current, self.i)
                # self.write_new_file(href, title, self.source, self.i)
        except (NoSuchElementException, NoSuchAttributeException) as e:
            print('Element error:', e)
        except Exception as ex:
            print(ex)

    # 生成md5
    def makeMD5(self, link):
        m = hashlib.md5()
        b = link.encode(encoding='utf-8')
        m.update(b)
        link = m.hexdigest()

        return link


    def initDict(self):
        file = './qie.txt'
        try:
            with open(file, mode='r') as f:
                line = f.readline()
                if line != '' or line != '{}':
                    self.d = eval(str(line))  # 直接把字符串转成字典格式
        except:
            # 如果没有文件，则直接创建文件
            fd = open(file, mode='a+', encoding='utf-8')
            fd.close()


    def calcDate(self, fullTime):
        time1 = fullTime + ':00'
        timeArr = time.strptime(time1, "%Y年%m月%d日 %H:%M:%S")
        timeStamp = int(time.mktime(timeArr))

        return timeStamp


    def quit(self):
        self.browser.quit()


if __name__ == '__main__':

    opts = webdriver.FirefoxOptions()
    browser = webdriver.Firefox()

    process = Qie(browser)
    try:
        keyword = ['微软', '金融', 'nvidia']

        while True:
            url = 'https://www.baidu.com/s?tn=news&rtt=4&bsst=1&cl=2&wd=site%3Aqq.com+' + keyword[0] + '&medium=0'
            obj = process.crawl(url)
            # print(obj)
            time.sleep(10)
            break

    except TimeoutException:
        print('The connection has timed out!')
    finally:
        process.quit()

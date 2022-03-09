# -*- coding: utf-8 -*-

import time, datetime, re, hashlib, os, sys
from time import sleep
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, date, timedelta
#import crawlerfun

class Weibo:
    def __init__(self, d):
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        self.date = time.strftime('%Y-%m-%d %H:%M:%S', timeArray)
        self.timeStamp = int(time.time())
        self.projectName = 'weibo'
        self.d = d
        self.dir = self._dir = self.source = ''
        # self.ipnum = crawlerfun.ip2num('61.130.181.229')
        self.debug = True


    def crawl(self):
        self.i = self.total = 0
        yesterday = (date.today() + timedelta(days = -1)).strftime("%m月%d日")
        self.browser = webdriver.Firefox()
        self.browser.set_window_position(x = 630, y = 0)
        n = 0
        url = 'https://s.weibo.com/weibo/%25E6%25B5%25B7%25E5%25B0%2594?topnav=1&wvr=6&b=1'
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
            if '小时前' in dateTime or '分钟前' in dateTime or '秒前' in dateTime or '今天' in dateTime or dateTime in yesterday:
                status = self.extract(item)
                if not status:
                    break
            else:
                continue

        print('quantity:', self.total, '\n')
        if n == 0:
            if self.total > 0:

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
            md5 = self.makeMD5(href)

            # dict filter
            if md5 in self.d:
                return False
            else:
                self.d[md5] = self.date.split(' ')[0]  # 往dict里插入记录
                self.i += 1
                self.total += 1

            title = 'aaaaaaa'

            source = item.find_element_by_css_selector('p.txt').get_attribute('innerHTML')
            if '展开全文' in source:
                try:
                    item.find_element_by_css_selector('p.txt > a[action-type="fl_unfold"]').click()
                except:
                    pass
                else:
                    source = item.find_element_by_css_selector('p.txt').get_attribute('innerHTML')


            print(title, href)
            # self.write_new_file(href, title, source, self.i, self.date, 1152935)
            return True
        except Exception:
            return False




    # 生成md5信息
    def makeMD5(self, link):
        m = hashlib.md5()
        b = link.encode(encoding = 'utf-8')
        m.update(b)
        enc = m.hexdigest()

        return enc





if __name__ == '__main__':
    a = Weibo({})
    a.crawl()
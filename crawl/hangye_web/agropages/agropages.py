# -*- coding: utf-8 -*-

import time, requests, bs4, datetime, re, hashlib, os, sys, json
from time import sleep
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from w3lib import html
from w3lib.html import remove_comments


class Agro:
    def __init__(self, d):
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        self.date = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        self.d = d
        self.dir = self._dir = ''
        # self.ipnum = crawlerfun.ip2num('61.130.181.229')
        self.debug = True


    def crawl(self):
        self.i = self.total = 0
        self.browser = webdriver.Firefox()
        self.browser.set_window_position(x = 700, y = 0)
        try:
            self.browser.get('http://cn.agropages.com/News/NewsList.htm')
        except TimeoutException:
            return 'interrupt', 'none', 'error'

        self.browser.find_element_by_xpath('/html/body').send_keys(Keys.END)
        self.browser.find_element_by_xpath('/html/body').send_keys(Keys.HOME)

        while True:
            newsList = self.browser.find_elements_by_css_selector('div.newslist > ul.cb > li.clearfix')
            for item in newsList:
                dateTime = item.find_element_by_css_selector('dl > dd > p > span').text
                if dateTime in self.date:
                    self.extract(item)


            if self.i < len(newsList):  # 如果当前采集的数量小于当前页的条数，就不翻页了
                break
            else:
                # 点击下一页
                btn = self.browser.find_elements_by_css_selector('div#bodyContent_AspPagerShop > a')
                for a in btn:
                    if a.text == '下一页':
                        a.click()
                        break

        if self.total > 0:
            # self.rename()
            # self.expire()

            return 'complete', str(self.total), 'ok'


    # 提取信息，一条的
    def extract(self, item):
        titleInfo = item.find_element_by_css_selector('dl > dd > h3 > a')
        try:
            href = titleInfo.get_attribute('href')
            md5 = self.makeMD5(href)

            # dict filter
            if md5 in self.d:
                return
            else:
                self.d[md5] = self.date.split(' ')[0]  # 往dict里插入记录
                self.i += 1
                self.total += 1

            title = titleInfo.text

            handle = self.browser.current_window_handle  # 拿到当前页面的handle
            titleInfo.click()

            # switch tab window
            WebDriverWait(self.browser, 10).until(EC.number_of_windows_to_be(2))
            handles = self.browser.window_handles
            for newHandle in handles:
                if newHandle != handle:
                    self.browser.switch_to.window(newHandle)    # 切换到新标签
                    sleep(2)                                    # 等个几秒钟
                    self.source = self.getPageText()            # 拿到网页源码
                    self.browser.close()                        # 关闭当前标签页
                    self.browser.switch_to.window(handle)       # 切换到之前的标签页
                    break

            # self.write_new_file(href, title, self.source, self.i, self.date)
        except (NoSuchElementException, NoSuchAttributeException) as e:
            print('Element error:', e)
        except Exception:
            pass


    def getPageText(self):  # 获取网页正文
        pageTitle = self.browser.find_element_by_css_selector('h1.title').get_attribute('outerHTML')
        pageHTML = self.browser.find_element_by_css_selector('div#cont_newstxt').get_attribute('innerHTML')
        # pureHTML = remove_comments(pageHTML)
        html = pageTitle + pageHTML

        return html


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
            fileName = '/home/zran/src/crawler/33/manzhua/crawlpy3/record/md5.txt'
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


if __name__ == '__main__':
    d = {}
    file = 'md5.txt'
    try:
        with open(file, mode = 'r') as f:
            line = f.readline()
            if line != '':
                d = eval(str(line))  # 直接把字符串转成字典格式
    except:
        # 如果没有文件，则直接创建文件
        fd = open(file, mode = 'a+', encoding = 'utf-8')
        fd.close()

    a = Agro(d)
    number = a.crawl()
    print(number)
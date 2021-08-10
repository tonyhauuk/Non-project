# -*- coding: utf-8 -*-
# login phone : 18513670871 , username:truwx,  password: Tt123456

import time, datetime, re, hashlib, os, sys
from datetime import datetime, date, timedelta
from time import sleep
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException, WebDriverException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import crawlerfun

from crawlerfun import ClearCache
import time, os, datetime, subprocess
from selenium import webdriver
from selenium.webdriver.opera.options import Options as operaOptions




class Baijiahao:
    def __init__(self, browser):
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        self.date = time.strftime('%Y-%m-%d %H:%M:%S', timeArray)
        self.timeStamp = int(time.time())
        self.d = self.initDict()
        self.url = browser.url
        self.browser = browser.driver
        self.dir = self._dir = self.source = ''
        self.ipnum = crawlerfun.ip2num(browser.ip)
        self.debug = True


    def crawl(self):
        self.i = self.total = 0
        try:
            self.browser.get(self.url)
        except Exception as e:
            print('open error: ', e, '\n')
            self.browser.execute_script('window.stop()')
            self.browser.refresh()
            # self.browser.find_element_by_css_selector('input#su').click()
            print('refresh page', '\n')

        if 'wappass.baidu.com/' in self.browser.current_url:
            sleep(10)

        for i in range(10):
            todo = ''
            newsList = self.browser.find_elements_by_css_selector('div > div.result-op.c-container.xpath-log.new-pmd')

            for item in newsList:
                todo = 'nothing'
                try:
                    dateTime = item.find_element_by_css_selector('span.c-color-gray2.c-font-normal').text
                except:
                    continue

                if '小时前' in dateTime or '分钟前' in dateTime or '秒前' in dateTime:
                    status = self.extract(item)
                    if status < 0:
                        todo = 'restart'
                        break

                    if status == 2:
                        break
                elif '昨天' in dateTime:
                    splitDate = dateTime.split('昨天')
                    yesterday = (date.today() + timedelta(days = -1)).strftime("%Y-%m-%d")
                    ft = yesterday + ' ' + splitDate[1]
                    try:
                        ts = self.calcDate(ft)
                    except:
                        continue
                    oneDay = 60 * 60 * 24

                    if self.timeStamp - ts < oneDay:
                        status = self.extract(item)
                        if status < 0:
                            todo = 'restart'
                            break

                        if status == 2:
                            break
                    else:
                        break
                else:
                    break

            if todo == 'restart':
                print('\nmore than two tabs\n')
                return 'interrupt', 'none', 'error'

            if self.i < len(newsList):
                break
            else:
                try:
                    self.browser.find_element_by_partial_link_text('下一页').click()
                    self.i = 0
                except:
                    break


        print('quantity:', self.total, '\n')
        if self.total > 0:
            self.rename()
            self.expire()

            return 'complete', self.source, 'ok'
        else:
            return 'complete', 'none', 'ok'


    # 提取信息，一条的
    def extract(self, item):

        source = ''
        titleInfo = item.find_element_by_css_selector('h3.news-title_1YtI1 > a')
        href = titleInfo.get_attribute('href')
        title = titleInfo.text
        md5 = self.makeMD5(title)

        # dict filter
        if md5 in self.d:
            return 2
        else:
            handle = self.browser.current_window_handle  # 拿到当前页面的handle
            try:
                titleInfo.click()
            except Exception as e:
                print('extract exception:', e)
                self.browser.refresh()
                print('refresh tab finish! \n')

            # switch tab window
            WebDriverWait(self.browser, 10).until(EC.number_of_windows_to_be(2))
            handles = self.browser.window_handles
            for newHandle in handles:
                if newHandle != handle:
                    self.browser.switch_to.window(newHandle)        # 切换到新标签
                    sleep(2)                                        # 等个几秒钟
                    source = self.getPageText()                     # 拿到网页源码
                    self.browser.close()                            # 关闭当前标签页
                    self.browser.switch_to.window(handle)           # 切换到之前的标签页
                    break

            # if len(self.browser.window_handles) > 1:
            #     return -1

            if source == '':
                return 0
            else:
                self.d[md5] = self.date.split(' ')[0]  # 往dict里插入记录
                self.i += 1
                self.total += 1

                self.write_new_file(href, title, source, self.i, self.date, 1160102)

                return 1



    def getPageText(self):  # 获取网页正文
        if 'wappass.baidu.com/' in self.browser.current_url:
            sleep(10)
            if 'wappass.baidu.com/' in self.browser.current_url:
                return ''

        try:
            html = self.browser.find_element_by_css_selector('div.index-module_articleWrap_2Zphx').get_attribute('innerHTML')
        except:
            html = self.browser.page_source

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
            fileName = '/home/zran/src/crawler/33/manzhua/crawlpy3/record/baijiahao_md5.txt'
            os.remove(fileName)
            with open(fileName, 'a+') as f:
                f.write(str(self.d))
        except Exception as e:
            print(e)


    def initDict(name):
        d = {}
        file = '/home/zran/src/crawler/33/manzhua/crawlpy3/record/baijiahao_md5.txt'
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


    # 日期转换成时间戳
    def calcDate(self, fullTime):
        time1 = fullTime + ':00'
        timeArr = time.strptime(time1, '%Y-%m-%d %H:%M:%S')
        timeStamp = int(time.mktime(timeArr))

        return timeStamp


    # 写一个新文章
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
            print('count:', self.total, ' --- ', title)

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
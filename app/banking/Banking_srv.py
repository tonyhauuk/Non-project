# -*- coding: utf-8 -*-

import time, requests, bs4, datetime, re, hashlib, os, sys, json
from time import sleep
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, NoSuchWindowException, TimeoutException, StaleElementReferenceException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from w3lib import html
from w3lib.html import remove_comments
import crawlerfun



class Banking:
    def __init__(self, browser):
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        self.date = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        self.d = self.initDict()
        self.browser = browser.driver
        self.dir = self._dir = ''
        self.ipnum = crawlerfun.ip2num(browser.ip)
        self.debug = True


    def crawl(self):
        n = 0
        for key, value in self.schedule():  # 获取频道链接
            i = self.doCrawl(key, value)
            if i == -1:
                return 'interrupt', 'none', 'error'
            n += i
            sleep(5)

        if n > 0:
            return 'complete', str(n), 'ok'
        else:
            return 'complete', 'none', 'ok'

    # 开始爬
    def doCrawl(self, colName, url):
        self.rename()
        self.i = self.total = 0
        try:
            self.browser.get(url)
        except:
            return -1

        i = 0

        skipList = ['政策解读', '新闻发言人', '数据图表']
        leftList = self.browser.find_elements_by_css_selector('div.caidan-left > ul.caidan-left-yiji > li.ng-scope')  # 左边频道列表点击, 循环

        if colName == '政府信息公开': # 政务信息栏目下的第一条，政府公开信息单独采集，页面都不一样
            n = self.particular()
            return n

        for j in range(len(leftList)):  # 循环左侧的列表
            if colName == '政务信息' and i == 0:
                i += 1  # 跳过政府信息公开那一栏的信息
                continue

            lst = self.browser.find_elements_by_css_selector('div.caidan-left > ul.caidan-left-yiji > li.ng-scope')  # 获取左边频道的element
            try:
                listName = lst[i].find_element_by_tag_name('a').text

                if listName in skipList:  # 如果当前文字符合list名称，直接跳过不采集
                    i += 1
                    lst[i].find_element_by_tag_name('a').click()
                    continue
            except (NoSuchElementException, StaleElementReferenceException):
                continue
            except IndexError:
                break

            if self.debug:
                print(colName, '-- list name:', listName)

            try:
                moreList = self.browser.find_elements_by_css_selector('div.list > div.tabs > a')
                if len(moreList) == 0:  # 判断是否有更多按钮, 没有直接跳转到正常页面采集
                    raise NoSuchElementException
                else:
                    for k in range(len(moreList)):
                        try:
                            self.browser.find_elements_by_css_selector('div.list > div.tabs > a')[k].click()
                            self.rightCrawl()
                            self.browser.back()
                            self.browser.find_elements_by_css_selector('div.list > div.tabs > a')   # 重新获取element对象
                        except StaleElementReferenceException:
                            print('more list:', self.browser.find_elements_by_css_selector('div.list > div.tabs > a')[k][k].text)

                    # 必须重新获取左边频道的element, 否则会报StaleElementReferenceException异常, 因为页面刷新过, 导致element看似相同, 实际上element id已经发生了变化
                    lst = self.browser.find_elements_by_css_selector('div.caidan-left > ul.caidan-left-yiji > li.ng-scope')
            except NoSuchElementException:
                self.rightCrawl()
            except IndexError:
                continue

            sleep(5)

            if i < len(lst):
                sleep(2)
                i += 1
                try:
                    self.browser.find_elements_by_css_selector('div.caidan-left > ul.caidan-left-yiji > li.ng-scope')[i].find_element_by_tag_name('a').click()
                except StaleElementReferenceException:
                    continue
                except IndexError:
                    break

        if self.total > 0:
            self.rename()
            self.expire()

            return self.total
        else:
            return 0



    # 抓取右侧的列表信息
    def rightCrawl(self):
        self.browser.find_element_by_xpath('/html/body').send_keys(Keys.END)
        sleep(1)
        self.browser.find_element_by_xpath('/html/body').send_keys(Keys.HOME)
        while True:  # 翻页的循环
            rightList = self.browser.find_elements_by_css_selector('div.row > div.ng-scope > div.list.caidan-right-list')  # 获取右边标题list的信息
            if len(rightList) > 0:
                length = self.normalCrawl(rightList)
                if self.i == 0 or self.i < length:
                    break
            else:
                try:
                    rightList = self.browser.find_element_by_css_selector('div.list.caidan-ritht-xinwenfabu')
                    length = self.otherCrawl(rightList)
                except NoSuchElementException:
                    length = self.particularCrawl() # 非正常页面采集

                if self.i == 0 or self.i < length:
                    break

            self.i = 0  # 当前页计数器清零

            try:
                self.browser.find_element_by_css_selector('a[ng-click="pager.next()"]').click()  # 点击下一页
                sleep(2)
            except NoSuchElementException:
                break


    # 正常采集, 网页形式大部分相同的
    def normalCrawl(self, items):
        length = 0
        for item in items:
            try:
                # 找到不包含class是ng-hide的div标签，他们的网站会隐藏某些div, 导致爬取的信息比看到的要多
                divs = item.find_elements_by_css_selector('div.panel-row.ng-scope:not(.ng-hide)')
                length += len(divs)
                for div in divs:
                    dateTime = div.find_element_by_css_selector('span.date.ng-binding').text
                    if dateTime in self.date:
                        self.extract(div)

            except StaleElementReferenceException :
                print('Normal StaleElementException')

        return length


    # 非正常页面采集, 跟大部分网页不同
    def otherCrawl(self, item):
        divs = item.find_elements_by_css_selector('div.panels.ng-scope')  # 获取条数
        for div in divs:
            try:
                dateTime = div.find_element_by_css_selector('span.date.ng-binding').text
                if dateTime in self.date:
                    self.extract(div)
            except StaleElementReferenceException:
                dateTime = div.find_element_by_css_selector('span.date.ng-binding').text
                if dateTime in self.date:
                    self.extract(div)

            sleep(2)

        return len(divs)


    # 特殊页面采集
    def particular(self):
        if self.debug:
            print('=== 政府信息公开 === 页面采集')

        self.browser.find_element_by_xpath('/html/body').send_keys(Keys.END)
        sleep(1)
        self.browser.find_element_by_xpath('/html/body').send_keys(Keys.HOME)

        moreList = self.browser.find_elements_by_css_selector('div.list.ng-scope > div.zhengfuxinxi-list.mb25.ng-scope > div.zhengfuxinxi-list-tabmore a')
        for i in range(len(moreList)):  # 点击更多, 如果没有略过
            try:
                self.browser.find_elements_by_css_selector('div.list.ng-scope > div.zhengfuxinxi-list.mb25.ng-scope > div.zhengfuxinxi-list-tabmore a')[i].click()
                sleep(1)
                self.rightCrawl()
                self.browser.back()
                sleep(1)
                self.browser.find_elements_by_css_selector('div.list.ng-scope > div.zhengfuxinxi-list.mb25.ng-scope > div.zhengfuxinxi-list-tabmore a')  # 重新获取element对象
                sleep(2)
            except IndexError:
                break
            except StaleElementReferenceException:
                print('Particular StaleElementException')

        if self.total > 0:
            self.rename()
            self.expire()
            return self.total
        else:
            return 0


    def particularCrawl(self):
        li = self.browser.find_elements_by_css_selector('div > ul.ng-scope > li.ng-scope')
        for info in li:
            dateTime = info.find_element_by_css_selector('span.zhengfuxinxi-list-date.ng-binding').text
            if dateTime in self.date:
                self.extract(info)

        return len(li)


    # 提取信息，一条的
    def extract(self, item):
        try:
            titleInfo = item.find_element_by_css_selector('span > a.ng-binding')  # normal & particular
        except NoSuchElementException:
            titleInfo = item.find_element_by_css_selector('div.title > a.ng-binding')  # other

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
                    sleep(1)                                    # 等个几秒钟
                    self.source = self.getPageText()            # 拿到网页源码
                    self.browser.close()                        # 关闭当前标签页
                    self.browser.switch_to.window(handle)       # 切换到之前的标签页
                    break

            self.write_new_file(href, title, self.source, self.i, self.date)
        except (NoSuchElementException, NoSuchAttributeException) as e:
            print('Element error:', e)
        except Exception:
            pass


    def getPageText(self):  # 获取网页正文
        pageTitle = self.browser.find_element_by_css_selector('div.container div.row > div[ng-show="showTitle"]').get_attribute('outerHTML')
        pageHTML = self.browser.find_element_by_css_selector('div.container div.row > div#wenzhang-content').get_attribute('innerHTML')
        pureHTML = remove_comments(pageHTML)
        html = pageTitle + pureHTML

        return html


    # 读取链接
    def schedule(self):
        filName = './banking/column_list.json'
        f = open(filName, encoding = 'utf-8')
        obj = json.load(f)
        items = obj.items()

        return items


    # 生成md5信息
    def makeMD5(self, title):
        m = hashlib.md5()
        b = title.encode(encoding = 'utf-8')
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


    # 写一个新文章
    def write_new_file(self, url, title, source, i, time):
        ok = 0
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
                            <span class="source">1170841</span>
                            <div class="article">''' + source + '''</div>
                        </body>
                    </html>
                '''
        page_text = url + '\n' + title + '\n1170841\n\n\n\n' + content
        if self.debug:
            print('count:', self.total, ' === ', title, ' ===')

        if '' == self._dir:
            self.banking_mkdir()

        filename = self._dir + 'iask_' + str(i) + '_' + str(len(self.d)) + '.htm-2'
        for num in range(2):
            if 1 == crawlerfun.write_file(filename, page_text, ifdisplay = 0):
                fileName = '/root/Downloads/' + 'iask_' + str(i) + '_' + str(len(self.d)) + '.htm-2'
                crawlerfun.write_file(fileName, page_text, ifdisplay = 0)  # 再次保存到/root/Downloads目录下
                ok = 1
                break
            else:  # 有时目录会被c程序删掉
                crawlerfun.mkdir(self._dir)

        return ok


    # 制作电网目录，注意不创建目录，只是生成目录信息
    def banking_mkdir(self):
        dirroot = '/estar/newhuike2/1/'
        tm_s, tm_millisecond = crawlerfun.get_timestamp(ifmillisecond = 1)
        dirsmall = 'iask' + str(self.ipnum) + '.' + str(1) + '.' + str(tm_s) + '.' + str(tm_millisecond) + '/'
        self._dir = dirroot + '_' + dirsmall
        self.dir = dirroot + dirsmall

        return self._dir, self.dir


    def initDict(self):
        d = {}
        file = '/home/zran/src/crawler/33/manzhua/crawlpy3/record/md5.txt'
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
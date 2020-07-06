# -*- coding: utf-8 -*-

import time, hashlib, os, urllib.parse
from time import sleep
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException, StaleElementReferenceException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Banking:
    def __init__(self, d):
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        self.date = time.strftime('%Y-%m-%d %H:%M:%S', timeArray)
        self.d = d
        self.dir = self._dir = self.source = ''
        self.debug = True

    def crawl(self):
        print('\n' ,'-' * 10, 'www.cbirc.gov.cn', '-' * 10)

        self.browser = webdriver.Firefox()
        self.browser.set_window_position(x = 690, y = 0)
        self.total = 0
        i = 0
        status = True
        file = './bank_weblist.txt'
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
                # self.deleteFiles()
                return 'complete', self.source, 'ok'
            else:
                return 'complete', 'none', 'ok'
        else:
            return 'interrupt', 'none', 'error'


    def doCrawl(self, url):
        self.i = 0
        try:
            self.browser.get(url)
        except TimeoutException:
            return -1

        if 'zhengwuxinxi' in url:  # 政务信息栏目下的第一条，政府公开信息单独采集，页面都不一样
            n = self.particular()
            return n

        while True:  # 翻页的循环
            rightList = self.browser.find_elements_by_css_selector('div.ng-scope > div.list.caidan-right-list')  # 获取右边标题list的信息
            if len(rightList) > 0:
                length = self.normalCrawl(rightList)
                if self.i == 0 or self.i < length:
                    break
            else:
                try:
                    rightList = self.browser.find_element_by_css_selector('div.list.caidan-ritht-xinwenfabu')
                    length = self.otherCrawl(rightList)
                except NoSuchElementException:
                    length = self.particularCrawl()  # 非正常页面采集

                if self.i == 0 or self.i < length:
                    break

            self.i = 0  # 当前页计数器清零

            try:
                self.browser.find_element_by_css_selector('a[ng-click="pager.next()"]').click()  # 点击下一页
                sleep(2)
            except NoSuchElementException:
                break


        if self.total > 0:
            self.rename()
            self.expire()

            return self.total
        else:
            return 0


    # 正常采集, 网页形式大部分相同的
    def normalCrawl(self, items):
        length = 0
        for item in items:
            # 找到不包含class是ng-hide的div标签，它们网站会隐藏某些div, 导致爬取的信息比看到的要多
            blocks = item.find_elements_by_css_selector('div.panel-row.ng-scope:not(.ng-hide)')
            length += len(blocks)
            for block in blocks:
                dateTime = block.find_element_by_css_selector('span.date.ng-binding').text
                if dateTime == self.date.split(' ')[0]:
                    self.extract(block)

        return length


    # 提取信息，一条的
    def extract(self, item):
        try:
            titleInfo = item.find_element_by_css_selector('span > a.ng-binding')        # normal & particular
        except NoSuchElementException:
            titleInfo = item.find_element_by_css_selector('div.title > a.ng-binding')   # other

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

            # self.write_new_file(href, title, self.source, self.i, self.date, 1170841)
        except Exception:
            self.i -= 1
            self.total -= 1


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


    def getPageText(self):  # 获取网页正文
        try:
            html = self.browser.find_element_by_css_selector('div#page_0').get_attribute('innerHTML')
        except NoSuchElementException:
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
            fileName = '/home/zran/src/crawler/33/manzhua/crawlpy3/record/hbia_md5.txt'
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


    def deleteFiles(self):
        filePath = '/root/estar_save/hbia_gov/'
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        current = time.strftime("%Y-%m-%d", timeArray)
        name = os.listdir(filePath)

        for i in name:
            try:
                fileName = filePath + i
                fileInfo = os.stat(fileName)
            except FileNotFoundError:
                continue
            ts = fileInfo.st_mtime
            timeArr = time.localtime(ts)
            date = time.strftime("%Y-%m-%d", timeArr)
            if current != date:
                os.remove(fileName)


    def initDict(self):
        d = {}
        file = '/home/zran/src/crawler/33/manzhua/crawlpy3/record/hbia_md5.txt'
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

    def getItemName(self, url):
        data = urllib.parse.unquote(url.split('itemName=')[1])

        return data


if __name__ == '__main__':
    bank = Banking({})
    bank.crawl()

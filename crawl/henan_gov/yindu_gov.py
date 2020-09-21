# -*- coding: utf-8 -*-

import time, hashlib, os, datetime
from time import sleep
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Yindu_gov:
    def __init__(self, d):
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        self.date = time.strftime('%Y-%m-%d %H:%M:%S', timeArray)
        self.d = d
        self.dir = self._dir = ''
        self.debug = True


    def crawl(self):
        print('\n' ,'-' * 10, 'http://www.yindu.gov.cn/', '-' * 10, '\n')

        self.browser = webdriver.Firefox()
        self.browser.set_window_position(x = 630, y = 0)

        self.total = 0
        i = 0
        status = True
        file = './yindu_gov_weblist.txt'
        with open(file, mode = 'r') as f:
            url = f.readlines()
            for x in url:
                n = self.doCrawl(x)
                if n == -1:
                    status = False
                    break
                else:
                    i += n

        self.browser.quit()
        if status:
            if i > 0:
                self.deleteFiles()
                return 'complete', self.source, 'ok'
            else:
                return 'complete', 'none', 'ok'
        else:
            return 'interrupt', 'none', 'error'


    def doCrawl(self, url):
        self.i = 0
        self.url = url
        try:
            self.browser.get(url)
        except TimeoutException:
            return -1


        if '1226' in url:
            blocks = self.browser.find_elements_by_css_selector('div.maplist > table')
            for i in range(len(blocks)):
                newsList = self.browser.find_elements_by_css_selector('div.RightSub > ul > li')
                for j in range(len(newsList)):
                    item = self.browser.find_elements_by_css_selector('div.RightSub > ul > li')[i]
                    dateTime = item.find_element_by_tag_name('span').text

                    if self.getTime(dateTime) in self.date:
                        self.extract(item)
                    else:
                        break

        else:
            if '/7' in url :
                newsCss = 'div.RightSub > ul > li'
            else:
                newsCss = 'div.ArticleWrap > ul > li'

            while True:
                newsList = self.browser.find_elements_by_css_selector(newsCss)
                for i in range(len(newsList)):
                    item = self.browser.find_elements_by_css_selector(newsCss)[i]
                    dateTime = item.find_element_by_tag_name('span').text

                    if self.getTime(dateTime) in self.date:
                        self.extract(item)
                    else:
                        break

                if self.i < len(newsList):
                    break
                else:
                    try:
                        self.browser.find_element_by_partial_link_text('下页').click()
                        self.i = 0
                    except NoSuchElementException:
                        break


        if self.total > 0:
            # self.rename()
            # self.expire()

            return self.total
        else:
            return 0


    # 提取信息，一条的
    def extract(self, item):
        titleInfo = item.find_element_by_css_selector('a')

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
            titleInfo.click()

            self.source = self.getPageText()  # 拿到网页源码
            sleep(1)
            self.browser.back()


            print(href, title)

            # self.write_new_file(href, title, self.source, self.i, self.date, 1166539)
        except Exception as e:
            return False


    def getPageText(self):  # 获取网页正文
        try:
            html = self.browser.find_element_by_css_selector('li#zomfont').get_attribute('innerHTML')
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
            fileName = '/home/zran/src/crawler/31/manzhua/crawlpy3/record/sc_md5.txt'
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
        filePath = '/root/estar_save/sc_gov/'
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

    def getTime(self,dateTime):
        t = dateTime.replace('[', '')
        t = t.replace(']', '')

        if '年' in dateTime or '月' in dateTime or '日' in dateTime:
            t = t.replace('年', '-')
            t = t.replace('月', '-')
            t = t.replace('日', '')

        if '发布时间：' in dateTime:
            t = t.replace('发布时间：', '')

        return t

if __name__ == '__main__':
    y = Yindu_gov({})
    y.crawl()

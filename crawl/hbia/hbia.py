# -*- coding: utf-8 -*-

import time, hashlib, os
from time import sleep
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Hbia:
    def __init__(self, d):
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        self.date = time.strftime('%Y-%m-%d %H:%M:%S', timeArray)
        self.d = d
        self.dir = self._dir = ''
        self.debug = True

    def crawl(self):
        print('\n' ,'-' * 10, 'http://www.hbia.cn/', '-' * 10)

        self.browser = webdriver.Firefox()
        self.browser.set_window_position(x = 650, y = 0)

        i = 0
        status = True
        file = './hbia_weblist.txt'
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
                self.deleteFiles()
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

        tbody = self.browser.find_element_by_xpath('/html/body/table[3]/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr/td/table/tbody')
        newsList = tbody.find_elements_by_tag_name('tr')

        for i in range(len(newsList)):
            tbody = self.browser.find_element_by_xpath('/html/body/table[3]/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr/td/table/tbody')
            newsList = tbody.find_elements_by_tag_name('tr')
            if i == 0:
                continue

            try:
                dateTime = newsList[i].find_elements_by_tag_name('td')[2].text
                if dateTime in self.date:
                    item = newsList[i].find_elements_by_tag_name('td')[1]
                    self.extract(item)
                else:
                    break
            except IndexError:
                break

        if self.i > 0:
            self.rename()
            self.expire()

            return self.i
        else:
            return 0


    # 提取信息，一条的
    def extract(self, item):
        titleInfo = item.find_element_by_tag_name('a')

        try:
            href = titleInfo.get_attribute('href')
            md5 = self.makeMD5(href)

            if md5 in self.d:
                return
            else:
                self.d[md5] = self.date.strip(' ')[0]  # 往dict里插入记录
                self.i += 1

            title = titleInfo.text
            titleInfo.click()
            self.source = self.getPageText()            # 拿到网页源码
            self.browser.back()

            # self.write_new_file(href, title, self.source, self.i, self.date)
        except (NoSuchElementException, NoSuchAttributeException) as e:
            print('Element error:', e)
            self.i -= 1
        except Exception:
            self.i -= 1
            return


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


if __name__ == '__main__':
    hbia = Hbia({})
    hbia.crawl()

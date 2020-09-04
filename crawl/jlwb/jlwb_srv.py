# -*- coding: utf-8 -*-

import time, hashlib, os
from time import sleep
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import crawlerfun

class Jlwb:
    def __init__(self, browser, ip):
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        self.date = time.strftime('%Y-%m-%d %H:%M:%S', timeArray)
        self.d = self.initDict()
        self.browser = browser
        self.dir = self._dir = ''
        self.ipnum = crawlerfun.ip2num(ip)
        self.debug = True


    def crawl(self):
        print('\n', '-'*10, 'http://jlwb.njnews.cn', '-'*10, self.date)
        self.i = 0
        try:
            self.browser.get('http://jlwb.njnews.cn')
        except:
            return 'interrupt', 'none', 'error'

        sleep(5)
        try:
            # self.browser.find_element_by_xpath('/html/body/table/tbody/tr[1]/td/div/div[3]/a[2]').click()
            self.browser.find_elements_by_css_selector('div.head > div.menu > a')[1].click()
            self.browser.find_element_by_xpath('/html/body').send_keys(Keys.END)
        except:
            return 'complete', 'none', 'ok'

        newsList = self.browser.find_elements_by_css_selector('div.list > a')
        for i in range(len(newsList)):
            info = self.browser.find_elements_by_css_selector('div.list > a')[i]
            href = info.get_attribute('href')
            md5 = self.makeMD5(href)

            if md5 in self.d:
                break
            else:
                self.d[md5] = self.date.split(' ')[0]  # 往dict里插入记录
                self.i += 1
                self.extract(info)


        if self.i > 0:
            self.rename()
            self.expire()
            self.deleteFiles()

            return 'complete', self.source, 'ok'
        else:
            return 'complete', 'none', 'ok'


    # 提取信息，一条的
    def extract(self, info):
        try:
            title = info.text
            info.click()
            try:
                img = self.browser.find_element_by_css_selector('div.coin-slider').get_attribute('innerHTML')
            except:
                img = self.browser.find_element_by_css_selector('div#coin-slider').get_attribute('innerHTML')

            img = img.replace('src="..\..\..\..\jlwb', 'http://jlwb.njnews.cn/jlwb')

            cnt = self.browser.find_element_by_css_selector('div.content').text
            self.source = img + cnt
            href = self.browser.current_url

            self.write_new_file(href, title, self.source, self.i, self.date, 414705)
            self.browser.back()
        except Exception:
            return





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
            fileName = '/home/zran/src/crawler/33/manzhua/crawlpy3/record/jlwb_md5.txt'
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


    def initDict(self):
        d = {}
        file = '/home/zran/src/crawler/33/manzhua/crawlpy3/record/jlwb_md5.txt'
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


    # 写一个新文章
    def write_new_file(self, url, title, source, i, time, id):
        if self.debug:
            print('count:', self.i, ' --- ', title)

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
            self.jlwb_mkdir()

        filename = self._dir + 'iask_' + str(i) + '_' + str(len(self.d)) + '.htm-2'
        for num in range(2):
            if 1 == crawlerfun.write_file(filename, page_text, ifdisplay = 0):
                savePath = '/root/estar_save/jlwb/'
                if not os.path.exists(savePath):
                    os.makedirs(savePath)
                fileName = savePath + 'iask_' + str(i) + '_' + str(len(self.d)) + '.htm-2'
                crawlerfun.write_file(fileName, page_text, ifdisplay = 0)  # 再次保存到/root/estar_save目录下

                break
            else:  # 有时目录会被c程序删掉
                crawlerfun.mkdir(self._dir)


    # 制作电网目录，注意不创建目录，只是生成目录信息
    def jlwb_mkdir(self):
        dirroot = '/estar/newhuike2/1/'
        tm_s, tm_millisecond = crawlerfun.get_timestamp(ifmillisecond = 1)
        dirsmall = 'iask' + str(self.ipnum) + '.' + str(1) + '.' + str(tm_s) + '.' + str(tm_millisecond) + '/'
        self._dir = dirroot + '_' + dirsmall
        self.dir = dirroot + dirsmall

        return self._dir, self.dir


    def deleteFiles(self):
        filePath = '/root/estar_save/jlwb/'
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

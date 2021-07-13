# -*- coding: utf-8 -*-

import time, hashlib, os
from time import sleep
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Yz:
    def __init__(self, d):
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        self.date = time.strftime('%Y-%m-%d %H:%M:%S', timeArray)
        self.d = d
        self.dir = self._dir = ''
        self.debug = True


    def crawl(self):
        self.browser = webdriver.Firefox()
        self.browser.set_window_position(x = 630, y = 0)
        self.i = 0

        try:
            self.browser.get('http://epaper.yzwb.net/pc/layout/')
        except TimeoutException:
            return 'interrupt', 'none', 'error'

        sleep(3)

        self.browser.find_element_by_css_selector('div.newsside > ul > li.oneclick1 > a')
        sleep(2)
        getLoop = self.browser.find_elements_by_css_selector('div.Chunkiconlist > p')

        for i in range(len(getLoop)):
            newsList = self.browser.find_elements_by_css_selector('div.newslist > ul > li')
            for j in range(len(newsList)):
                item = self.browser.find_elements_by_css_selector('div.newslist > ul > li')[j]
                titleInfo = item.find_element_by_tag_name('a')
                href = titleInfo.get_attribute('href')

                md5 = self.makeMD5(href)
                # dict filter
                if md5 in self.d:
                    return
                else:
                    self.d[md5] = self.date.split(' ')[0]  # 往dict里插入记录
                    self.i += 1
                    self.extract(titleInfo, href)

            try:
                self.browser.find_element_by_partial_link_text('下一版').click()
                self.i = 0
            except:
                break


        if self.i > 0:
            pass
            # self.rename()
            # self.expire()

            return 'complete', self.source, 'ok'
        else:
            return 'complete', 'none', 'ok'


    # 提取信息，一条的
    def extract(self, info, href):
        try:
            title = info.text
            self.browser.set_page_load_timeout(2)
            self.browser.set_script_timeout(2)
            try:
                self.browser.get(href)
            except:
                self.browser.execute_script('window.stop()')

            if self.debug:
                print('count:', self.i, ' --- ', title)


            self.source = self.browser.find_element_by_css_selector('div.newsdetatext').text

            # self.write_new_file(href, title, self.source, self.i, self.date, 416045)
            self.browser.back()
            sleep(2)
        except Exception as e:
            print(e)
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
            fileName = '/home/zran/src/crawler/33/manzhua/crawlpy3/record/hbxw_md5.txt'
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
        file = '/home/zran/src/crawler/33/manzhua/crawlpy3/record/hbxw_md5.txt'
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
    x = Yz({})
    x.crawl()
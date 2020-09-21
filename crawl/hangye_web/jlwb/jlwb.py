# -*- coding: utf-8 -*-

import time, hashlib, os
from time import sleep
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Jlwb:
    def __init__(self, d):
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        self.date = time.strftime('%Y-%m-%d %H:%M:%S', timeArray)
        self.d = d
        self.dir = self._dir = ''
        self.debug = True


    def crawl(self):
        self.browser = webdriver.Firefox()
        self.browser.set_window_position(x = 600, y = 0)
        self.i = 0

        try:
            self.browser.get('http://jlwb.njnews.cn')
        except TimeoutException:
            return 'interrupt', 'none', 'error'

        sleep(5)
        self.browser.find_elements_by_css_selector('div.head > div.menu > a')[1].click()

        newsList = self.browser.find_elements_by_css_selector('div.list > a')
        for i in range(len(newsList)):
            info = self.browser.find_elements_by_css_selector('div.list > a')[i]
            href = info.get_attribute('href')

            md5 = self.makeMD5(href)
            # dict filter
            if md5 in self.d:
                return
            else:
                self.d[md5] = self.date.split(' ')[0]  # 往dict里插入记录
                self.i += 1
                self.extract(info)


        if self.i > 0:
            self.rename()
            self.expire()

            return 'complete', self.source, 'ok'
        else:
            return 'complete', 'none', 'ok'


    # 提取信息，一条的
    def extract(self, info):
        try:
            title = info.text
            self.browser.set_page_load_timeout(2)
            self.browser.set_script_timeout(2)
            try:
                info.click()
            except:
                self.browser.execute_script('window.stop()')

            if self.debug:
                print('count:', self.i, ' --- ', title)

            try:
                img = self.browser.find_element_by_css_selector('div.coin-slider').get_attribute('innerHTML')
            except:
                img = self.browser.find_element_by_css_selector('div#coin-slider').get_attribute('innerHTML')

            cnt = self.browser.find_element_by_css_selector('div.content').text
            self.source = img + cnt
            href = self.browser.current_url

            # self.write_new_file(href, title, self.source, self.i, self.date, 414705)
            self.browser.back()
            sleep(2)
        except (NoSuchElementException, NoSuchAttributeException) as e:
            print('Element error:', e)

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
    j = Jlwb({})
    j.crawl()
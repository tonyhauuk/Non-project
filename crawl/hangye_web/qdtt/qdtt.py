# -*- coding: utf-8 -*-

import time, hashlib, os, re
from time import sleep
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Qdtt:
    def __init__(self, d):
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        self.date = time.strftime('%Y-%m-%d', timeArray)
        self.d = d
        self.dir = self._dir = ''
        self.debug = True


    def crawl(self):
        self.browser = webdriver.Firefox()
        self.browser.set_window_position(x = 600, y = 0)
        self.total = 0

        try:
            self.browser.get('http://www.qddtz.com/')
        except TimeoutException:
            return 'interrupt', 'none', 'error'

        # newsList = self.browser.find_elements_by_css_selector('div.new_lanmu_l > div')
        # for items in newsList:
        #     ul = items.find_elements_by_css_selector('div.new_lanmu_cl > div.new_lanmu_list > ul')
        #     for lis in ul:
        #         li = lis.find_elements_by_tag_name('li')
        #         for item in li:
        #             self.extract(item)
        #             sleep(2)

        newsList = self.browser.find_elements_by_css_selector('div.new_lanmu_l > div')
        for i in range(len(newsList)):
            ul = self.browser.find_elements_by_css_selector('div.new_lanmu_l > div')[i].find_elements_by_css_selector('div.new_lanmu_cl > div.new_lanmu_list > ul')
            for j in range(len(ul)):
                li = self.browser.find_elements_by_css_selector('div.new_lanmu_l > div')[i].find_elements_by_css_selector('div.new_lanmu_cl > div.new_lanmu_list > ul')[j].find_elements_by_tag_name('li')
                for k in range(len(li)):
                    item = self.browser.find_elements_by_css_selector('div.new_lanmu_l > div')[i].find_elements_by_css_selector('div.new_lanmu_cl > div.new_lanmu_list > ul')[j].find_elements_by_tag_name('li')[k]
                    self.extract(item)
                    sleep(2)


    def extract(self, item):
        item.find_element_by_tag_name('a').click()
        sleep(2)
        content = self.browser.find_element_by_css_selector('div.arc')
        timeStr = content.find_element_by_css_selector('div.resource').text
        dateTime = self.filterChn(timeStr)

        if self.date in dateTime:  # 如果时间匹配
            href = self.browser.current_url
            md5 = self.makeMD5(href)
            # dict filter
            if md5 in self.d:
                return
            else:
                self.d[md5] = dateTime  # 往dict里插入记录
                self.total += 1
                title = content.find_element_by_css_selector('div.title').text
                source = content.find_element_by_css_selector('div.content').text
                print(dateTime, title)
                # self.write_new_file(href, title, source, self.i, 1169930)
                self.browser.back()
        else:
            return


    def filterChn(self, timeStr):
        fakeTime = timeStr.split('：')[1]
        pattern = re.compile(r'[^\u4e00-\u9fa5]')
        chinese = re.sub(pattern, '', fakeTime)
        dateTime = fakeTime.replace(chinese, '')

        return dateTime


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
            fileName = '/home/zran/src/crawler/33/manzhua/crawlpy3/record/qqdt_md5.txt'
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
        file = '/home/zran/src/crawler/33/manzhua/crawlpy3/record/qqdt_md5.txt'
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
    q = Qdtt({})
    q.crawl()

# -*- coding: utf-8 -*-

import time, hashlib, os
from time import sleep
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Zibo:
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
        self.total = 0
        i = 0
        status = True
        file = 'zibo_gov_weblist.txt'
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
        self.url = url
        try:
            self.browser.get(url)
        except TimeoutException:
            return -1

        # self.browser.find_element_by_xpath('/html/body').send_keys(Keys.END)
        # sleep(1)
        # self.browser.find_element_by_xpath('/html/body').send_keys(Keys.HOME)

        while True:
            newsList = self.browser.find_elements_by_css_selector('div.default_pgContainer > ul > li')
            for item in newsList:
                dateTime = item.find_element_by_tag_name('span').text
                if dateTime in self.date:
                    self.extract(item)
                else:
                    break

            if self.i < len(newsList):  # 如果当前抓取的数量小于页面展示的数量并且在第一页，就不翻页了
                break
            else:
                try:
                    self.browser.find_element_by_css_selector('table.default_pgPanel > tbody > tr > td > a.default_pgNext').click()  # 点击下一页
                    self.i = 0  # 当前页的计数器清零
                    sleep(2)
                except:
                    break
        return 1
        # if self.total > 0:
        #     self.rename()
        #     self.expire()
        #
        #     return self.total
        # else:
        #     return 0


    # 提取信息，一条的
    def extract(self, item):
        try:
            titleInfo = item.find_element_by_tag_name('a')
            href = titleInfo.get_attribute('href')
            md5 = self.makeMD5(href)

            # dict filter
            if md5 in self.d:
                return
            else:
                self.d[md5] = self.date.split(' ')[0]  # 往dict里插入记录
                self.i += 1
                self.total += 1

            if '429' in self.url:
                title = titleInfo.text
            else:
                title = titleInfo.get_attribute('title')

            handle = self.browser.current_window_handle  # 拿到当前页面的handle
            titleInfo.click()

            # switch tab window
            WebDriverWait(self.browser, 10).util(EC.number_of_windows_to_be(2))
            handles = self.browser.window_handles
            for newHandle in handles:
                if newHandle != handle:
                    self.browser.switch_to.window(newHandle)    # 切换到新标签
                    sleep(1)                                    # 等个几秒钟
                    self.source = self.getPageText()            # 拿到网页源码
                    self.browser.close()                        # 关闭当前标签页
                    self.browser.switch_to.window(handle)       # 切换到之前的标签页
                    break

            if self.debug:
                print('count:', self.i, ' === ', title, ' ===')

            # self.write_new_file(href, title, self.source, self.i, 1168570)
        except (NoSuchElementException, NoSuchAttributeException) as e:
            print('Element error:', e)
        except Exception:
            return


    def getPageText(self):  # 获取网页正文
        try:
            if '429' in self.url:
                html = self.browser.find_element_by_css_selector('div.content_wzy > div').get_attribute('innerHTML')
            else:
                html = self.browser.find_element_by_css_selector('td.bt_content').get_attribute('innerHTML')
        except NoSuchElementException:
            html = self.browser.page_source

        return html


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
    z = Zibo({})
    z.crawl()
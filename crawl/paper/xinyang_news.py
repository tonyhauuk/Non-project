# -*- coding: utf-8 -*-

import time, datetime, re, hashlib, os, sys
from time import sleep
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#import crawlerfun

class Xinyang_news:
    def __init__(self, d):
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        self.date = time.strftime('%Y-%m-%d %H:%M:%S', timeArray)
        self.projectName = 'food'
        self.d = d
        self.dir = self._dir = self.source = ''
        # self.ipnum = crawlerfun.ip2num('61.130.181.229')
        self.debug = True


    def crawl(self):
        print('\n', '-' * 10, 'https://www.xyxww.com.cn/', '-' * 10, '\n')
        self.i = self.total = 0
        self.browser = webdriver.Firefox()
        self.browser.set_window_position(x = 630, y = 0)
        n = 0

        keywords = ['hn', 'gn', 'gj', 'xinyang', 'xianqu', 'shtt', 'zht', 'shehui', 'pl', 'lskd', 'yxgs', 'fczx', 'csdt', 'hdbd', 'xckb',
                    'cxdq', 'cj', 'jkzx', 'bgt', 'lx', 'xl', 'bj', 'mr', 'myt', 'yy', 'yctj', 'hwcy', 'mslm', 'msrd', 'msys', 'mfsc', 'xymshi',
                    'jyzx', 'ztjyj', 'cglx', 'xjzz', 'gongan', 'xyfzh', 'fayuan', 'xfzz', 'shwx', 'xf', 'xwzx', 'jjzx', 'dj']

        for keyword in keywords:
            try:
                url = 'https://www.xyxww.com.cn/jhtml/' + keyword
                self.browser.get(url)
            except TimeoutException:
                n = -1
                break

            page = 1
            while True:
                newsList = self.browser.find_elements_by_css_selector('div#content > ul.newslist > li')
                for item in newsList:
                    dateTime = item.find_element_by_tag_name('span').text
                    dateTime = dateTime.replace('[', '').split(' ')[0]
                    if dateTime in self.date:
                        self.extract(item)
                    else:
                        break

                if self.i < len(newsList):
                    break
                else:
                    page += 1
                    try:
                        self.browser.find_elements_by_css_selector('ul.newslist > div > a')[page].click()
                        self.i = 0
                    except NoSuchElementException:
                        break


        print('quantity:', self.total)
        if n == 0:
            if self.total > 0:
                # self.rename()
                # self.expire()
                # self.deleteFiles()

                return 'complete', self.source, 'ok'
            else:
                return 'complete', 'none', 'ok'
        else:
            return 'interrupt', 'none', 'error'


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

            title = titleInfo.text

            handle = self.browser.current_window_handle  # 拿到当前页面的handle
            titleInfo.click()

            # switch tab window
            WebDriverWait(self.browser, 10).until(EC.number_of_windows_to_be(2))
            handles = self.browser.window_handles
            for newHandle in handles:
                if newHandle != handle:
                    self.browser.switch_to.window(newHandle)        # 切换到新标签
                    sleep(1)                                        # 等个几秒钟
                    self.source = self.getPageText()                # 拿到网页源码
                    self.browser.close()                            # 关闭当前标签页
                    self.browser.switch_to.window(handle)           # 切换到之前的标签页
                    break

            if self.source != '':
                print(href, title)
                # self.write_new_file(href, title, self.source, self.i, self.date, 498605)
            else:
                return
        except (NoSuchElementException, NoSuchAttributeException) as e:
            print('Element error:', e)
        except Exception:
            return


    def getPageText(self):  # 获取网页正文
        try:
            pubTime = self.browser.find_element_by_css_selector('div.subtext > span#pubtime_baidu').text
        except:
            html = ''
        else:
            dateTime = pubTime.split(' ')[0]
            if dateTime in self.date:
                try:
                    html = self.browser.find_element_by_css_selector('div#artibody').get_attribute('innerHTML')
                except NoSuchElementException:
                    html = self.browser.page_source
            else:
                html = ''

        return  html


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
            fileName = '/home/zran/src/crawler/33/manzhua/crawlpy3/record/cnstock_md5.txt'
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
        filePath = '/root/estar_save/cnstock/'
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


if __name__ == '__main__':
    z = Xinyang_news({})
    z.crawl()
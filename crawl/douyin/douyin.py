# -*- coding: utf-8 -*-

import time, datetime, re, hashlib, os, sys
from datetime import datetime, date, timedelta
from time import sleep
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
#import crawlerfun
import warnings
warnings.filterwarnings('ignore')

class Douyin:
    def __init__(self, d):
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        self.date = time.strftime('%Y-%m-%d %H:%M:%S', timeArray)
        self.timeStamp = int(time.time())
        self.projectName = 'douyin'
        self.d = d
        self.dir = self._dir = self.source = ''
        # self.ipnum = crawlerfun.ip2num('61.130.181.229')
        self.debug = True


    def crawl(self):
        self.browser = webdriver.Firefox()
        self.browser.set_window_position(x = 630, y = 0)

        keywords = ['一流科技', '资金缺口', '３６１度', '研究成果', '高科技', '优山美地', '绿色生产', '发展方向', '春蕾计划', '无责免陪', '美地雅登']
        for keyword in keywords:
            self.doJob(keyword)

    def doJob(self, keyword):
        print('\n', '-' * 10, 'https://www.douyin.com/', '-' * 10, '\n')
        self.i = self.total = 0

        n = 0
        url = 'https://www.douyin.com/search/' + keyword + '?publish_time=1&sort_type=0&source=tab_search&type=general'
        try:
            self.browser.get(url)
            sleep(5)
        except TimeoutException:
            n = -1

        try:
            self.browser.find_element(by = By.ID, value = 'login-pannel')
            sleep(2)
            print('[login page]')
            self.browser.find_element(by = By.CSS_SELECTOR, value = 'div.dy-account-close').click()
        except NoSuchElementException:
            pass

        try:
            self.browser.find_element(by = By.CSS_SELECTOR, value = 'div.captcha_verify_container.style__CaptchaWrapper-sc-1gpeoge-0.zGYIR')
            print('[slide page]')
            sleep(600)
            # self.browser.refresh()
            # return 'complete', 'none', 'ok'
        except:
            newsList = self.browser.find_elements(by = By.CSS_SELECTOR, value = 'div.IFYTLgyk.xAmWmd67:nth-child(1) > ul.qrvPn3bC > li')
            print('video list length: ', len(newsList))
            for item in newsList:
                pass
                # self.extract(item)

        print('quantity:', self.total, '\n')
        # if n == 0:
        #     if self.total > 0:
        #         self.rename()
        #         self.expire()


    # 提取信息，一条的
    def extract(self, item):
        try:
            titleInfo = item.find_element(by = By.CSS_SELECTOR, value = 'div.display-none > a')
            href = titleInfo.get_attribute('href')
            md5 = self.makeMD5(href)

            # dict filter
            if md5 in self.d:
                return
            else:
                self.d[md5] = self.date.split(' ')[0]  # 往dict里插入记录
                self.i += 1
                self.total += 1

            # title = content = item.find_element(by = By.CSS_SELECTOR, value = 'div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > span:nth-child(2) > span:nth-child(1) > span:nth-child(1) > span:nth-child(1) > span:nth-child(1) > span:nth-child(1)').text
            title = content = item.find_element(by = By.CSS_SELECTOR, value = 'div.KxCuain0.QekCqA8W span span.Nu66P_ba').text

            print(href, title, '\ncontent:' + content)
            # self.write_new_file(href, title, self.source, self.i, self.date, 1172664)
        except Exception as e:
            # print('exe', e)
            pass


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
    dy = Douyin({})
    dy.crawl()
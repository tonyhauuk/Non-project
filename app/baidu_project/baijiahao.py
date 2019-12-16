# -*- coding: utf-8 -*-

from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException, NoSuchWindowException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
from os.path import join, getsize
import shutil
from bloom_filter import BloomFilter
from datetime import datetime, date, timedelta
import datetime
import hashlib


class Baijiahao:
    def __init__(self, browser):
        self.browser = browser
        self.timeStamp = int(time.time())
        self.filePath = './baidu/'
        self.filter = BloomFilter(max_elements = 10000000, error_rate = 0.1)
        self.initFilter()

    def crawl(self, url):
        try:
            self.browser.get(url)
        except:
            print('page can not open !!!')

        try:
            self.cleanDir(self.filePath)
            self.browser.find_element_by_xpath('/html/body').send_keys(Keys.END)
            self.i = 0
            while True:
                items = self.browser.find_elements_by_css_selector('div#wrapper_wrapper > div#container.container_l > div#content_left > div > div.result')

                for item in items:
                    time = item.find_element_by_css_selector('div.c-summary.c-row p').text

                    if '小时前' in time or '分钟前' in time:
                        self.extract(item)
                    else:
                        year = datetime.datetime.now().year
                        splitDate = time.split(str(year))
                        fullTime = str(year) + splitDate[1]
                        ts = self.calcDate(fullTime)
                        oneDay = 60 * 60 * 24

                        if self.timeStamp - ts < oneDay:
                            self.extract(item)
                        else:
                            break

                if self.i == 0:
                    break

                try:
                    if self.i == 10:
                        self.browser.find_element_by_partial_link_text('下一页').click()
                        # self.browser.find_element_by_css_selector('html body div#wrapper.wrapper_l p#page > a.n').click()
                    else:
                        break
                except NoSuchElementException:
                    break

                # self.i = 0
        except Exception as e:
            print('Crawl error: ', e)

    def extract(self, item):
        try:

            content = item.find_element_by_css_selector('div.result h3.c-title a')
            href = content.get_attribute('href')

            # bloom-filter
            if self.makeMD5(href) in self.filter:
                return
            else:
                self.writeBloom(href)
                self.i += 1

            title = content.text
            handle = self.browser.current_window_handle
            content.click()
            source = ''
            time.sleep(0.5)

            # switch tab window
            handles = self.browser.window_handles
            for newHandle in handles:
                if newHandle != handle:
                    self.browser.switch_to.window(newHandle)
                    source = self.browser.page_source
                    self.browser.close()
                    self.browser.switch_to.window(handles[0])

            time.sleep(0.5)
            objStr = title + '\n\n' + href + '\n\n\n\n' + source
            self.writeFile(objStr, self.i)
        except (NoSuchElementException, NoSuchAttributeException) as e:
            print('Element error:', e)
        except Exception as e:
            print('Extract Exception: ', e)


    def writeFile(self, objStr, i):
        try:
            if not os.path.exists(self.filePath):
                os.mkdir(self.filePath)

            ts = int(time.time())
            fileName = self.filePath + str(ts) + '_' + str(i) + '.html'
            with open(fileName, mode = 'a+', encoding = 'utf-8') as obj:
                obj.write(objStr)
        except Exception as e:
            print('write file error: ', e)


    def writeBloom(self, href):
        try:
            if not os.path.exists('./record/'):
                os.mkdir('./record/')

            fileName = './record/baijiahao.txt'

            with open(fileName, 'a+') as f:
                current = str(int(time.time()))
                link = self.makeMD5(href)
                string = current + '_' + link  # 取md5码中间8位

                f.write(string + '\n')  # 记录文件
                self.filter.add(link)  # 往bloomfilter里插入记录

        except Exception as e:
            print('write bloom-filter file error: ', self.i, e)


    def calcDate(self, fullTime):
        time1 = fullTime + ':00'
        timeArr = time.strptime(time1, "%Y年%m月%d日 %H:%M:%S")
        timeStamp = int(time.mktime(timeArr))

        return timeStamp


    def cleanDir(self, dir):
        size = 0
        for root, dirs, files in os.walk(dir):
            size += sum([getsize(join(root, name)) for name in files])

        size = int(size / 1024)

        if size > 10000:
            shutil.rmtree(dir)
            os.mkdir(dir)

    def checkBloom(self, fileName):
        try:
            if not os.path.exists(fileName):
                yesterday = (date.today() + timedelta(days = -1)).strftime('%Y-%m-%d')
                with open(yesterday + '-bloom.txt', 'r') as f:
                    line = f.readlines()
                    self.filter.add(line)

                os.remove(yesterday + '-bloom.txt')

            # size = os.path.getsize(fileName)
            # if size == 0:
            #     return
            # content = ''
            # current = int(time.time())
            # day = 60 * 60 * 24
            #
            # if size > 2000:
            #     self.bloom = BloomFilter(max_elements = 1000000, error_rate = 0.01)
            #
            #     file = open(fileName)
            #     for line in file.readlines():
            #         st = int(line.split('_')[0])
            #
            #         if current - st > current - day:
            #             content += line
            #         else:
            #             continue
            #
            #     file.close()
            #
            #     with open(fileName, 'r+') as f:
            #         f.seek(0)
            #         f.truncate()  # 清空文件
            #         f.write(content) # 重新写入新的文件

        except Exception as e:
            print('Check Bloom-Filter error: ', e)


    def recordSet(self, link):
        pass


    def fileChecker(self, link):
        status = False
        files = ['./record/old.txt', './record/new.txt']
        for file in files:
            if not os.path.isfile(file):
                fd = open(file, mode = 'a+', encoding = 'utf-8')
                fd.close()

        for file in files:
            with open(file, 'r') as f:
                lines = f.readlines()

            if len(lines) > 0:
                for line in lines:
                    if link in line:
                        status = True
                        break

                if not status:
                    print(' 不存在 ')
                    size = os.path.getsize(file) / 1024 / 1024
                    size = round(size, 2)
                    if size < 5:
                        with open(file, mode = 'a+', encoding = 'utf-8') as obj:
                            obj.write(link + '\n')
                            break
                    else:
                        if file == './record/old.txt': # old.txt file more than 5MB
                            with open('./record/new.txt', mode = 'a+', encoding = 'utf-8') as obj:
                                obj.write(link + '\n')
                                break
                        elif file == './record/new.txt':
                            os.remove('./record/old.txt')
                            os.rename('./record/new.txt', './record/old.txt')
                            with open('./record/new.txt', mode = 'a+', encoding = 'utf-8') as obj:
                                obj.write(link + '\n')
                            break

                    status = False
                    # return status
            else:
                with open(file, mode = 'a+', encoding = 'utf-8') as obj:
                    obj.write(link + '\n')

                status = False
                # return status

            if status:
                return True
            else:
                return False


    def initFilter(self):
        file = './record/baijiahao.txt'
        try:
            with open(file, mode = 'r') as f:
                lines = f.readlines()

                current = int(time.time())
                day = 60 * 60 * 24
                if len(lines) > 0:
                    for line in lines:
                        t = int(line.split('_')[0])
                        if current - t < day:  # 判断如果时间在一天之内，也加入到filer里
                            md5 = line.split('_')[1]
                            self.filter.add(md5.strip())
        except:
            fd = open(file, mode = 'a+', encoding = 'utf-8')
            fd.close()


    def makeMD5(self, link):
        m = hashlib.md5()
        b = link.encode(encoding = 'utf-8')
        m.update(b)
        link = m.hexdigest()

        return link[8:-8] # 取中间8位md5码


    def close(self):
        self.browser.close()

    def quit(self):
        self.browser.quit()


if __name__ == '__main__':

    opts = webdriver.FirefoxOptions()
    # opts.add_argument('--headless')     # Headless browser
    # opts.add_argument('--disable-gpu')  # Disable gpu acceleration
    profile = webdriver.FirefoxProfile()
    # profile.set_preference('browser.privatebrowsing.autostart', True)  # Start a private browsing
    browser = webdriver.Firefox()
    # browser.set_page_load_timeout(30)

    process = Baijiahao(browser)
    try:
        # url = 'https://www.baidu.com/s?ie=utf-8&cl=2&medium=2&rtt=4&bsst=1&rsv_dl=news_b_pn&tn=news&wd=' + keyword
        # url = 'https://www.baidu.com/s?ie=utf-8&cl=2&medium=2&rtt=4&bsst=1&rsv_dl=news_t_sk&tn=news&word=' + keyword
        # obj = process.crawl(url)
        keyword = ['微软', '立邦', 'nvidia']
        while True:
            url = 'https://www.baidu.com/s?ie=utf-8&cl=2&medium=2&rtt=4&bsst=1&rsv_dl=news_t_sk&tn=news&word=' + keyword[0]
            process.crawl(url)
            break

    except TimeoutException:
        print('The connection has timed out!')
    finally:
        process.quit()


'''
with open 模式
模式 	可做操作 	若文件不存在 	是否覆盖
r 	    只能读 	        报错 	    -
r+ 	    可读可写 	    报错 	    是
w 	    只能写 	        创建 	    是
w+　 	可读可写 	    创建 	    是
a　　 	只能写 	        创建 	    否，追加写
a+ 	    可读可写 	    创建 	    否，追加写


ps -efww|grep opera|grep -v grep|cut -c 9-15|xargs kill


'''

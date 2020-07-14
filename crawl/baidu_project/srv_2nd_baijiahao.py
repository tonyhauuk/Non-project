# -*- coding: utf-8 -*-
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException, NoSuchWindowException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import sys
import os
import hashlib
from os.path import join, getsize
import shutil
from datetime import datetime, date, timedelta
import datetime
from bloom_filter import BloomFilter

import threading

class Baijiahao:
    url = ''
    tasktype = ''
    driver = ''
    returnDataType = ''
    index = 0
    browser = ''
    instance = ''

    def __init__(self, browser):
        self.browser = browser
        self.timeStamp = int(time.time())
        self.filePath = './baidu/'
        self.d = {}
        self.initDict()
        # self.writeDict()


        # self.url = browser.url
        # self.tasktype = browser.tasktype
        # self.browser = browser.driver
        # self.returnDataType = browser.returnDataType
        # self.index = browser.index
        # self.instance = DriverElement()

    def crawl(self):
        print(' -------   execution  --------- \n')
        limit = 'ok'
        self.url = 'https://www.baidu.com/s?ie=utf-8&cl=2&medium=2&rtt=4&bsst=1&rsv_dl=news_t_sk&tn=news&wd=wizcoz%E6%A0%AA%E5%BC%8F%E4%BC%9A%E7%A4%BE&tfflag=0'

        try:
            # if 'error' == self.instance.element_open_link(self.browser, self.url, self.index, sleeptime = 0):
            #     limit = 'error'

            self.browser.get(self.url)
        except:
            print('page can not open !!!')

        if '抱歉，没有找到' in self.browser.page_source:
            print('没有')
            return

        try:
            print('try start ./../....')
            completed = 'complete'
            # self.browser.find_element_by_xpath('/html/body').send_keys(Keys.END)
            self.i = 0

            while True:

                items = self.browser.find_elements_by_css_selector('div#wrapper_wrapper > div#container > div#content_left > div > div.result')


                # items = self.element.elements_lock(self.browser, 'div#wrapper_wrapper > div#container > div#content_left > div > div.result', self.index, sleeptime = 0)

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

                self.i = 0
            return completed, '', limit
        except Exception as e:
            print('Crawl error: ', e)

    # 提取信息，一条的
    def extract(self, item):
        try:
            interval = 0.5
            current = int(time.time())
            content = item.find_element_by_css_selector('div.result h3.c-title a')
            href = content.get_attribute('href')
            md5 = self.makeMD5(href)

            # dict filter
            if md5 in self.d:
                # 更新当前文章的时间戳
                # self.d[md5] = str(current)
                return
            else:
                self.d[md5] = str(current)  # 往dict里插入记录
                self.i += 1

            title = content.text
            handle = self.browser.current_window_handle
            content.click()
            source = ''
            time.sleep(interval)

            # switch tab window
            handles = self.browser.window_handles
            for newHandle in handles:
                if newHandle != handle:
                    self.browser.switch_to.window(newHandle)
                    source = self.browser.page_source
                    self.browser.close()
                    self.browser.switch_to.window(handles[0])

            time.sleep(interval)
            objStr = href + '\n' + title + '\n0\n\n\n\n' + source

            self.writeFile(objStr, current, self.i)
        except (NoSuchElementException, NoSuchAttributeException) as e:
            print('Element error:', e)
        except Exception as e:
            print('Extract Exception: ', e)


    # html生成文件，爬取下来的信息写到文件当中
    def writeFile(self, objStr, ts, i):
        try:
            if not os.path.exists(self.filePath):
                os.mkdir(self.filePath)

            fileName = self.filePath + str(ts) + '_' + str(i) + '.html'
            with open(fileName, 'w+', encoding = 'utf-8') as obj:
                obj.write(objStr)

        except Exception as e:
            print('write file error: ', e)


    # 写入dict记录
    def writeDict(self):
        try:
            threads = []
            t = threading.Thread(target = Baijiahao.deleteExpire, args = (self, ))
            threads.append(t)
            threads[0].start()
            threads[0].join()

        except Exception as e:
            print('write dict file error: ', e)

    # 定时把内存中的字典写入到文件中
    def cleanAndWrite(self):
        interval = 60 * 60 * 1
        fileName = './record/baijiahao.txt'
        while True:
            time.sleep(interval)
            with open(fileName, 'a+') as f:
                f.write(str(self.d))

                # for k, v in self.d.items():
                #     with open(fileName, 'a+') as f:
                #         string = k + '_' + v
                #         f.write(string + '\n')  # 记录文件


    # 日期转换成时间戳
    def calcDate(self, fullTime):
        time1 = fullTime + ':00'
        timeArr = time.strptime(time1, "%Y年%m月%d日 %H:%M:%S")
        timeStamp = int(time.mktime(timeArr))

        return timeStamp

    # 清理文件夹
    def cleanDir(self, dir):
        try:
            size = 0
            for root, dirs, files in os.walk(dir):
                size += sum([getsize(join(root, name)) for name in files])

            size = int(size / 1024)

            capa = 50000  # 值是KB
            if size > capa:
                shutil.rmtree(dir)
                os.mkdir(dir)
        except:
            print('No file !!!')

    # 初始化字典， 把从文件当中读出来的字符串转成字典格式，写入到内存当中
    def initDict(self):
        file = './record/baijiahao.txt'
        try:
            with open(file, mode = 'r') as f:
                line = f.readline()
                if line != '':
                    self.d = eval(str(line)) # 直接把字符串转成字典格式
        except:
            # 如果没有文件，则直接创建文件
            fd = open(file, mode = 'a+', encoding = 'utf-8')
            fd.close()

    # 生成md5
    def makeMD5(self, link):
        m = hashlib.md5()
        b = link.encode(encoding = 'utf-8')
        m.update(b)
        link = m.hexdigest()

        return link


    # 删除过期记录
    def deleteExpire(self):
        now = datetime.datetime.now()
        nextTime = now + datetime.timedelta(days = +1)
        nextYear = nextTime.date().year
        nextMonth = nextTime.date().month
        nextDay = nextTime.date().day
        # 时间设置成凌晨3点，这个时间段信息相对来说比较少，更新文件冲突较少
        nextDayTime = datetime.datetime.strptime(str(nextYear) + '-' + str(nextMonth) + '-' + str(nextDay) + ' 03:00:00', '%Y-%m-%d %H:%M:%S')
        timerStartTime = (nextDayTime - now).total_seconds()
        timer = threading.Timer(timerStartTime, self.expire)
        timer.start()


    # 内存字典：每天凌晨3点执行这个程序，程序检查文件当中的过期数据
    def expire(self):
        # 检查过期数据
        li = []
        current = int(time.time())
        day = 60 * 60 * 24
        for k, v in self.d.items():
            if current - int(v) > day: # 如果时间戳的差大于1天的秒数，就删除
                li.append(k)

        # 删除字典里过期的数据
        for i in li:
            self.d.pop(i)


        # 更新txt文件
        fileName = './record/baijiahao.txt'
        os.remove(fileName)
        with open(fileName, 'a+') as f:
            f.write(str(self.d))


        # 文件夹过大删除
        self.cleanDir('./baidu/')

        end = int(time.time()) - current
        # interval = 86400 - end  # 下一次间隔多久来执行这个程序，每次的执行时间不固定，所以得用总时间来减去当前所用的时间，得出的差就是执行下次一次需要的秒数
        # timer = threading.Timer(interval, self.expire)
        # timer.start()


    # 文件形式： 每天凌晨3点执行这个程序，程序检查文件当中的过期数据
    def expireFile(self):
        try:
            lst = list()
            current = int(time.time())
            # 读取当前的文件
            with open ('./record/baijiahao.txt', mode = 'r') as f:
                lines = f.readlines()
                day = 60 * 60 * 24
                if len(lines) > 0:
                    for line in lines:
                        t = int(line.split('_')[1])
                        if current - t < day:  # 判断如果时间在一天之内，加入到数组中
                            lst.append(line)

            # 写一个新的文件，记录的都是删除过期记录的信息
            with open('./record/tmp_baijiahao.txt', mode = 'a+', encoding = 'utf-8') as f:
                for text in lst:
                    f.write(text)

            # 删除旧文件，把tmp文件名修改成刚才删除文件的名称
            os.remove('./record/baijiahao.txt')
            os.rename('./record/tmp_baijiahao.txt', './record/baijiahao.txt')

            end = int(time.time()) - current
            interval = 86400 - end  # 下一次间隔多久来执行这个程序，每次的执行时间不固定，所以得用总时间来减去当前所用的时间，得出的差就是执行下次一次需要的秒数
            timer = threading.Timer(interval, self.expireFile)
            timer.start()
        except:
            pass





    ''' 
        下面的程序暂时用不到，先保留
    '''

    # 检查bloomfilter的记录
    def checkBloom(self, fileName):
        try:
            if not os.path.exists(fileName):
                yesterday = (date.today() + timedelta(days = -1)).strftime('%Y-%m-%d')
                with open(yesterday + '-bloom.txt', 'r') as f:
                    line = f.readlines()
                    self.bloom.add(line)

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

    # 记录文件的检查函数
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

            if len(lines) > 0:  # 如果文件有记录，就继续检查
                for line in lines:
                    if link in line:
                        status = True
                        break

                if not status:
                    size = os.path.getsize(file) / 1024 / 1024
                    size = round(size, 2)
                    if size < 5:
                        with open(file, mode = 'a+', encoding = 'utf-8') as obj:
                            obj.write(link + '\n')
                            break
                    else:
                        if file == './record/old.txt':  # old.txt file more than 5MB
                            with open('./record/new.txt', mode = 'a+', encoding = 'utf-8') as obj:
                                obj.write(link + '\n')
                                break
                        elif file == './record/new.txt':  # 如果new文件大于5MB，先删除old文件，并且把new文件名修改成old
                            os.remove('./record/old.txt')
                            os.rename('./record/new.txt', './record/old.txt')
                            with open('./record/new.txt', mode = 'a+', encoding = 'utf-8') as obj:
                                obj.write(link + '\n')
                            break

                    status = False
                    # return status
            else:  # 如果文件没有记录，直接写入
                with open(file, mode = 'a+', encoding = 'utf-8') as obj:
                    obj.write(link + '\n')

                status = False
                # return status

            if status:
                return True
            else:
                return False

    # 初始化bloomfilter
    def initBF(self):
        # 先读取前一天的记录，如果没有，建立一个当天的新文件
        try:
            yesterday = (date.today() + timedelta(days = -1)).strftime('%Y-%m-%d')
            file = './record/' + yesterday + '_baijiahao.txt'
            with open(file, mode = 'r') as f:
                lines = f.readlines()

            current = int(time.time())
            day = 60 * 60 * 24
            if len(lines) > 0:
                for line in lines:
                    t = int(line.split('_')[0])
                    if current - t < day:  # 判断如果时间在一天之内，也加入到filer里
                        self.filter.add(line)
        except:
            # 建立当天的新文件，如果有记录，就加入到filter里
            file = str(datetime.date.today()) + '-bloom.txt'
            with open(file, mode = 'r') as f:
                lines = f.readlines()

            if len(lines) > 0:
                for line in lines:
                    self.filter.add(line)


if __name__ == '__main__':
    browser = webdriver.Firefox()
    process = Baijiahao(browser)
    try:
        while True:
            process.crawl()
            process.expire()
            time.sleep(2)

    except TimeoutException:
        print('The connection has timed out!')
    finally:
        browser.quit()

'''
with open 模式
模式 	可做操作 	若文件不存在 	是否覆盖
r 	    只能读 	        报错 	    -
r+ 	    可读可写 	    报错 	    是
w 	    只能写 	        创建 	    是
w+　 	可读可写 	    创建 	    是
a　　 	只能写 	        创建 	    否，追加写
a+ 	    可读可写 	    创建 	    否，追加写

'''

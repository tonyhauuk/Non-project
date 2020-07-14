# -*- coding: utf-8 -*-

from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException, WebDriverException, StaleElementReferenceException, \
    NoSuchWindowException
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os ,json
from datetime import datetime, date, timedelta
import datetime
import hashlib
import threading

class Toutiao:

    def __init__(self, browser):
        self.browser = browser
        self.d = {}
        # self.initDict()
        # self.writeDict()

    def crawl(self, url):
        self.i = 0

        try:
            self.browser.get(url)
            self.browser.refresh()
        except:
            print('page can not open !!!')

        try:
            self.browser.find_element_by_css_selector('div.feedBox div div.no-feed')
            print('没有查询结果....\n')
            return 'complete', 'none', 'ok'
        except NoSuchElementException:
            pass

        # height = []
        # height.append(self.browser.execute_script("return document.body.scrollHeight;"))

        for i in range(5):
            try:
                self.browser.find_element_by_xpath('/html/body').send_keys(Keys.END)
                WebDriverWait(self.browser, 20, 0.5).until_not(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, '加载中')))
                # checkHeight = self.browser.execute_script("return document.body.scrollHeight;")
                # if checkHeight == height[-1]:
                #     break
                # else:
                #     height.append(checkHeight)
            except (NoSuchElementException, WebDriverException):
                print('exception \n')

        try:
            sections =  WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'html body div.y-wrap div.y-box.container div.y-left.index-middle div.feedBox div div.sections')))
            slices = sections.find_elements_by_css_selector('div.articleCard')

            for section in slices:
                # ptime = section.find_element_by_css_selector('div.item div.item-inner.y-box div.normal.rbox div.rbox-inner div.y-box.footer div.y-left span.lbtn').text
                ptime = section.find_element_by_css_selector('div.item div.item-inner div.normal div.rbox-inner div.footer div.y-left span.lbtn').text
                if '小时前' in ptime or '分钟前' in ptime:
                    self.extract(section)

        except (NoSuchElementException, WebDriverException) as e:
            print(e, self.i)

        if self.i == 0:
            return 'complete', 'none', 'ok'

        print('Number : ', self.i, '\n', 'total dict: ', json.dumps(self.d))

    def extract(self, section):
        try:
            interval = 1
            current = int(time.time())
            linkTitle = section.find_element_by_css_selector('div.item div.item-inner.y-box div.normal.rbox div.rbox-inner div.title-box a')
            href = linkTitle.get_attribute('href')
            md5 = self.makeMD5(href)

            # dict filter
            if md5 in self.d:
                return
            else:
                self.d[md5] = str(current)  # 往dict里插入记录
                self.i += 1


            title = linkTitle.text
            handle = self.browser.current_window_handle
            linkTitle.click()
            time.sleep(interval)

            # switch tab window
            handles = self.browser.window_handles
            for newHandle in handles:
                if newHandle != handle:
                    self.browser.switch_to.window(newHandle)
                    time.sleep(interval)
                    self.source = self.browser.page_source
                    self.browser.close()
                    self.browser.switch_to.window(handles[0])


            objstr = title + '\n' + href + '\n' + self.source
            self.writeFile(objstr, current, self.i)
            # self.write_new_file(href, title, self.source, self.i)
        except:
            pass





    # 初始化字典， 把从文件当中读出来的字符串转成字典格式，写入到内存当中
    def initDict(self):
        file = './record/toutiao.txt'
        try:
            with open(file, mode='r') as f:
                line = f.readline()
                if line != '' or line != '{}':
                    self.d = eval(str(line))  # 直接把字符串转成字典格式
        except:
            # 如果没有文件，则直接创建文件
            fd = open(file, mode='a+', encoding='utf-8')
            fd.close()


    # 写入dict记录
    def writeDict(self):
        try:
            threads = []
            t1 = threading.Thread(target = Toutiao.deleteExpire, args = (self, ))
            threads.append(t1)
            # t2 = threading.Thread(target=Toutiao.persistence, args=(self,))
            # threads.append(t2)

            threads[0].start()
            # threads[1].start()
            threads[0].join()
            # threads[1].join()
        except Exception as e:
            print('threading error : ', e)


    # 生成md5
    def makeMD5(self, link):
        m = hashlib.md5()
        b = link.encode(encoding='utf-8')
        m.update(b)
        link = m.hexdigest()

        return link


    # 删除过期记录
    def deleteExpire(self):
        now = datetime.datetime.now()
        nextTime = now + datetime.timedelta(days=1)
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
            if current - int(v) > day:  # 如果时间戳的差大于1天的秒数，就删除
                li.append(k)

        # 删除字典里过期的数据
        for i in li:
            self.d.pop(i)

        # 更新txt文件
        fileName = './record/toutiao.txt'
        os.remove(fileName)
        with open(fileName, 'a+') as f:
            f.write(str(self.d))

        end = int(time.time()) - current
        interval = 86400 - end  # 下一次间隔多久来执行这个程序，每次的执行时间不固定，所以得用总时间来减去当前所用的时间，得出的差就是执行下次一次需要的秒数
        timer = threading.Timer(interval, self.expire)
        timer.start()

    # html生成文件，爬取下来的信息写到文件当中
    def writeFile(self, objStr, ts, i):
        try:
            self.filePath = './html/'
            if not os.path.exists(self.filePath):
                os.mkdir(self.filePath)

            fileName = self.filePath + str(ts) + '_' + str(i) + '.html'
            with open(fileName, 'w+', encoding='utf-8') as obj:
                obj.write(objStr)

        except Exception as e:
            print('write file error: ', e)

    def quit(self):
        browser.quit()


if __name__ == '__main__':
    browser = webdriver.Firefox()
    # browser.set_window_size(800, 640)
    # browser.implicitly_wait(10)
    browser.set_page_load_timeout(300)
    browser.set_script_timeout(300)
    process = Toutiao(browser)
    try:
        keyword = ['微软', '经济', 'nvidia', '@']
        while True:
            url = 'https://www.toutiao.com/search/?keyword=' + keyword[2]
            process.crawl(url)
            # time.sleep(5)
            break

    except TimeoutException:
        print('The connection has timed out!')
    finally:
        pass

# coding: utf-8
# -*- coding: utf-8 -*-
import time, requests, bs4, datetime, re, hashlib, os, sys, json
from time import sleep
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException, \
    NoSuchWindowException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# sys.path.append('../')
# import crawlerfun


class Crawler:
    def __init__(self, d):
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        self.date = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        self.d = d
        self.dir = self._dir = ''
        # self.ipnum = crawlerfun.ip2num('61.130.181.229')
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0",
        }
        self.debug = True


    def doJob(self):
        n = 0
        for key, value in self.schedule():  # 获取频道链接
            self.doCrawl(key, value)
            n += 1
            if n == 1:
                break



    # 开始爬
    def doCrawl(self, colName, url):
        self.i = self.total = 0
        self.startBrowser()
        self.browser.get(url)
        # 左边频道列表点击, 循环
        leftList = self.browser.find_elements_by_css_selector('div.caidan-left-div > div.caidan-left > ul.caidan-left-yiji > li.x.in.menuData')
        for lst in leftList:
            try:
                # 点击更多, 如果没有略过
                self.browser.find_element_by_css_selector('div.list.ng-scope > div.tabs > div.tab.active > a').click()
            except NoSuchElementException:
                pass

            try:
                rightLst = self.browser.find_elements_by_css_selector('div.row > div.ng-scope > div.list.caidan-right-list')
                self.normalCrawl(rightLst)
            except Exception as e:
                print(e)
            finally:
                sleep(10)
                self.close()

            listName = lst.find_element_by_tag_name('a').text
            if '政策解读' == listName: # 如果当前文字符合list名称，直接跳过不采集
                continue
            else:
                lst.find_element_by_tag_name('a').click()

        # if self.total > 0:
        #     self.rename()
        #     self.expire()


    # 正常采集
    def normalCrawl(self, items):
        for item in items:
            # 找到不包含class是ng-hide的div标签，他们的网站会隐藏某些div, 导致爬取的信息比看到的要多
            divs = item.find_elements_by_css_selector('div.panel-row.ng-scope:not(.ng-hide)')
            for div in divs:
                dateTime = div.find_element_by_css_selector('span.date.ng-binding').text
                # if dateTime.text in self.date:
                self.extract(div, dateTime)


    # 提取信息，一条的
    def extract(self, item, dateTime):
        try:
            interval = 1
            titleInfo = item.find_element_by_css_selector('span > a')
            href = titleInfo.get_attribute('href')
            md5 = self.makeMD5(href)

            # dict filter
            if md5 in self.d:
                return
            else:
                self.d[md5] = self.date.split(' ')[0]  # 往dict里插入记录
                self.i += 1
                self.total += 1

            title = titleInfo.get_attribute('title')
            handle = self.browser.current_window_handle
            titleInfo.click()

            # switch tab window
            handles = self.browser.window_handles
            for newHandle in handles:
                if newHandle != handle:
                    self.browser.switch_to.window(newHandle)
                    time.sleep(interval)
                    self.source = self.browser.page_source
                    self.browser.close()
                    self.browser.switch_to.window(handles[0])

            if self.debug:
                print('count: ', self.total)

            # self.write_new_file(href, title, self.source, self.i)
        except (NoSuchElementException, NoSuchAttributeException) as e:
            print('Element error:', e)
        except Exception:
            pass


    def startBrowser(self):
        opts = webdriver.ChromeOptions()
        opts.add_argument('--no-sandbox')
        opts.add_argument('--disable-gpu')
        opts.add_argument(
            'user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"')
        opts.add_argument('--disk-cache-dir=%s' % 'D:\PyProject\/Non-project\/app\/banking\cache')
        # 为Chrome开启实验性功能参数excludeSwitches，它的值为['enable-automation']
        opts.add_experimental_option('excludeSwitches', ['enable-automation'])
        opts.add_experimental_option('excludeSwitches', ['enable-logging'])

        # self.browser = webdriver.Chrome(chrome_options = opts)
        self.browser = webdriver.Firefox()
        '''
            self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                Object.defineProperty(navigator, 'webdriver', {
                  get: () => undefined
                })
              """
            })
        '''


    # 关闭标签或者窗口
    def close(self):
        self.browser.close()


    # 退出浏览器
    def quit(self):
        self.browser.quit()


    # 重启浏览器
    def restartBrowser(self):
        self.quit()
        self.startBrowser()


    # 读取链接
    def schedule(self):
        filName = './column_list.json'
        f = open(filName, encoding = 'utf-8')
        obj = json.load(f)
        items = obj.items()

        return items


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
            fileName = './md5.txt'
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

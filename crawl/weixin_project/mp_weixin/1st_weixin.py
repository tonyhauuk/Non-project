# coding: utf-8
import requests, random, re, time, hashlib, os, json, sys, subprocess
from http import cookiejar
from urllib import request, parse
from time import sleep
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from apscheduler.schedulers.blocking import BlockingScheduler

sys.path.append('..')
import crawlerfun
from crawlerfun import ClearCache


class MpWeixin:
    def __init__(self, browser):
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        self.date = time.strftime('%Y-%m-%d %H:%M:%S', timeArray)
        self.projectName = 'mp_weixin'
        self.d = crawlerfun.initDict(self.projectName)
        self.browser = browser
        self.dir = self._dir = self.source = ''
        self.ipnum = crawlerfun.ip2num('192.168.149.51')
        self.debug = True


    def crawl(self):
        self.total = 0
        i = 0
        status = True
        file = './userList.json'
        with open(file, mode = 'r') as f:
            keywords = json.load(f)
            for key in keywords:  # 关键词循环
                for account in keywords[key]:  # 公众号循环
                    n = self.doCrawl(key, account)
                    if n == -1:
                        status = False
                        break
                    else:
                        i += n

        if status:
            if i > 0:
                # crawlerfun.deleteFiles(self.projectName)
                return 'complete', self.source, 'ok'
            else:
                return 'complete', 'none', 'ok'
        else:
            return 'interrupt', 'none', 'error'


    def doCrawl(self, key, account):
        print('\nkey: ', key, '| account: ', account)
        self.i = 0
        try:
            url = 'https://weixin.sogou.com/weixin?type=1&query=' + account + '&ie=utf8&s_from=input&_sug_=y&_sug_type_='
            self.browser.get(url)
            # sleep(1)
            WebDriverWait(self.browser, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.news-box > ul.news-list2 > li')))
        except TimeoutException:
            return -1

        while True:
            newsList = self.browser.find_elements_by_css_selector('div.news-box > ul.news-list2 > li')
            for item in newsList:
                try:
                    dateTime = item.find_element_by_css_selector('dl:last-child > dd > span').text
                except:
                    continue

                if '前' in dateTime and '天前' not in dateTime:
                    self.extract(item, account)
                else:
                    continue

            try:
                self.browser.find_element_by_partial_link_text('下一页').click()  # 点击下一页
            except NoSuchElementException:
                break

        if self.total > 0:
            crawlerfun.renameNew()
            crawlerfun.expire(self.date, self.d, self.projectName)

            return self.total
        else:
            return 0


    # 提取信息，一条的
    def extract(self, item, account):
        titleInfo = item.find_element_by_css_selector('dd > a')
        title = titleInfo.text
        tag = title + '|' + account
        try:
            md5 = crawlerfun.makeMD5(tag)

            # dict filter
            if md5 in self.d:
                return
            else:
                self.d[md5] = self.date.split(' ')[0]  # 往dict里插入记录
                self.i += 1
                self.total += 1

            handle = self.browser.current_window_handle  # 拿到当前页面的handle
            titleInfo.click()

            # switch tab window
            WebDriverWait(self.browser, 10).until(EC.number_of_windows_to_be(2))
            handles = self.browser.window_handles
            for newHandle in handles:
                if newHandle != handle:
                    self.browser.switch_to.window(newHandle)  # 切换到新标签
                    sleep(1)  # 等个几秒钟
                    # WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div#js_content')))
                    self.source = self.getPageText()  # 拿到网页源码
                    self.link = self.browser.current_url  # 获取当前网页的链接
                    self.browser.close()  # 关闭当前标签页
                    self.browser.switch_to.window(handle)  # 切换到之前的标签页
                    break

            self.write_new_file(self.link, title, self.source, self.i, self.date, 1152937)
        except (NoSuchElementException, NoSuchAttributeException) as e:
            print('Element error:', e)
        except Exception:
            return


    def getPageText(self):  # 获取网页正文
        try:
            html = self.browser.find_element_by_css_selector('div#js_content').get_attribute('innerHTML')
        except NoSuchElementException:
            html = self.browser.page_source

        return html


    def write_new_file(self, url, title, source, i, time, id):
        content = '''
                <html>
                    <head> 
                       <meta charset="utf-8">
                       <meta name="keywords" content="estarinfo">
                       <title>''' + title + '''</title>
                    </head> 
                    <body>
                        <h1 class="title">''' + title + '''</h1>
                        <span class="time">''' + time + '''</span>
                        <span class="source">''' + str(id) + '''</span>
                        <div class="article">''' + source + '''</div>
                    </body>
                </html>
                '''
        page_text = url + '\n' + title + '\n' + str(id) + '\n\n\n\n' + content

        if self.debug:
            print('count:', self.i, ' --- ', title)

        if '' == self._dir:
            self.crawl_mkdir()

        filename = self._dir + 'iask_' + str(i) + '_' + str(len(self.d)) + '.htm-2'
        for num in range(2):
            if 1 == crawlerfun.write_file(filename, page_text, ifdisplay = 0):
                # savePath = '/root/estar_save/' + self.projectName + '/'
                # if not os.path.exists(savePath):
                #     os.makedirs(savePath)
                # fileName = savePath + 'iask_' + str(i) + '_' + str(len(self.d)) + '.htm-2'
                # crawlerfun.write_file(fileName, page_text, ifdisplay = 0)  # 再次保存到/root/estar_save目录下

                break
            else:  # 有时目录会被c程序删掉
                crawlerfun.mkdir(self._dir)


    def crawl_mkdir(self):
        dirroot = '/estar/newhuike2/1/'
        tm_s, tm_millisecond = crawlerfun.get_timestamp(ifmillisecond = 1)
        dirsmall = 'iask' + str(self.ipnum) + '.' + str(1) + '.' + str(tm_s) + '.' + str(tm_millisecond) + '/'
        self._dir = dirroot + '_' + dirsmall
        self.dir = dirroot + dirsmall

        return self._dir, self.dir


def clean(browser):
    subprocess.Popen('rm -rf /dev/shm/cache', shell = True, stdout = subprocess.PIPE)
    subprocess.Popen('rm nohup.out -rf', shell = True, stdout = subprocess.PIPE)
    subprocess.Popen('tmpwatch 1 /tmp/', shell = True, stdout = subprocess.PIPE)
    ClearCache(browser)


def startBrowser():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-logging')
    options.add_argument("--disable-infobars")
    options.add_argument(
        'user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.103 Safari/537.36"')
    options.add_argument('--disk-cache-dir=%s' % '/dev/shm/cache')
    browser = webdriver.Chrome(chrome_options = options)
    browser.set_window_size(1050, 685)
    browser.set_window_position(x = 225, y = 0)
    clean(browser)

    return browser


def getUserList():
    d = getAccountList()

    with open('../../kw_weixin_more.txt', mode = 'r', encoding = 'utf-8') as f:
        keywords = f.readlines()

    browser = startBrowser()
    try:

        for keyword in keywords:
            keyword = keyword.strip()
            keyword = parse.unquote(keyword, encoding = 'utf-8', errors = 'replace')

            # keyword = parse.quote(keyword)
            try:
                userList = d[keyword]
            except KeyError:
                userSet = set()
            else:
                userSet = set(userList)

            url = 'https://weixin.sogou.com/weixin?type=2&s_from=input&query=' + keyword + '&ie=utf8'
            browser.get(url)

            for i in range(10):
                itemList = browser.find_elements_by_css_selector('div.news-box > ul.news-list > li')
                for item in itemList:
                    account = item.find_element_by_css_selector('div.txt-box > div.s-p > a').text
                    userSet.add(account)

                try:
                    browser.find_element_by_partial_link_text('下一页').click()
                except NoSuchElementException:
                    break

            userList = list(userSet)
            d[keyword] = userList
    except Exception as e:
        print(e)
    finally:
        browser.quit()
        print('=' * 10, 'mp account finished!', '=' * 10, '\n')

    # 更新txt文件
    try:
        fileName = './userList.json'
        jsonStr = json.dumps(d, indent = 4, ensure_ascii = False).replace("'", '"')
        with open(fileName, 'w') as json_file:
            json_file.write(jsonStr)

    except Exception as e:
        print('expire exception: ', e)


def getAccountList():
    d = {}
    file = './userList.json'
    try:
        with open(file, mode = 'r') as f:
            jsonStr = json.load(f)
            if jsonStr != '':
                d = eval(str(jsonStr))  # 直接把字符串转成字典格式

        return d
    except Exception as e:
        # 如果没有文件，则直接创建文件
        fd = open(file, mode = 'a+', encoding = 'utf-8')
        fd.close()

        return d


def crawlWeixin():
    browser = startBrowser()
    try:
        w = MpWeixin(browser)
        for i in range(2):
            w.crawl()
            sleep(10)
    except Exception as e:
        print('crawl weixin exception:', e)
    finally:
        browser.quit()


if __name__ == '__main__':
    crawlWeixin()

    scheduler = BlockingScheduler()
    # scheduler.add_job(getUserList, 'cron', day = '*', hour = 4)     # 每天凌晨4点执行更新公众号程序
    scheduler.add_job(crawlWeixin, 'cron', day = '*', hour = 7)  # 每天7点开始采集公众号信息

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemError):
        scheduler.shutdown(wait = False)

# coding: utf-8
import requests, random, re, time, hashlib, os, json, sys, subprocess, configparser, ddddocr
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
from selenium.webdriver.opera.options import Options as operaOptions

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
        self.pageNum = self.getPageNum()


    def crawl(self):
        file = './userList.json'
        with open(file, mode = 'r') as f:
            keywords = json.load(f)
            for key in keywords:  # 关键词循环
                for value in keywords[key]:  # 公众号循环
                    if value.get('state') == 0:
                        continue

                    self.doCrawl(key, value.get('nickname'))


    def doCrawl(self, key, nickname):
        self.i = 0
        try:
            url = 'https://weixin.sogou.com/weixin?type=1&query=' + nickname + '&ie=utf8&s_from=input&_sug_=y&_sug_type_='
            self.browser.get(url)
            sleep(3)

            if 'antispider' in browser.current_url:     # 检查是否被ban
                self.checkBanned()

            try:
                self.browser.find_element_by_css_selector('div.b404-box > div.text-info')  # 公众号没有文章
                self.recordNone(key, nickname)
                return
            except NoSuchElementException:
                pass

            print('\n' + key + ': ' + nickname)
        except Exception:
            return

        while True:
            newsList = self.browser.find_elements_by_css_selector('div.news-box > ul.news-list2 > li')
            for item in newsList:
                try:
                    dateTime = item.find_element_by_css_selector('dl:last-child > dd > span').text
                except NoSuchElementException:
                    continue

                if '前' in dateTime and '天前' not in dateTime:
                    self.extract(item, nickname)
                else:
                    continue

            if self.pageNum > 0:
                try:
                    self.browser.find_element_by_partial_link_text('下一页').click()
                except NoSuchElementException:
                    break
            elif self.pageNum == 0:
                break

        if self.i > 0:
            crawlerfun.renameNew()
            crawlerfun.expire(self.date, self.d, self.projectName)

        return self.browser



    # 提取信息，一条的
    def extract(self, item, nickname):
        titleInfo = item.find_element_by_css_selector('dd > a')
        title = titleInfo.text
        tag = title + '|' + nickname
        try:
            # href = titleInfo.get_attribute('href')
            md5 = crawlerfun.makeMD5(tag)
            link = ''
            # dict filter
            if md5 in self.d:
                return
            else:
                self.d[md5] = self.date.split(' ')[0]  # 往dict里插入记录
                self.i += 1

            handle = self.browser.current_window_handle  # 拿到当前页面的handle
            titleInfo.click()

            # switch tab window
            WebDriverWait(self.browser, 10).until(EC.number_of_windows_to_be(2))
            handles = self.browser.window_handles
            for newHandle in handles:
                if newHandle != handle:
                    self.browser.switch_to.window(newHandle)        # 切换到新标签
                    sleep(2)                                        # 等个几秒钟
                    self.source = self.getPageText()                # 拿到网页源码
                    link = self.browser.current_url                 # 获取当前网页的链接
                    # self.bottomNews(self.browser, handle)         # 底部3条信息
                    sleep(1)                                        # 强制等1秒
                    self.browser.close()                            # 关闭当前标签页
                    self.browser.switch_to.window(handle)           # 切换到之前的标签页
                    break

            self.write_new_file(link, title, self.source, self.i, self.date, 1152937)
        except Exception as e:
            try:
                self.browser.refresh()
            except Exception as e:
                print('after refresh error: ', e, '-' * 10)
                self.i -= 1
                crawlerfun.renameNew()
                crawlerfun.expire(self.date, self.d, self.projectName)

                raise Exception



    def bottomNews(self, browser, handle):
        self.browser.find_element_by_xpath('/html/body').send_keys(Keys.END)
        current = int(time.time())
        newsList = browser.find_elements_by_css_selector('a.weui-media-box.weui-media-box_appmsg.js_related_item')
        for item in newsList:
            try:
                dateTime = int(item.get_attribute('data-time'))
            except:
                continue

            if current - dateTime < 86400:
                self.extractSingle(item, handle)
            else:
                continue

        sleep(1)


    def extractSingle(self, item, firstHandle):
        titleInfo = item.find_element_by_css_selector('div > div.weui_ellipsis_mod_inner')
        title = titleInfo.text
        try:
            # href = item.get_attribute('data-url')
            md5 = crawlerfun.makeMD5(title)
            link = ''
            # dict filter
            if md5 in self.d:
                return
            else:
                self.d[md5] = self.date.split(' ')[0]  # 往dict里插入记录
                self.i += 1

            handle = self.browser.current_window_handle  # 拿到当前页面的handle
            titleInfo.click()

            # switch tab window
            WebDriverWait(self.browser, 10).until(EC.number_of_windows_to_be(3))
            handles = self.browser.window_handles
            for newHandle in handles:
                if newHandle != handle and newHandle != firstHandle:
                    self.browser.switch_to.window(newHandle)    # 切换到新标签
                    sleep(1)                                    # 等个几秒钟
                    self.source = self.getPageText()            # 拿到网页源码
                    link = self.browser.current_url             # 获取当前网页的链接
                    self.browser.close()                        # 关闭当前标签页
                    sleep(1)
                    self.browser.switch_to.window(handle)       # 切换到之前的标签页
                    break

            self.write_new_file(link, title, self.source, self.i, self.date, 1152937)
        except Exception as e:
            print('single error:', e, self.date)
            self.i -= 1
            crawlerfun.renameNew()
            crawlerfun.expire(self.date, self.d, self.projectName)
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


    def getPageNum(self):
        configFile = 'weixin.ini'
        conf = configparser.ConfigParser()
        conf.read(configFile)
        sections = conf.sections()
        option = conf.options(sections[1])

        pageNum = conf.get(sections[1], option[0])  # 采集模式：全采集，精确采集

        return int(pageNum)


    def checkBanned(self):
        imgFile = 'codeImage.png'
        for i in range(5):
            if i > 0:
                if 'antispider' in browser.current_url:
                    browser.find_element(by = By.CSS_SELECTOR, value = 'a#change-img').click()  # 点击换一张
                    sleep(2)

                    browser.execute_script('document.body.style.zoom="0.8"')
                    verify = browser.find_element(by = By.CSS_SELECTOR, value = 'img#seccodeImage')
                    verify.screenshot(imgFile)

                    ocr = ddddocr.DdddOcr(show_ad = False)

                    with open(imgFile, 'rb') as f:
                        byte = f.read()

                    res = ocr.classification(byte)
                    print('Submit verify code times:', i, '. The Code: ' + res + '\n')

                    os.remove(imgFile)

                    browser.find_element(by = By.CSS_SELECTOR, value = 'input#seccodeInput').send_keys(res)  # 输入验证码
                    sleep(2)
                    browser.find_element(by = By.CSS_SELECTOR, value = 'a#submit').click()  # 点击‘提交’按钮
                else:
                    break


    def recordNone(self, key, nickname):
        print('[' + key + '->' + nickname + ']', 'has no article!\n')

        with open('./none.txt', 'a+', newline = '\n') as f:
            f.write(key + '|' + nickname + '\n')


    def updateJson(self):
        oldFile = './userListOld.json'
        newFile = './userList.json'

        with open(newFile, 'r') as jsonFile:
            obj = json.load(jsonFile)

        with open('./none.txt', 'r', newline = '\n') as f:
            for line in f.readlines():
                key = line.split('|')[0]
                nickname = line.split('|')[1].strip()

                values = obj[key]
                for value in values:
                    if value.get('nickname') == nickname:
                        value['state'] = 0

        if os.path.exists(newFile):
            os.remove(newFile)
        else:
            try:
                os.rename(newFile, oldFile)
            except Exception as e:
                print(e)

        with open(newFile, 'w') as fp:
            json.dump(obj, fp, indent = 2, ensure_ascii = False)

        if os.path.exists('./none.txt'):
            os.remove('./none.txt')



def clean(browser):
    subprocess.Popen('rm -rf /dev/shm/cache', shell = True, stdout = subprocess.PIPE)
    subprocess.Popen('rm nohup.out -rf', shell = True, stdout = subprocess.PIPE)
    subprocess.Popen('tmpwatch 1 /tmp/', shell = True, stdout = subprocess.PIPE)
    ClearCache(browser)


def startBrowser():
    # options = webdriver.ChromeOptions()
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-gpu')
    # options.add_argument('--disable-logging')
    # options.add_argument("--disable-infobars")
    # options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.103 Safari/537.36"')
    # options.add_argument('--disk-cache-dir=%s' % '/dev/shm/cache')
    # browser = webdriver.Chrome(chrome_options = options)
    # browser.set_window_size(1135, 685)
    # browser.set_window_position(x = 225, y = 0)
    # clean(browser)

    options = operaOptions()
    options.binary_location = '/usr/lib64/opera/opera'
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-logging')
    options.add_argument('--disable-plugins')
    options.add_argument('--disable-java')
    browser = webdriver.Opera(options = options, executable_path = '/usr/bin/operadriver')
    browser.set_window_size(1200, 685)
    browser.set_window_position(x = 150, y = 0)


    return browser

def crawlWeixin():
    for i in range(2):
        browser = startBrowser()
        try:
            w = MpWeixin(browser)
            w.crawl()
        except Exception as e:
            pass
        finally:
            browser.quit()


def loopCrawl():
    while True:
        browser = startBrowser()
        w = MpWeixin(browser)
        try:
            w.crawl()
            browser.quit()
        except Exception as e:
            browser.quit()
            print('loop exception:', e)
        finally:
            if os.path.exists('./none.txt'):    # 如果有none.txt文件，就更新userList.json 文件
                w.updateJson()
            browser.quit()

if __name__ == '__main__':
    loopCrawl()
    exit()

    # crawlWeixin()

    scheduler = BlockingScheduler()
    # scheduler.add_job(getUserList, 'cron', day = '*', hour = 4)         # 每天凌晨4点执行更新公众号程序
    scheduler.add_job(crawlWeixin, 'cron', day = '*', hour = 7)         # 每天7点开始采集公众号信息

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemError):
        scheduler.shutdown(wait = False)

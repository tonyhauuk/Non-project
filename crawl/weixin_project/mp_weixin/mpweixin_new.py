# coding: utf-8
import requests, random, re, time, hashlib, os, json, sys, subprocess, configparser, ddddocr
from http import cookiejar
from urllib import request, parse
from time import sleep
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException, StaleElementReferenceException, WebDriverException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from apscheduler.schedulers.blocking import BlockingScheduler

# from selenium.webdriver.opera.options import Options as operaOptions

sys.path.append('..')
import crawlerfun
from crawlerfun import ClearCache


class MpWeixin:
    def __init__(self):
        self.projectName = 'mp_weixin'
        self.d = crawlerfun.initDict(self.projectName)
        self.browser = self.startBrowser()
        self.dir = self._dir = self.source = ''
        self.ipnum = crawlerfun.ip2num('154.209.71.54')
        self.debug = True
        self.pageNum = self.getPageNum()


    def crawl(self):
        while True:
            file = './userList.json'
            with open(file, mode = 'r') as f:
                keywords = json.load(f)

            for key in keywords:  # 关键词循环
                for value in keywords[key]:  # 公众号循环
                    if value.get('state') == 0:
                        continue

                    try:
                        timeStamp = time.time()
                        timeArray = time.localtime(timeStamp)
                        self.date = time.strftime('%Y-%m-%d %H:%M:%S', timeArray)

                        self.doCrawl(key, value.get('nickname'))
                    except Exception as e:
                        print('crawl loop:', str(e)[:200])
                        self.browser = self.restart()
                        self.doCrawl(key, value.get('nickname'))
            try:
                self.browser = self.restart()
            except Exception as e:
                print('restart except:', e, '\n')
            finally:
                if os.path.exists('./none.txt'):  # 如果有none.txt文件，就更新userList.json 文件
                    w.updateJson()


    def doCrawl(self, key, nickname):
        self.i = 0
        try:
            url = 'https://weixin.sogou.com/weixin?type=1&query=' + nickname + '&ie=utf8&s_from=input&_sug_=y&_sug_type_='
            self.browser.get(url)
            sleeping = random.randint(5, 45)
            sleep(sleeping)

            if 'antispider' in self.browser.current_url:  # 检查是否被ban
                self.checkBanned()

            try:
                self.browser.find_element(by = By.CSS_SELECTOR, value = 'div.b404-box > div.text-info')  # 公众号没有文章
                self.recordNone(key, nickname)
                return
            except NoSuchElementException:
                pass

            print('\n' + key + ': ' + nickname)
        except (TimeoutException, WebDriverException) as e:
            print('key:', nickname, '--> open url exception:', str(e)[:200])
            sleep(10)
            self.browser = self.restart()
            return

        while True:
            newsList = self.browser.find_elements(by = By.CSS_SELECTOR, value = 'div.news-box > ul.news-list2 > li')
            for item in newsList:
                try:
                    dateTime = item.find_element(by = By.CSS_SELECTOR, value = 'dl:last-child > dd > span').text
                except NoSuchElementException:
                    continue

                if '前' in dateTime and '天前' not in dateTime:
                    self.extract(item, nickname)
                else:
                    continue

            if self.pageNum > 0:
                try:
                    self.browser.find_element(by = By.PARTIAL_LINK_TEXT, value = '下一页').click()
                except NoSuchElementException:
                    break
            elif self.pageNum == 0:
                break

        if self.i > 0:
            crawlerfun.renameNew()
            crawlerfun.expire(self.date, self.d, self.projectName)
            crawlerfun.deleteFiles(self.projectName)
            crawlerfun.recordTotal(self.projectName, self.i)


    # 提取信息，一条的
    def extract(self, item, nickname):
        titleInfo = item.find_element(by = By.CSS_SELECTOR, value = 'dd > a')
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
            return


    def bottomNews(self, browser, handle):
        self.browser.find_elements(by = By.XPATH, value = '/html/body').send_keys(Keys.END)
        current = int(time.time())
        newsList = browser.find_elements(by = By.CSS_SELECTOR, value = 'a.weui-media-box.weui-media-box_appmsg.js_related_item')
        for item in newsList:
            try:
                dateTime = int(item.get_attribute('data-time'))
            except:
                continue

            if current - dateTime < 86400:
                self.extractSingle(item, handle)
            else:
                continue


    def extractSingle(self, item, firstHandle):
        titleInfo = item.find_element(by = By.CSS_SELECTOR, value = 'div > div.weui_ellipsis_mod_inner')
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
                    self.browser.switch_to.window(newHandle)        # 切换到新标签
                    sleep(1)                                        # 等个几秒钟
                    self.source = self.getPageText()                # 拿到网页源码
                    link = self.browser.current_url                 # 获取当前网页的链接
                    self.browser.close()                            # 关闭当前标签页
                    sleep(1)
                    self.browser.switch_to.window(handle)  # 切换到之前的标签页
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
            html = self.browser.find_element(by = By.CSS_SELECTOR, value = 'div#js_content').get_attribute('innerHTML')
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
            print('count:', self.i, ' --- ', title, time)

        if '' == self._dir:
            self.crawl_mkdir()

        filename = self._dir + 'iask_' + str(i) + '_' + str(len(self.d)) + '.htm-2'
        for num in range(2):
            if 1 == crawlerfun.write_file(filename, page_text, ifdisplay = 0):
                savePath = '/root/estar_save/' + self.projectName + '/'
                if not os.path.exists(savePath):
                    os.makedirs(savePath)
                fileName = savePath + 'iask_' + str(i) + '_' + str(len(self.d)) + '.htm-2'
                crawlerfun.write_file(fileName, page_text, ifdisplay = 0)  # 再次保存到/root/estar_save目录下

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
            if 'antispider' in self.browser.current_url:
                if i > 0:
                    self.browser.find_element(by = By.CSS_SELECTOR, value = 'a#change-img').click()  # 点击换一张
                    sleep(2)

                # self.browser.execute_script('document.body.style.zoom="0.8"')
                verify = self.browser.find_element(by = By.CSS_SELECTOR, value = 'img#seccodeImage')
                verify.screenshot(imgFile)

                ocr = ddddocr.DdddOcr(show_ad = False)

                with open(imgFile, 'rb') as f:
                    byte = f.read()

                res = ocr.classification(byte)
                print('Verify code times:', i + 1, '. The Code: ' + res + '\n')
                os.remove(imgFile)

                self.browser.find_element(by = By.CSS_SELECTOR, value = 'input#seccodeInput').send_keys(res)  # 输入验证码
                sleep(2)
                self.browser.find_element(by = By.CSS_SELECTOR, value = 'p.p5 > a#submit').click()  # 点击‘提交’按钮
                sleep(5)
            else:
                break


    def recordNone(self, key, nickname):
        print('\n[' + key + '->' + nickname + ']', 'has no article!')

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

        if os.path.exists(oldFile):
            os.remove(oldFile)
        else:
            try:
                os.rename(newFile, oldFile)
            except Exception as e:
                print(e)

        with open(newFile, 'w') as fp:
            json.dump(obj, fp, indent = 2, ensure_ascii = False)

        if os.path.exists('./none.txt'):
            os.remove('./none.txt')


    def startBrowser(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-logging')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-javascript')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--disable-browser-side-navigation')
        options.add_argument('--ignore-certificate-errors-spki-list')
        options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.103 Safari/537.36"')

        browser = webdriver.Chrome(options = options)

        return browser


    def quit(self):
        for _ in range(3):
            try:
                self.browser.quit()
            except:
                continue


    def restart(self):
        print('----- restart browser -----\n')
        self.quit()
        sleep(2)
        browser = self.startBrowser()

        return browser




if __name__ == '__main__':
    w = MpWeixin()
    w.crawl()

    exit()

    # crawlWeixin()

    scheduler = BlockingScheduler()
    # scheduler.add_job(getUserList, 'cron', day = '*', hour = 4)         # 每天凌晨4点执行更新公众号程序
    scheduler.add_job(crawlWeixin, 'cron', day = '*', hour = 7)  # 每天7点开始采集公众号信息

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemError):
        scheduler.shutdown(wait = False)

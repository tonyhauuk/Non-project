import requests, random, re, execjs, time, hashlib, os, json, configparser
from http import cookiejar
from urllib import request, parse
from time import sleep
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MpWeixin:
    def __init__(self, d):
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        self.date = time.strftime('%Y-%m-%d %H:%M:%S', timeArray)
        self.d = d
        self.dir = self._dir = ''
        self.debug = True
        self.pageNum = self.getPageNum()



    def crawl(self):
        self.browser = webdriver.Firefox()
        self.browser.set_window_position(x = 630, y = 0)
        self.total = 0

        file = 'userList.json'
        with open(file, mode = 'r') as f:
            keywords = json.load(f)
            for key in keywords:    # 关键词循环
                for value in keywords[key]:   # 公众号循环
                    self.doCrawl(key, value['nickname'])

        self.browser.quit()


    def doCrawl(self, key, account):
        # print('key: ', key, '| account: ', account)
        print('\n' + key + ' ---> ' + account)
        self.i = 0
        try:
            sleep(1)
            url = 'https://weixin.sogou.com/weixin?type=1&query=' + account + '&ie=utf8&s_from=input&_sug_=y&_sug_type_='
            self.browser.get(url)
        except TimeoutException:
            return

        while True:
            newsList = self.browser.find_elements_by_css_selector('div.news-box > ul.news-list2 > li')
            for item in newsList:
                try:
                    dateTime = item.find_element_by_css_selector('dl:last-child > dd > span').text
                except NoSuchElementException:
                    continue

                if '前' in dateTime and '天前' not in dateTime:
                    self.extract(item, account)
                else:
                    continue

            if self.pageNum > 0:
                try:
                    self.browser.find_element_by_partial_link_text('下一页').click()
                except NoSuchElementException:
                    break
            elif self.pageNum == 0:
                break

        # if self.total > 0:
            # crawlerfun.renameNew()
            # crawlerfun.expire(self.date, self.d, self.projectName)


    # 提取信息，一条的
    def extract(self, item, account):
        titleInfo = item.find_element_by_css_selector('dd > a')
        title = titleInfo.text
        tag = title + '|' + account
        try:
            # href = titleInfo.get_attribute('href')
            md5 = self.makeMD5(tag)

            # dict filter
            if md5 in self.d:
                return
            else:
                self.d[md5] = self.date.split(' ')[0]  # 往dict里插入记录
                self.i += 1
                self.total += 1

            handle = self.browser.current_window_handle  # 拿到当前页面的handle
            titleInfo.click()
            link = ''
            # switch tab window
            WebDriverWait(self.browser, 10).until(EC.number_of_windows_to_be(2))
            handles = self.browser.window_handles
            for newHandle in handles:
                if newHandle != handle:
                    self.browser.switch_to.window(newHandle)  # 切换到新标签
                    sleep(2)  # 等个几秒钟
                    self.source = self.getPageText()  # 拿到网页源码
                    link = self.browser.current_url  # 获取当前网页的链接
                    self.bottomNews(self.browser, handle)  # 底部3条信息
                    self.browser.close()  # 关闭当前标签页
                    self.browser.switch_to.window(handle)  # 切换到之前的标签页
                    break
            print(title, link)
            # self.write_new_file(self.link, title, self.source, self.i, self.date, 1152937)
        except Exception as e:
            print('extract exception: ', e)
            print(self.date)
            return


    def bottomNews(self, browser, handle):
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
            WebDriverWait(self.browser, 10).until(EC.number_of_windows_to_be(3))
            handles = self.browser.window_handles
            for newHandle in handles:
                if newHandle != handle and newHandle != firstHandle:
                    self.browser.switch_to.window(newHandle)  # 切换到新标签
                    sleep(1)  # 等个几秒钟
                    self.source = self.getPageText()  # 拿到网页源码
                    self.singleLink = self.browser.current_url  # 获取当前网页的链接
                    self.browser.close()  # 关闭当前标签页
                    sleep(1)
                    self.browser.switch_to.window(handle)  # 切换到之前的标签页
                    break

            # self.write_new_file(self.singleLink, title, self.source, self.i, self.date, 1152937)
        except Exception as e:
            print('single error:', e)
            return


    def getPageText(self):  # 获取网页正文
        self.browser.find_element_by_xpath('/html/body').send_keys(Keys.END)
        try:
            html = self.browser.find_element_by_css_selector('div#js_content').get_attribute('innerHTML')
        except NoSuchElementException:
            html = self.browser.page_source

        return html


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
            fileName = '/home/zran/src/crawler/33/manzhua/crawlpy3/record/cq_md5.txt'
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
        filePath = '/root/estar_save/cq_gov/'
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


    def getPageNum(self):
        configFile = 'weixin.ini'
        conf = configparser.ConfigParser()
        conf.read(configFile)
        sections = conf.sections()
        option = conf.options(sections[1])

        pageNum = conf.get(sections[1], option[0])  # 采集模式：全采集，精确采集

        return int(pageNum)



if __name__ == '__main__':
    w = MpWeixin({})
    w.crawl()

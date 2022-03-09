# -*- coding: utf-8 -*-

import time, hashlib, os
from time import sleep
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Cls:
    def __init__(self, d):
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        self.date = time.strftime('%Y-%m-%d %H:%M:%S', timeArray)
        self.d = d
        self.dir = self._dir = self.source = ''
        self.debug = True

    def crawl(self):
        print('\n' ,'-' * 10, 'https://www.cls.cn/', '-' * 10, '\n')

        self.browser = webdriver.Firefox()
        self.browser.set_window_position(x = 630, y = 0)

        i = self.total = 0
        status = True
        file = 'cls_weblist.txt'
        with open(file, mode = 'r') as f:
            url = f.readlines()
            for x in url:
                n = self.doCrawl(x)
                if n == -1:
                    status = False
                    break
                else:
                    i += n

        print('quantity: ', self.total)
        if status:
            if i > 0:
                # self.deleteFiles()
                return 'complete', self.source, 'ok'
            else:
                return 'complete', 'none', 'ok'
        else:
            return 'interrupt', 'none', 'error'


    def doCrawl(self, url):
        self.i = 0
        self.url = url
        try:
            self.browser.get(url)
        except TimeoutException:
            return -1


        if 'telegraph' in url:
            newsList = self.browser.find_elements_by_css_selector('div.f-l.content-left > div > div.telegraph-list')
            for item in newsList:
                self.extract(item)
        else:
            newsCss = dateCss = ''

            if 'subject' in url:
                newsCss = 'div > div.b-c-e6e7ea.telegraph-list'
                dateCss = 'div > span.f-s-12.c-999'
            elif 'depth' in url:
                newsCss = 'div > div.subject-interest-list'
                dateCss = 'span.m-r-5'


            newsList = self.browser.find_elements_by_css_selector(newsCss)
            for item in newsList:
                dateTime = item.find_element_by_css_selector(dateCss).text
                self.dateTime = dateTime

                self.extract(item)

                if 'depth' not in url:
                    if dateTime.split(' ')[0] in self.date:
                        self.extract(item)
                    else:
                        break
                else:
                    if '前' in dateTime:
                        self.extract(item)
                    else:
                        break



        if self.i > 0:
            # self.rename()
            # self.expire()

            return self.i
        else:
            return 0


    # 提取信息，一条的
    def extract(self, item):
        if 'telegraph' in self.url:
            try:
                title = item.find_element_by_xpath('div/div[1]/span[2]').text
            except NoSuchElementException:
                return

            md5 = self.makeMD5(title)
            # dict filter
            if md5 in self.d:
                return
            else:
                self.d[md5] = self.date.split(' ')[0]  # 往dict里插入记录
                self.i += 1
                self.total += 1

            href = 'https://www.cls.cn/telegraph'
            self.source = title
            print(href, title, '\n')

            #self.write_new_file(href, title, self.source, self.i, self.date, 1167649)
        else:
            titleInfo = None
            if 'subject' in self.url:
                if '财联社' in self.dateTime:
                    titleInfo = item.find_element_by_css_selector('div.subject-interest-image-content-box > div.clearfix > a')
                else:
                    titleInfo = item.find_element_by_css_selector('div.clearfix > div > a')
            elif 'depth' in self.url:
                titleInfo = item.find_element_by_css_selector('div.clearfix.subject-interest-title > a')


            try:
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

                if 'subject' in self.url:
                    if '财联社' in self.dateTime:
                        handle = self.browser.current_window_handle  # 拿到当前页面的handle
                        titleInfo.click()

                        # switch tab window
                        WebDriverWait(self.browser, 10).until(EC.number_of_windows_to_be(2))
                        handles = self.browser.window_handles
                        for newHandle in handles:
                            if newHandle != handle:
                                self.browser.switch_to.window(newHandle)    # 切换到新标签
                                sleep(2)                                    # 等个几秒钟
                                self.source = self.getPageText()            # 拿到网页源码
                                self.browser.close()                        # 关闭当前标签页
                                self.browser.switch_to.window(handle)       # 切换到之前的标签页
                                break

                        print(href, title, '\n')
                        # self.write_new_file(href, title, self.source, self.i, self.date, 1167649)
                    else:
                        print(href, title, '\n')
                        self.source = titleInfo.find_element_by_css_selector('span').text
                        # self.write_new_file(href, title, self.source, self.i, self.date, 1167649)
                else:
                    handle = self.browser.current_window_handle  # 拿到当前页面的handle
                    titleInfo.click()

                    # switch tab window
                    WebDriverWait(self.browser, 10).until(EC.number_of_windows_to_be(2))
                    handles = self.browser.window_handles
                    for newHandle in handles:
                        if newHandle != handle:
                            self.browser.switch_to.window(newHandle)  # 切换到新标签
                            sleep(2)  # 等个几秒钟
                            self.source = self.getPageText()  # 拿到网页源码
                            self.browser.close()  # 关闭当前标签页
                            self.browser.switch_to.window(handle)  # 切换到之前的标签页
                            break

                    print('link:',href, 'title:',title, '\n')
                    # self.write_new_file(href, title, self.source, self.i, self.date, 1167649)

            except (NoSuchElementException, NoSuchAttributeException) as e:
                print('Element error:', e)
            except Exception:
                return


    def getPageText(self):  # 获取网页正文
        try:
            html = self.browser.find_element_by_css_selector('div.bd > div.content').get_attribute('innerHTML')
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
            fileName = '/home/zran/src/crawler/31/manzhua/crawlpy3/record/sc_md5.txt'
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
        filePath = '/root/estar_save/sc_gov/'
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
    sc = Cls({})
    sc.crawl()

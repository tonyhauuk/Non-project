# -*- coding: utf-8 -*-
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException, NoSuchWindowException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time, json
import sys
import os
import hashlib
from os.path import join, getsize
import shutil
from datetime import datetime, date, timedelta
import datetime
# import crawlerfun
# from crawlerfun import DriverElement
# import crawlerfun
import threading



class Qie:
    def __init__(self, browser):
        self.browser = browser
        self.d = {}
        self.debug = True


    def crawl(self, url):
        self.i = 0
        page = 0

        keyword = self.url.split('word=')[1]
        self.url = 'https://www.toutiao.com/search/?keyword=' + keyword

        try:
            self.browser.get(url)
        except:
            return 'interrupt', 'none', 'error'

        try:
            if '没有找到与' in self.browser.page_source:
                return 'complete', 'none', 'ok'
        except:
                return 'interrupt', 'none', 'error'




        for i in range(5):
            try:
                sections = self.browser.find_elements_by_css_selector('html body div.wrap div.wrapper div.main div.results div.vrwrap')
                for section in sections:
                    ptime = section.find_element_by_css_selector('p.news-from').text
                    link = section.find_element_by_css_selector('div h3 a').get_attribute('href')

                    if 'new.qq.com/rain' in link or 'new.qq.com/omn' in link:
                        self.extract(section, link)

                    # if '小时前' in ptime or '分钟前' in ptime:
                    #     if 'new.qq.com/rain' in link or 'new.qq.com/omn' in link:
                    #         self.extract(section, link)
                    # else:
                    #     if 'new.qq.com/rain' in link or 'new.qq.com/omn' in link:
                    #         self.extract(section, link)
            except (NoSuchAttributeException, NoSuchElementException) as e:
                pass

            try:
                if self.i == 0:
                    break

                self.browser.find_element_by_partial_link_text('下一页').click()
                if self.debug:
                    print('翻页...... page: ', page + 2)
                    page += 1
            except NoSuchElementException as e:
                break

            self.i = 0

        return 'complete', self.source, 'ok'


    def extract(self, item, link):
        try:
            interval = 2
            current = int(time.time())
            content = item.find_element_by_css_selector('div h3.vrTitle a')
            md5 = self.makeMD5(link)

            # dict filter
            if md5 in self.d:
                return
            else:
                self.d[md5] = str(current)  # 往dict里插入记录
                self.i += 1
                self.total += 1

            title = content.text
            handle = self.browser.current_window_handle
            content.click()

            # switch tab window
            handles = self.browser.window_handles
            for newHandle in handles:
                if newHandle != handle:
                    self.browser.switch_to.window(newHandle)
                    time.sleep(interval)
                    self.source = self.browser.page_source
                    self.browser.close()
                    self.browser.switch_to.window(handles[0])

            # self.writeFile(objStr, current, self.i)
            # self.write_new_file(href, title, self.source, self.i)
        except (NoSuchElementException, NoSuchAttributeException) as e:
            print('Element error:', e)
        except Exception:
            pass

    # 生成md5
    def makeMD5(self, link):
        m = hashlib.md5()
        b = link.encode(encoding='utf-8')
        m.update(b)
        link = m.hexdigest()

        return link

    def initDict(self):
        file = './qie.txt'
        try:
            with open(file, mode='r') as f:
                line = f.readline()
                if line != '' or line != '{}':
                    self.d = eval(str(line))  # 直接把字符串转成字典格式
        except:
            # 如果没有文件，则直接创建文件
            fd = open(file, mode='a+', encoding='utf-8')
            fd.close()

    def quit(self):
        self.browser.quit()


if __name__ == '__main__':

    opts = webdriver.FirefoxOptions()
    browser = webdriver.Firefox()

    process = Qie(browser)
    try:
        keyword = ['微软', '金融', 'nvidia']
        url = 'https://news.sogou.com/news?query=site%3Aqq.com+'+ keyword[2]+ '&_ast=1578557952&_asf=' \
              'news.sogou.com&time=0&w=01029901&sort=1&mode=1&manual=true&dp=1&sut=88204&sst0=1578558105750&lkt=0%2C0%2C0'
        obj = process.crawl(url)
    except TimeoutException:
        print('The connection has timed out!')
    finally:
        browser.quit()

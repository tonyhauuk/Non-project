# -*- coding: utf-8 -*-
import time, datetime, re, hashlib, os, sys, urllib.parse, random
from datetime import datetime, date, timedelta
from time import sleep
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException, WebDriverException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import crawlerfun

from crawlerfun import ClearCache
import time, os, datetime, subprocess
from selenium import webdriver
from selenium.webdriver.opera.options import Options as operaOptions

class Douyin:
    def __init__(self, browser):
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        self.date = time.strftime('%Y-%m-%d %H:%M:%S', timeArray)
        self.projectName = 'douyin'
        self.d = crawlerfun.initDict(self.projectName)
        self.url = browser.url
        self.browser = browser.driver
        self.dir = self._dir = self.source = ''
        self.ipnum = crawlerfun.ip2num(browser.ip)
        self.debug = True


    def crawl(self):
        # print('\n', '-' * 10, 'https://www.douyin.com/', '-' * 10, '\n')
        self.i = 0
        feed = 'boxgrid'    # list    boxgrid
        self.titleInfo = self.title = ''

        keyword = self.url.split('/weibo/')[1].split('&scope=')[0]
        url = 'https://www.douyin.com/search/' + keyword + '?publish_time=1&sort_type=0&source=tab_search&type=general'
        try:
            self.browser.get(url)
            sleeping = random.randint(5, 10)
            print('sleep ' + str(sleeping) + 's...\n')
            sleep(sleeping)
        except TimeoutException:
            print('page timed-out!')
            return 'complete', '', 'ok'

        try:
            error = self.browser.find_element(by = By.CSS_SELECTOR, value = 'div.P6wJrwQ6').text
            print('Error content:', error)
            # if error == '服务出现异常' or error == '无搜索内容':
            #     return 'interrupt', '', 'no'
            return 'interrupt', '', 'no'
        except NoSuchElementException:
            pass

        try:
            self.browser.find_elements(by = By.CSS_SELECTOR, value = 'ul.qrvPn3bC.KPpARyeA > li.aCTzxbOJ.mZ4vbHBN.foy_xdJY')
        except:
            try:
                login = self.browser.find_element(by = By.CSS_SELECTOR, value = 'div.NmJ3uOde > div.Q1mRRzo8').text
                print('Mutiple login error:', login)

                return 'interrupt', '', 'no'
            except:
                pass

        # try:
        #     login = self.browser.find_element(by = By.CSS_SELECTOR, value = 'div.NmJ3uOde > div.Q1mRRzo8').text
        #     print('Mutiple login error:', login)
        #     try:
        #         self.browser.find_elements(by = By.CSS_SELECTOR, value = 'ul.qrvPn3bC.KPpARyeA > li.aCTzxbOJ.mZ4vbHBN.foy_xdJY')
        #     except:
        #         pass
        #     else:
        #         return 'interrupt', '', 'no'
        # except NoSuchElementException:
        #     pass

        if feed == 'boxgrid':
            self.titleInfo = 'div > div > a'
            self.title = 'div.swoZuiEM'
            try:
                boxgrid = self.browser.find_element(by = By.CSS_SELECTOR, value = 'div.RGlTqsxm.P3KnuaJb.cJjQzCs7 > svg')
                boxgrid.click()
                sleep(5)
            except Exception as e:
                pass
                # print('Can not found 9 box-grid icon!\n')
        elif feed == 'list':
            self.titleInfo = 'div.display-none > a'
            self.title = 'div.KxCuain0.QekCqA8W span span.Nu66P_ba'

        try:
            self.browser.find_element(by = By.ID, value = 'login-pannel')
            sleep(2)
            print('[login page]')
            self.browser.find_element(by = By.CSS_SELECTOR, value = 'div.dy-account-close').click()
        except NoSuchElementException:
            pass

        try:
            slide = self.browser.find_element(by = By.CSS_SELECTOR, value = 'div.captcha_verify_container.style__CaptchaWrapper-sc-1gpeoge-0.zGYIR')
            print('[slide page]')
            sleep(2)
            self.slideCheck(slide)
            # self.browser.refresh()
            # print('refresh page')
            # return 'complete', 'none', 'ok'
        except:
            newsList = self.browser.find_elements(by = By.CSS_SELECTOR, value = 'div.IFYTLgyk.xAmWmd67:nth-child(1) > ul.qrvPn3bC > li')
            # print('video list length: ', len(newsList))
            for item in newsList:
                self.extract(item)

        print('quantity:', self.i, '\n')
        if self.i > 0:
            crawlerfun.renameNew()
            crawlerfun.expire(self.date, self.d, self.projectName)

            return 'complete', self.source, 'ok'
        else:
            return 'complete', 'none', 'ok'



    # 提取信息，一条的
    def extract(self, item):
        try:
            titleInfo = item.find_element(by = By.CSS_SELECTOR, value = self.titleInfo)
            href = titleInfo.get_attribute('href')
            md5 = crawlerfun.makeMD5(href)

            # dict filter
            if md5 in self.d:
                return
            else:
                self.d[md5] = self.date.split(' ')[0]  # 往dict里插入记录
                self.i += 1

            # title = content = item.find_element(by = By.CSS_SELECTOR, value = 'div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > span:nth-child(2) > span:nth-child(1) > span:nth-child(1) > span:nth-child(1) > span:nth-child(1) > span:nth-child(1)').text
            title = self.source = item.find_element(by = By.CSS_SELECTOR, value = self.title).text

            # print(href, title, '\ncontent:' + content)
            self.write_new_file(href, title, self.source, self.i, self.date, 1172664)
        except NoSuchElementException as ex:
            # print('element error:', ex)
            pass
        except Exception as e:
            print('dy exception:', e)
            # pass


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
            print('count:', i, ' --- ', title)

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


    def slideCheck(self, block):
        # close = block.find_element(by = By.CSS_SELECTOR, value = '')
        feedback = block.find_element(by = By.CSS_SELECTOR, value = 'span.secsdk_captcha_feedback--text.sc-bxivhb.gDEuBz')
        feedback.click()
        sleep(5)
        text = ['加载失败', '重复弹框', '样式错位','其他']
        randomPickup = text[random.random(0, len(text) - 1)]
        self.browser.find_element(by = By.PARTIAL_LINK_TEXT, value = randomPickup).click()
        sleep(2)
        self.browser.find_element(by = By.PARTIAL_LINK_TEXT, value = '提交').click()
        sleep(2)

# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException, StaleElementReferenceException, WebDriverException
from urllib.parse import unquote
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re, json, uuid, time, datetime, sys


class Zhihu:
    def __init__(self, browser, timestamp):
        self.browser = browser
        self.timestamp = timestamp

    def main(self, url):
        try:
            self.browser.get(url)
        except:
            return dict(errno = 2, error = 'Page can not open')
        else:
            try:
                cardList = self.browser.find_element_by_css_selector('html>body>div:nth-of-type(1)>div>main>div>div:nth-of-type(2)>div:nth-of-type(2)>div:nth-of-type(2)')
                data = self.doParse(cardList)

                return data
            except NoSuchElementException:
                self.doLogin(url)

    def doParse(self, cardList):
        data = dict()
        i = 1
        try:
            allClick = cardList.find_elements_by_css_selector('div.RichContent>div.RichContent-inner>button')
            for more in allClick:
                self.browser.execute_script("arguments[0].click();", more)

            items = cardList.find_elements_by_css_selector('div.List-item')
            for item in items:
                info = self.blockParse(item)
                data[i] = info
                i += 1

            return data
        except NoSuchElementException:
            return dict(errno = 2, error = 'No results!')

    def blockParse(self, item):
        try:
            urlTag = item.find_element_by_css_selector('div.ContentItem>h2.ContentItem-title a')
            url = urlTag.get_attribute('href')
            title = urlTag.find_element_by_css_selector('span.Highlight').text
            richContent = item.find_element_by_css_selector('div.RichContent')
            authorInfo = richContent.find_element_by_css_selector('div.SearchItem-authorInfo>div.AuthorInfo')
            userName = authorInfo.find_element_by_css_selector('div.AuthorInfo-head').text
            richElement = richContent.find_element_by_css_selector('div.RichContent-inner>span.RichText').get_attribute('innerHTML')
            text = self.filterHTML(richElement)
            publishStr = richContent.find_element_by_css_selector('div.ContentItem-time>a>span').get_attribute('data-tooltip')
            publishTime = self.getPublishTime(publishStr)
            actions = richContent.find_element_by_css_selector('div.ContentItem-actions')
            likes = actions.find_element_by_css_selector('span>button.VoteButton--up').text
            like = self.getLikeNumber(likes)

            data = dict(title = title, url = url, userName = userName, text = text, time = publishTime, like = like)

            return data
        except (NoSuchElementException):
            pass

    def doLogin(self, url):
        user = '13261593150'
        password = '800915'
        self.main(url)

    @staticmethod
    def filterHTML(str):
        reg1 = '<[^<img>].*?>'
        reg2 = '<[^img>]+>'
        p = re.compile(reg1)
        r1 = p.sub('', str)
        r1 = r1.replace('<figure>', '')
        r1 = r1.replace('</figure>', '')
        r1 = r1.replace('<noscript>', '')
        r1 = r1.replace('</noscript>', '')
        p = re.compile(r'''(<img\b[^<>]*?\bsrc[\s\t\r\n]*=[\s\t\r\n]*["']?[\s\t\r\n]*([^\s\t\r\n"'<>]*)[^<>]*?/?[\s\t\r\n]*>)''', re.IGNORECASE)
        r2 = p.sub(r'''<img src="\2">''', r1)

        return r2

    @staticmethod
    def getPublishTime(str):
        s = ''
        for i in str:
            if i >= u'\u4e00' and i <= u'\u9fa5':
                s += i
        t = str.replace(s, '')
        t = t.strip()

        return t

    @staticmethod
    def getLikeNumber(likes):
        array = likes.split('赞同')
        num = array[1].strip()
        if num == '':
            num = '0'

        return num

    def closed(self):
        self.browser.close()

    def quit(self):
        self.browser.quit()


if __name__ == '__main__':
    try:
        keyword = sys.argv[1]
    except IndexError:
        obj = dict(errno = 4, error = 'Argument is missing')
        jsonObj = json.dumps(obj, ensure_ascii = False, indent = 4, separators = (',', ': '))
        print(jsonObj)
    else:
        opts = webdriver.FirefoxOptions()
        opts.add_argument('--headless')  # Headless browser
        opts.add_argument('--disable-gpu')  # Disable gpu acceleration
        profile = webdriver.FirefoxProfile()
        # profile.set_preference('browser.privatebrowsing.autostart', True)  # Start a private browsing
        browser = webdriver.Firefox(firefox_profile = profile, firefox_options = opts)

        timestamp = int(time.time())
        process = Zhihu(browser, timestamp)
        try:
            s = time.time()
            url = 'https://www.zhihu.com/search?type=content&q=' + keyword
            obj = process.main(url)
            jsonObj = json.dumps(obj, ensure_ascii = False, indent = 4, separators = (',', ': '))
            print(jsonObj)
            print(str(time.time() - s) + " 's time used")
        except (TimeoutException,):
            obj = dict(errno = 6, error = 'The connection has timed out!')
            jsonObj = json.dumps(obj, ensure_ascii = False, indent = 4, separators = (',', ': '))
            print(jsonObj)
        finally:
            process.quit()

'''
xpath locate to 'div.Card div.List'
/html/body/div[1]/div/main/div/div[2]/div[2]/div[2]

'''

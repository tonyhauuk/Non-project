# -*- coding: utf-8 -*-
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException, WebDriverException, StaleElementReferenceException, \
    NoSuchWindowException
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re, json, time, sys, math
import multiprocessing as mp


class Zhihu:
    def __init__(self, browser, timestamp, amount = 10, mode = 'day'):
        self.browser = browser
        self.timestamp = timestamp
        self.amount = amount
        self.cardList = None
        self.loopNum = self.calcLoop(amount)
        self.mode = mode  # normal, day, week, month

    def main(self, url):
        try:
            self.browser.get(url)
            if self.mode == 'day':
                self.oneDay()
        except NoSuchWindowException:
            return dict(errno = 2, error = 'Page can not open')
        else:
            css = ''
            if self.amount > 10:
                for k in range(self.loopNum):
                    try:
                        # WebDriverWait(self.browser, 1).until(lambda x: x.find_element_by_xpath('/html/body')).send_keys(Keys.END)
                        WebDriverWait(self.browser, 1).until(EC.presence_of_element_located((By.XPATH, '/html/body'))).send_keys(Keys.END)
                        time.sleep(1)
                    except (NoSuchElementException, WebDriverException):
                        continue
            else:
                WebDriverWait(self.browser, 1).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/main/div/div[2]/div[2]/div/div/div/div[11]')))

            if self.mode == 'day':
                css = 'div>div.Search-container>div#SearchMain.SearchMain>div.Card>div.List>div'
            elif self.mode == 'normal':
                css = 'html>body>div:nth-of-type(1)>div>main>div>div:nth-of-type(2)>div:nth-of-type(2)>div:nth-of-type(2)'

            try:
                cardList = self.browser.find_element_by_css_selector(css)
                data = self.doParse(cardList)
                jsonObj = json.dumps(data, ensure_ascii = False, indent = 4, separators = (',', ': '))

                return jsonObj
            except NoSuchElementException:
                return dict(errno = 7, error = 'Web page error')

    def doParse(self, cardList):
        data = dict()
        i = 1
        j = 0
        try:
            allClick = cardList.find_elements_by_css_selector('div.RichContent>div.RichContent-inner>button')
            for more in allClick:
                self.browser.execute_script("arguments[0].click();", more)
                j += 1
                if self.amount == j:
                    break

            items = cardList.find_elements_by_css_selector('div.List-item')

            for item in items:
                try:
                    info = self.blockParse(item)
                    data[i] = info
                except NoSuchElementException:
                    break
                i += 1
                if self.amount < i:
                    break

            if len(data) == 0:
                data = dict(errno = 1, error = 'No results!')

            return data
        except NoSuchElementException as e:
            return dict(errno = 3, error = str(e))

    def blockParse(self, item):
        # pool = mp.Pool(4)
        try:
            urlTag = item.find_element_by_css_selector('div.AnswerItem>h2.ContentItem-title>div>a')
        except NoSuchElementException:
            urlTag = item.find_element_by_css_selector('div.ArticleItem>h2.ContentItem-title>a')

        try:
            url = urlTag.get_attribute('href').split('/answer')[0]
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
            # jobs = [pool.apply_async(self.getComments, args = (url,)) for url in url]
            # comments = [j.get() for j in jobs]
            # print(comments)
            # exit()

            data = dict(title = title, url = url, userName = userName, text = text[0:100], time = publishTime, like = like)

            return data
        except (NoSuchElementException, NoSuchAttributeException) as e:
            print('Block error: ' + str(e))

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

    # Click one day selection
    def oneDay(self):
        try:
            self.browser.find_element_by_xpath('/html/body/div[1]/div/main/div/div[1]/div/div/div/button').click()
            self.browser.find_element_by_xpath('/html/body/div[4]/div/span/div/div/button[2]').click()
        except NoSuchElementException as e:
            print(e)

    def calcLoop(self, amount):
        remain = amount % 10
        division = amount / 10

        if remain == 0:
            num = division - 1
            num = math.ceil(num)
        else:
            num = amount / 10
            num = math.ceil(num)

        return int(num)

    def getComments(self, url):
        return self.browser.get(url)


    def closed(self):
        self.browser.close()

    def quit(self):
        self.browser.quit()


if __name__ == '__main__':
    try:
        keyword = sys.argv[1]
        mode = sys.argv[2]
    except IndexError:
        obj = dict(errno = 4, error = 'Argument is missing')
        jsonObj = json.dumps(obj, ensure_ascii = False, indent = 4, separators = (',', ': '))
        print(jsonObj)
    else:
        opts = webdriver.FirefoxOptions()
        # opts.add_argument('--headless')     # Headless browser
        # opts.add_argument('--disable-gpu')  # Disable gpu acceleration
        profile = webdriver.FirefoxProfile()
        profile.set_preference('browser.privatebrowsing.autostart', True)  # Start a private browsing
        browser = webdriver.Firefox(firefox_profile = profile, options = opts)

        timestamp = int(time.time())
        process = Zhihu(browser, timestamp, mode)
        try:
            url = 'https://www.zhihu.com/search?type=content&type=content&q=' + keyword
            obj = process.main(url)
            print(obj)
        except TimeoutException:
            obj = dict(errno = 6, error = 'The connection has timed out!')
            jsonObj = json.dumps(obj, ensure_ascii = False, indent = 4, separators = (',', ': '))
            print(jsonObj)
        finally:
            process.quit()

'''

xpath locate to 'div.Card div.List'
/html/body/div[1]/div/main/div/div[2]/div[2]/div[2]

'''

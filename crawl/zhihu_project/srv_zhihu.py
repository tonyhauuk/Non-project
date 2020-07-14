# -*- coding: utf-8 -*-
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException, WebDriverException, StaleElementReferenceException, \
    NoSuchWindowException
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re, json, time, sys, math
import urllib.parse
import xmltodict
import dicttoxml
import xml.dom.minidom as Dom
import crawlerfun
from crawlerfun import DriverElement, MANZHUADATABASE


class Zhihu:
    url = ''
    tasktype = ''
    driver = ''
    returnDataType = ''
    index = 0
    browser = ''
    instance = ''

    def __init__(self, browser, sendType = 'xml', amount = 10, mode = 'day'):
        self.sendType = sendType
        self.amount = amount
        self.loopNum = self.calcLoop(amount)
        self.mode = mode  # normal, day, week, month
        self.keyword = ''
        self.isChinese = False

        # Class 参数
        self.url = browser.url
        self.tasktype = browser.tasktype
        self.browser = browser.driver
        self.returnDataType = browser.returnDataType
        self.index = browser.index
        self.instance = DriverElement()
        self.db = MANZHUADATABASE()

        # XML的变量
        if sendType == 'xml':
            self.doc = Dom.Document()
            self.rootNode = self.doc.createElement("article")
            self.doc.appendChild(self.rootNode)

    def crawl(self):
        limit = 'ok'
        obj = None
        # self.url = 'https://www.zhihu.com/search?range=1d&q=intel&type=content'  # + self.getKeyWord()

        try:
            if 'error' == self.instance.element_open_link(self.browser, self.url, self.index, sleeptime = 0):
                limit = 'error'

            # if self.mode == 'day':
            #     self.oneDay()
        except NoSuchWindowException:
            print(dict(errno = 2, error = 'Page can not open'))
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
                WebDriverWait(self.browser, 1).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/main/div/div[2]/div[2]/div/div/div')))

            # 目前不手动选择时间的话，没有用
            if self.mode == 'day':
                # css = 'div>div.Search-container>div#SearchMain.SearchMain>div.Card>div.List>div'
                css = 'div#SearchMain>div>div.ListShortcut>div.List>div'
            elif self.mode == 'normal':
                css = 'html>body>div:nth-of-type(1)>div>main>div>div:nth-of-type(2)>div:nth-of-type(2)>div:nth-of-type(2)'

            # 判断关键词是否是中文
            self.isChinese = self.isChn()

            # 获取整个list的信息
            cardList = self.browser.find_element_by_css_selector(css)

            # 解析大块的信息
            data, complete = self.doParse(cardList)

            if self.sendType == 'json':
                obj = json.dumps(data, ensure_ascii = False, indent = 4, separators = (',', ': '))
            elif self.sendType == 'xml':
                obj = self.doc.toprettyxml()
                print(obj)

            return complete, obj, limit

    def doParse(self, cardList):
        completed = 'interrupt'
        data = {}
        i = 1
        j, feq, k = 0, 0, 0
        self.keyword = self.getKeyWord() # 拿到关键词，等会去文中匹配

        try:
            allClick = cardList.find_elements_by_css_selector('div.RichContent>div.RichContent-inner>button')
            for more in allClick:
                self.browser.execute_script("arguments[0].click();", more)
                j += 1
                if self.amount < j:
                    break

            items = cardList.find_elements_by_css_selector('div.List-item')
            for item in items:
                if self.amount == feq:
                    break

                info = self.blockParse(item)
                feq += 1

                if 'error' in info or info == 'none':
                    continue
                else:
                    k += 1

                if self.sendType == 'xml':
                    self.dictToXml(info)
                else:
                    data[i] = info
                    i += 1

            if len(data) == 0 and self.sendType == 'json':
                data = dict(errno = 1, error = 'No results!')

            if len(data) > 0 and self.sendType == 'json':
                completed = 'complete'
            elif k > 0 and self.sendType == 'xml':
                completed = 'complete'

            return data, completed
        except NoSuchElementException as e:
            return dict(errno = 3, error = str(e))

    def blockParse(self, item):
        try:
            urlTag = item.find_element_by_css_selector('div.ContentItem.AnswerItem>h2.ContentItem-title>div>a')
        except NoSuchElementException:
            urlTag = item.find_element_by_css_selector('div.ContentItem.ArticleItem>h2.ContentItem-title>a')

        url = urlTag.get_attribute('href').split('/answer')[0]
        title = urlTag.find_element_by_css_selector('span.Highlight').text

        try:
            richContent = item.find_element_by_css_selector('div.ContentItem.AnswerItem>div.RichContent')
        except NoSuchElementException:
            richContent = item.find_element_by_css_selector('div.ContentItem.ArticleItem>div.RichContent')

        try:
            userName = richContent.find_element_by_css_selector('div.SearchItem-meta.SearchItem-authorInfo>div.AuthorInfo').text
        except NoSuchElementException:
            userName = richContent.find_element_by_css_selector('div.AuthorInfo-content').text

        try:
            # userName = authorInfo.find_element_by_css_selector('div.Popover>div>a').text
            richElement = richContent.find_element_by_css_selector('div.RichContent-inner>span.RichText').get_attribute('innerHTML')
            text = self.filterHTML(richElement)
            publishStr = richContent.find_element_by_css_selector('div.ContentItem-time>a>span').get_attribute('data-tooltip')
            publishTime = self.getPublishTime(publishStr)
            actions = richContent.find_element_by_css_selector('div.ContentItem-actions')
            likes = actions.find_element_by_css_selector('span>button.VoteButton--up').text
            like = self.getLikeNumber(likes)

            # 先检查数据库中是否有当前连接的记录值，如果有这个block就不要
            if self.sendType == 'xml':
                query, current_title, md5_title = self.instance.url_search_db(url, self.db, 0)
                if 'error' == query or 1 == query:
                    return 'none'

            # 判断是否是中文，如果是中文检查标题和正文当中是否有关键词，都没有的话这个block information不要
            if self.isChinese:
                if self.keyword not in title and self.keyword not in text:
                    return 'none'

            data = dict(title = title, url = url, userName = userName, text = text, time = publishTime, like = like)

            return data
        except (NoSuchElementException, NoSuchAttributeException) as e:
            print('Block error: ' + str(e))
            return 'block error'

    def filterHTML(self, str):
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
        content = r2.replace('<img src=\"data:image/svg+xml;utf8,\">', '')
        content = content.replace('<img src="data:image/svg+xml;utf8,&lt;svg">', '')

        return content

    def getPublishTime(self, str):
        s = ''
        for i in str:
            if i >= u'\u4e00' and i <= u'\u9fa5':
                s += i
        t = str.replace(s, '')
        t = t.strip()

        return t

    def getLikeNumber(self, likes):
        array = likes.split('赞同')
        num = array[1].strip()
        if num == '':
            num = '0'

        return num

    # Click one day selection
    def oneDay(self):
        try:
            # self.browser.find_element_by_xpath('/html/body/div[1]/div/main/div/div[1]/div/div/div/button').click()
            # self.browser.find_element_by_xpath('/html/body/div[4]/div/span/div/div/button[2]').click()
            self.browser.find_element_by_xpath('/html/body/div[1]/div/main/div/div[1]/div/div/div/button/span').click()
            self.browser.find_element_by_xpath('//*[@id="Select3-1"]').click()
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

    def getKeyWord(self):
        import re
        kw = re.findall(r'q=(.+?)&', self.url)
        kwStr = urllib.parse.unquote(kw[0])

        return kwStr

    def isChn(self):
        keyword = self.getKeyWord()
        for ch in keyword:
            if '\u4e00' <= ch <= '\u9fff':
                return True

        return False

    def dictToXml(self, data):
        content = self.doc.createElement("content")

        titleNode = self.doc.createElement('title')
        titleValue = self.doc.createTextNode(data['title'])
        titleNode.appendChild(titleValue)
        content.appendChild(titleNode)

        urlNode = self.doc.createElement('url')
        urlValue = self.doc.createTextNode(data['url'])
        urlNode.appendChild(urlValue)
        content.appendChild(urlNode)

        userNameNode = self.doc.createElement('userName')
        userNameValue = self.doc.createTextNode(data['userName'])
        userNameNode.appendChild(userNameValue)
        content.appendChild(userNameNode)

        textNode = self.doc.createElement('text')
        textValue = self.doc.createTextNode(data['text'])
        textNode.appendChild(textValue)
        content.appendChild(textNode)

        timeNode = self.doc.createElement('time')
        timeValue = self.doc.createTextNode(data['time'])
        timeNode.appendChild(timeValue)
        content.appendChild(timeNode)

        likeNode = self.doc.createElement('like')
        likeValue = self.doc.createTextNode(data['like'])
        likeNode.appendChild(likeValue)
        content.appendChild(likeNode)

        self.rootNode.appendChild(content)

    def closed(self):
        self.browser.close()

    def quit(self):
        self.browser.quit()

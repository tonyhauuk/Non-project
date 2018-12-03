# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException, StaleElementReferenceException, WebDriverException
from urllib.parse import unquote
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re, json, uuid, time, datetime, sys



class Weibo:
    def __init__(self, browser, timestamp):
        self.browser = browser
        self.namespace = uuid.NAMESPACE_URL
        self.status = False
        self.timestamp = timestamp
        self.date = ''

    # Return latest weibo in 24 hours
    def parseHTML(self, link):
        allInfo, info  = dict(), dict()
        j = 1
        try:
            self.browser.get(link)
        except:
             return dict(errno = 2, error = 'Web can not open!')
        else:
            error = self.checkResult()
            if error == 'success':
                while True:
                    try:
                        # Scroll to the bottom
                        self.browser.find_element_by_xpath('/html/body').send_keys(Keys.END)
                        feedList = self.browser.find_element_by_css_selector('div.m-wrap>div#pl_feedlist_index')
                    except NoSuchElementException:
                        return dict(errno = 4, error = 'Page No results!')

                    try:
                        blocks = feedList.find_elements_by_css_selector('div>div.card-wrap')
                    except NoSuchElementException:
                        return dict(errno = 3, error = 'Page can not open')

                    i = 1
                    for block in blocks:
                        try:
                            mid = block.get_attribute('mid')
                            if not mid:
                                continue
                        except NoSuchAttributeException:
                            continue
                        else:
                            data = self.blockParse(block)
                            if self.status:
                                info[i] = data
                                i += 1

                    if len(info) == 0 and j == 1:
                        allInfo = dict(errno = 2, error = 'No results!')
                        break
                    elif len(info) == 0:
                        break
                    else:
                        allInfo[j] = info

                    try:
                        self.browser.find_element_by_css_selector('a.next').click()
                    except NoSuchElementException:
                        break
                    j += 1
                    info = {}
            else:
                allInfo = dict(errno = 1, error = error)

        return allInfo

    # Parse one of block information
    def blockParse(self, block):
        polymerization = None
        imgUrls, contentLink = list(), list()
        forwardNumber = commentsNumber = like = num= 0
        nickname = verify = avatar = video = uid = userID = date = content = deviceID = contentUrl = ''

        # If out of 24 hours, then skip blow if code
        # 1: 判断时间
        try:
            polymerization = block.find_elements_by_css_selector('div.content>p.from')
            length = len(polymerization)
            num = length - 1
            timeInfo = polymerization[num].find_element_by_css_selector('a[target="_blank"]').text

            if '年' in timeInfo:
                date = timeInfo
            elif '今天' in timeInfo:
                date = self.calcDate(timeInfo, 'day')
            elif '分钟前' in timeInfo:
                date = self.calcDate(timeInfo, 'minute')
            elif '秒前' in timeInfo:
                date = self.calcDate(timeInfo, 'second')
            else:
                year = str(datetime.datetime.now().year) + '年'
                date = year + timeInfo

            self.date = date
            self.status = self.isOneDay()

        except (NoSuchElementException, NoSuchAttributeException, IndexError):
            pass

        if self.status:
            try:
                contentUrl = polymerization[num].find_element_by_tag_name('a').get_attribute('href')
                contentUrl = self.urlFilter(contentUrl)
                deviceID = polymerization[num].find_element_by_css_selector('a[rel="nofollow"]').text
            except (NoSuchElementException, NoSuchAttributeException, IndexError):
                pass

            try:
                avatarTag = block.find_element_by_css_selector('div.card-feed>div.avator>a>img')
            except NoSuchElementException:
                pass
            else:
                avatar = avatarTag.get_attribute('src')
            # return dict(vid = deviceID)
            try:
                profile = block.find_element_by_css_selector('div.content>div.info')
                nickname = profile.find_element_by_css_selector('a.name').text
                userID = self.getUserID(profile.find_element_by_css_selector('a.name').get_attribute('href'))
                uid = self.getUID(userID)

                # If does not match this tag, then verification is null
                approveTag = profile.find_element_by_css_selector('a[href="//verified.weibo.com/verify"]')
                approve = approveTag.find_element_by_tag_name('i').get_attribute('class')

                if 'icon-vip-b' in approve:
                    verify = '微博官方认证'
                elif 'icon-vip-y' in approve or 'icon-vip-g' in approve:
                    verify = '微博个人认证'
            except (NoSuchAttributeException, NoSuchElementException):
                pass

            try:
                allClick = block.find_element_by_css_selector('div.content>p.txt>a[action-type="fl_unfold"]')
                allClick.click()
            except NoSuchElementException:
                pass

            try:
                text = block.find_element_by_css_selector('div.content>p[node-type="feed_list_content"]')
                content = self.contentFilter(text)
                contentLink = self.getContentLink(text)
            except (NoSuchElementException, IndexError):
                try:
                    text = block.find_element_by_css_selector('div.content>p[node-type="feed_list_content_full"]')
                    content = self.contentFilter(text)
                    contentLink = self.getContentLink(text)
                except (NoSuchElementException, IndexError):
                    pass

            try:
                media = block.find_element_by_css_selector('div.content>div[node-type="feed_list_media_prev"]')
            except NoSuchElementException:
                pass
            else:
                # Obtain video url
                try:
                    a = media.find_element_by_css_selector('div.thumbnail>a.WB_video_h5')
                    src = a.get_attribute('action-data')
                    video = self.getVideoLink(src)
                except (NoSuchElementException, NoSuchAttributeException):
                    # Pictures list display, one picture or picture list
                    try:
                        div = media.find_element_by_css_selector('div.media-piclist')
                        li = div.find_elements_by_css_selector('ul>li')
                        for img in li:
                            # Obtain image url
                            src = img.find_element_by_tag_name('img').get_attribute('src')  # Obtain image url
                            url = self.replaceBigPic(src)
                            imgUrls.append(url)
                    except (NoSuchElementException, NoSuchAttributeException):
                        pass

            '''
            Move Obtain time, timestamp and device id code to above
            '''
            try:
                feedAction = block.find_element_by_css_selector('div.card-act>ul')
            except NoSuchElementException:
                pass
            else:
                try:
                    li = feedAction.find_elements_by_css_selector('li>a')
                    # Forward number
                    forward = li[1].text
                    forwardNumber = 0 if forward.isalnum() else self.getDigit(forward)

                    # Comments number
                    comments = li[2].text
                    commentsNumber = 0 if comments.isalnum() else self.getDigit(comments)

                    # Like number
                    likes = li[3].find_element_by_tag_name('em').text
                    like = 0 if likes == '' else self.getDigit(likes)
                except (NoSuchElementException, IndexError):
                    pass

            data = dict(id = uid, userID = userID, avatar = avatar, nickname = nickname, verification = verify, text = content,
                        contentLink = contentLink, time = date, url = contentUrl, deviceID = deviceID, forwardNumber = forwardNumber,
                        commentsNumber = commentsNumber, like = like, video = video, imgUrls = imgUrls)

            return data


    def replaceBigPic(self, src):
        url = src.replace('thumb150', 'bmiddle')

        return url

    def getUID(self, userID):
        uid = uuid.uuid3(self.namespace, userID)
        code = str(uid).split('-')
        id = ''.join(code)

        return id

    def getUserID(self, id):
        match = re.findall(r'//weibo.com/(.*?)refer', id)
        uid = ''.join(match)
        userID = uid.rstrip('?')
        userID = userID.replace('u/', '')

        return userID

    def contentFilter(self, string):
        content = string.text
        content = content.replace('收起全文d', '')
        content = content.replace('|', '')

        try:
            a = string.find_elements_by_tag_name('a')
        except NoSuchElementException:
            pass
        else:
            for link in a:
                s = link.text
                if '@' not in s:
                    content = content.replace(s, '')

        return content.strip()

    def urlFilter(self, url):
        contentUrl = url.split('?refer')
        result = contentUrl[0]

        return result

    def getContentLink(self, text):
        href = list()
        try:
            contentLink = text.find_elements_by_tag_name('a[target="_blank"]')
        except (NoSuchElementException, NoSuchAttributeException):
            href = []
        else:
            for link in contentLink:
                try:
                    i = link.find_element_by_tag_name('i').text
                    if i == 'O':
                        str = link.get_attribute('href')
                        href.append(str)
                except NoSuchElementException:
                    continue

        return href

    def getVideoLink(self, src):
        utf8 = unquote(src, 'utf-8')
        find = re.findall(r'video_src=//(.*)&cover_img', utf8, re.S)

        return ''.join(find)

    def getDigit(self, text):
        try:
            number = int(re.sub('\D', '', text))
        except ValueError:
            number = 0

        return number

    def checkResult(self):
        try:
            error = self.browser.find_element_by_css_selector('div.card-wrap>div.card-no-result>p').text
        except NoSuchElementException:
            error = 'success'

        return error

    def calcDate(self, timeInfo, category):
        getTime = datetime.datetime.now()
        year = getTime.year
        month = getTime.month
        day = getTime.day
        date = ''

        if category == 'day':
            string = timeInfo.replace('今天', ' ')
            date = str(year) + '年' + str(month) + '月' + str(day) + '日' + string
        elif category == 'minute':
            before = self.getDigit(timeInfo)
            currentTime = int(time.time())
            second = before * 60
            real = currentTime - second
            local = time.localtime(real)
            date = time.strftime('%Y年%m月%d日 %H:%M', local)
        elif category == 'second':
            currentTime = int(time.time())
            local = time.localtime(currentTime)
            date = time.strftime('%Y年%m月%d日 %H:%M', local)

        return date

    def isOneDay(self):
        try:
            array = time.strptime(self.date, '%Y年%m月%d日 %H:%M')
            st = time.mktime(array)
            oneDay = 24 * 60 * 60
            diff = self.timestamp - int(st)
            if diff < oneDay:
                return True
            else:
                return False
        except ValueError:
            return False

    def closed(self):
        self.browser.close()

    def quit(self):
        self.browser.quit()


if __name__ == '__main__':
    try:
        keyword = sys.argv[1]
    except IndexError:
        obj = dict(errno = 5, error = 'Argument is missing')
        jsonObj = json.dumps(obj, ensure_ascii = False, indent = 4, separators = (',', ': '))
        print(jsonObj)
    else:
        browser = webdriver.Firefox()
        timestamp = int(time.time())
        process = Weibo(browser, timestamp)
        try:
            url = 'https://s.weibo.com/weibo?q=' + keyword
            t1 = int(time.time())
            obj = process.parseHTML(url)
            jsonObj = json.dumps(obj, ensure_ascii = False, indent = 4, separators = (',', ': '))
            print(jsonObj)
        except (TimeoutException, StaleElementReferenceException, WebDriverException):
            obj = dict(errno = 6, error = 'The connection has timed out!')
            jsonObj = json.dumps(obj, ensure_ascii = False, indent = 4, separators = (',', ': '))
            print(jsonObj)
        finally:
            process.quit()
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException
from urllib.parse import unquote
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from log import Log
from selenium.webdriver.common.keys import Keys
import re, json, uuid, sys, threading, time, datetime, sys


class Weibo:
    def __init__(self, browser):
        self.browser = browser
        self.namespace = uuid.NAMESPACE_URL

    def loadHTML(self, url, page):
        info = dict()

        if page == 1:
            self.browser.get(url)
            error = self.checkPage()
            if 'success' == error:
                one = self.loadFullPage()
                info[1] = one
            else:
                info = dict(errno = 1, error = error)
        elif page > 1000:
            for i in range(page):
                try:
                    self.browser.get(url + '&page=' + str(i + 1))
                    error = self.checkPage()
                    if 'success' == error:
                        multi = self.loadFullPage()
                        info[i] = multi
                    else:
                        info = dict(errno = 1, error = error)
                        break
                except TimeoutException:
                    break
        elif page > 1:
            self.browser.get(url)
            error = self.checkPage()
            for i in range(page):
                if i == page:
                    self.browser.close()
                    break
                if 'success' == error:
                    multi = self.loadFullPage()
                    info[i + 1] = multi
                    try:
                        self.browser.find_element_by_css_selector('a.next').click()
                    except NoSuchElementException:
                        break
                else:
                    info = dict(errno = 1, error = error)
                    break

        return info

    def loadFullPage(self):
        info = dict()
        try:
            try:
                # Mock mouse click 'see more'
                clicks = WebDriverWait(self.browser, 1).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'p.txt a[action-type="fl_unfold"]')))
                # clicks = self.browser.find_elements_by_css_selector('p.txt a[action-type="fl_unfold"]')
                for more in clicks:
                    more.click()
            except:
                pass

            # Scroll to the bottom
            # self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            self.browser.find_element_by_xpath('/html/body').send_keys(Keys.END)

            try:
                feedList = self.browser.find_element_by_css_selector('div.m-wrap div#pl_feedlist_index')
            except NoSuchElementException:
                data = dict(errno = 2, error = 'Not found feed list tag !')

                return data

            blocks = feedList.find_elements_by_css_selector('div div.card-wrap')
        except NoSuchElementException:
            data = dict(errno = 3, error = 'Web page can not open')

            return data
        else:
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
                    info[i] = data
                    i += 1

        return info

    # Parse one of block information
    def blockParse(self, block):
        detail = block
        imgUrls = list()
        forwardNumber = commentsNumber = like = 0
        nickname = verify = avatar = video = id = userID = time = content = deviceID = contentLink = ''

        try:
            mid = detail.get_attribute('mid')
            try:
                avatarTag = detail.find_element_by_css_selector('div.card-feed div.avator a img')
            except NoSuchElementException:
                pass
            else:
                avatar = avatarTag.get_attribute('src')

            try:
                profile = detail.find_element_by_css_selector('div.content div.info')
                nickname = profile.find_element_by_css_selector('a.name').text
                userID = self.getUserID(profile.find_element_by_css_selector('a.name').get_attribute('href'))
                id = self.getUID(userID)

                # If does not match this tag, then verification is null
                try:
                    approveTag = profile.find_element_by_css_selector('a[href="//verified.weibo.com/verify"]')
                    approve = approveTag.find_element_by_tag_name('i').get_attribute('class')

                    if 'icon-vip-b' in approve:
                        verify = '微博官方认证'
                    elif 'icon-vip-y' in approve or 'icon-vip-g' in approve:
                        verify = '微博个人认证'

                except (NoSuchAttributeException, NoSuchElementException) as e:
                    verify = ''
            except NoSuchElementException as e:
                pass

            try:
                text = detail.find_element_by_css_selector('div.content p[node-type="feed_list_content_full"]')
                if text.get_attribute('nick-name') == nickname:
                    content = self.contentFilter(text)
                    contentLink = self.getContentLink(text)
            except NoSuchElementException:
                try:
                    text = detail.find_element_by_css_selector('div.content p[node-type="feed_list_content"]')
                    if text.get_attribute('nick-name') == nickname:
                        content = self.contentFilter(text)
                        contentLink = self.getContentLink(text)
                except NoSuchElementException:
                    content = ''
                    contentLink = list()

            try:
                media = detail.find_element_by_css_selector('div.content div[node-type="feed_list_media_prev"]')
            except NoSuchElementException:
                pass
            else:
                # Obtain video url
                try:
                    a = media.find_element_by_css_selector('div.thumbnail a.WB_video_h5')
                    src = a.get_attribute('action-data')
                    if mid in src:
                        video = self.getVideoLink(src)
                except (NoSuchElementException, NoSuchAttributeException) as e:
                    # Pictures list display, one picture or picture list
                    try:
                        div = media.find_element_by_css_selector('div.media-piclist')
                        if mid in div.get_attribute('action-data'):
                            li = div.find_elements_by_css_selector('ul li')
                            for img in li:
                                # Obtain image url
                                src = img.find_element_by_tag_name('img').get_attribute('src')  # Obtain image url
                                url = self.replaceBigPic(src)
                                imgUrls.append(url)
                    except (NoSuchElementException, NoSuchAttributeException) as e:
                        pass

            try:
                # Obtain time, timestamp and device id
                polymerization = detail.find_elements_by_css_selector('div.content>p.from')
                length = len(polymerization)
                num = length - 1
                timeInfo = polymerization[num].find_element_by_css_selector('a[target="_blank"]').text
                if '年' in timeInfo:
                    time = timeInfo
                else:
                    year = str(datetime.datetime.now().year) + '年'
                    time = year + timeInfo
                try:
                    deviceID = polymerization[num].find_element_by_css_selector('a[rel="nofollow"]').text
                except NoSuchElementException:
                    pass
            except (NoSuchElementException, NoSuchAttributeException) as e:
                pass

            try:
                feedAction = detail.find_element_by_css_selector('div.card div.card-act')
                li = feedAction.find_elements_by_tag_name('li a')

                # Forward number
                forward = li[1].text
                forwardNumber = 0 if forward.isalnum() else self.getDigit(forward)

                # Comments number
                comments = li[2].text
                commentsNumber = 0 if comments.isalnum() else self.getDigit(comments)

                # Like number
                likes = li[3].find_element_by_tag_name('em').text
                like = 0 if likes == '' else self.getDigit(likes)

            except NoSuchElementException:
                pass
            data = dict(id = id, userID = userID, avatar = avatar, nickname = nickname, verification = verify,
                        text = content, contentLink = contentLink, time = time,
                        deviceID = deviceID, forwardNumber = forwardNumber, commentsNumber = commentsNumber,
                        like = like, video = video, imgUrls = imgUrls)

            return data
        except NoSuchElementException as e:
            print('Can not find block info, error: ' + str(e))

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
                    pass

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

    def checkPage(self):
        try:
            error = self.browser.find_element_by_css_selector('div.card-wrap div.card-no-result p').text
        except NoSuchElementException:
            error = 'success'

        return error

    def closed(self):
        self.browser.close()

    def quit(self):
        self.browser.quit()


if __name__ == '__main__':
    try:
        keyword = sys.argv[1]
        page = int(sys.argv[2])
    except IndexError:
        data = dict(errno = 4, error = 'Argument is missing')
        jsonObj = json.dumps(data, ensure_ascii = False, indent = 4, separators = (',', ': '))
        print(jsonObj)
    except ValueError:
        data = dict(errno = 5, error = 'Argument incorrect')
        jsonObj = json.dumps(data, ensure_ascii = False, indent = 4, separators = (',', ': '))
        print(jsonObj)
    else:
        profile = webdriver.FirefoxProfile()
        profile.set_preference('browser.privatebrowsing.autostart', True)
        browser = webdriver.Firefox(firefox_profile = profile)
        # browser.maximize_window()

        process = Weibo(browser)

        try:
            url = 'https://s.weibo.com/weibo?q=' + keyword
            data = process.loadHTML(url, page)
            jsonObj = json.dumps(data, ensure_ascii = False, indent = 4, separators = (',', ': '))
            print(jsonObj)
        except TimeoutException as e:
            data = dict(errno = 6, error = 'The connection has timed out!')
            jsonObj = json.dumps(data, ensure_ascii = False, indent = 4, separators = (',', ': '))
            print(jsonObj)
        finally:
            process.closed()

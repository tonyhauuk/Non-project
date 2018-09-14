# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import *

import re, json, uuid, sys, threading


class Weibo:
    def __init__(self, browser):
        self.browser = browser
        self.namespace = uuid.NAMESPACE_URL

    # Mock weibo login
    def login(self):
        username = ['']
        password = ''

    def loadHTML(self, url, page = 1):
        self.browser.get(url)
        data = dict()
        try:
            # Mock mouse click 'see more'
            clicks = self.browser.find_elements_by_css_selector('a.WB_text_opt')
            for more in clicks:
                more.click()
                break

            try:
                feedList = self.browser.find_element_by_css_selector('div.search_feed')
            except NoSuchElementException:
                sys.exit(1)

            blocks = feedList.find_elements_by_css_selector('div.search_feed>div[node-type="feed_list"]>div.WB_cardwrap')
        except NoSuchElementException as e:
            print('Load html function throw: ' + str(e))
            data = dict(errno = '1', error = 'Web can not open')
            return data
        else:
            for block in blocks:
                data = self.blockParse(block)
                break

        return data

    # Parse one of block information
    def blockParse(self, block):
        detail = None
        imgUrls = list()
        nickname = verify = avatar = video = id = userID = ''
        hrefLink = 'http://verified.weibo.com/verify'

        try:
            detail = block.find_element_by_css_selector('div.WB_feed_detail')
            nickInfo = detail.find_element_by_css_selector('div.feed_content.wbcon>a.W_texta.W_fb')
            nickname = nickInfo.text
            userID = self.getUserID(nickInfo.get_attribute('href'))
            id = self.getUID(userID)
        except NoSuchElementException as e:
            print('Can not find block info, error: ' + str(e))

        # If does not match this tag, then verification is null
        try:
            approve = detail.find_element_by_class_name('W_icon')
            href = approve.get_attribute('href')
            if href == hrefLink:
                verify = approve.get_attribute('title')
        except NoSuchElementException:
            verify = 'null'

        try:
            avatarTag = detail.find_element_by_css_selector('img.W_face_radius')
            avatarAlt = avatarTag.get_attribute('alt')
            if avatarAlt == nickname:
                avatar = avatarTag.get_attribute('src')

            text = self.browser.find_element_by_css_selector('div.feed_content.wbcon>p[node-type="feed_list_content_full"]').text
            content = self.filteContent(text)
            media = detail.find_element_by_css_selector('div.WB_media_wrap.clearfix')
            mediaBox = media.find_element_by_class_name('media_box')
            try:
                nodeType = mediaBox.get_attribute('node-type')
            except NoSuchAttributeException:
                # It only has just one single media, one picture or a video link
                try:
                    # Obtain img url
                    img = mediaBox.find_element_by_tag_name('img')
                    src = img.get_attribute('src')
                    url = self.replaceBigPic(src)
                    imgUrls.append(url)
                    video = 'null'
                except NoSuchElementException:
                    # Obtain video url
                    div = mediaBox.find_element_by_css_selector('div.con-2.hv-pos')
                    video = div.find_element_by_tag_name('video').get_attribute('src')
                    imgUrls = []
            else:
                # Pictures list display, more than one picture
                if nodeType == 'fl_pic_list':
                    li = mediaBox.find_elements_by_css_selector('li.WB_pic')  # Get a list of picture
                    for img in li:
                        src = img.find_element_by_tag_name('img').get_attribute('src')  # Obtain image url
                        url = self.replaceBigPic(src)
                        imgUrls.append(url)

            # Obtain time, timestamp and device id
            polymerization = detail.find_element_by_css_selector('div.feed_from.W_textb')
            timeInfo = polymerization.find_element_by_css_selector('a.W_textb')
            time = timeInfo.get_attribute('title')
            timestamp = timeInfo.get_attribute('date')
            deviceID = polymerization.find_element_by_css_selector('a[rel="nofollow"]').text

            # Obtain forward number, comments number and like number
            feedAction = self.browser.find_element_by_css_selector('div[action-type="feed_list_item"]>div.feed_action.clearfix>ul.feed_action_row4')
            li = feedAction.find_elements_by_tag_name('li>a')
            forward = li[1].find_element_by_tag_name('em').text
            comments = li[2].find_element_by_tag_name('em').text
            likes = li[3].find_element_by_tag_name('em').text

            forwardNum = 0 if forward == '' else int(forward)
            commentsNum = 0 if comments == '' else int(comments)
            like = 0 if likes == '' else int(likes)

            data = dict(id = id, userID = userID, avatar = avatar, nickname = nickname, verification = verify,
                        text = content, time = time, timestamp = timestamp, deviceID = deviceID,
                        forwardNum = forwardNum, commentsNum = commentsNum, like = like, video = video,
                        imgUrls = imgUrls)
            return data
        except NoSuchElementException as e:
            print(e)

    def replaceBigPic(self, src):
        url = src.replace('thunbnail', 'bmiddle')
        url = url.replace('square', 'bmiddle')

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

        return userID

    def filteContent(self, text):
        content = text.replace('收起全文d', '')

        return content

    def closed(self):
        self.browser.quit()
        print('\nBrowser closed !')


if __name__ == '__main__':
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.privatebrowsing.autostart", True)
    browser = webdriver.Firefox(firefox_profile = profile)

    process = Weibo(browser)
    try:
        url = 'http://s.weibo.com/weibo/nvidia&Refer=STopic_box'
        info = []
        data = process.loadHTML(url, 1)
        info.append(data)
        jsonObj = json.dumps(info, ensure_ascii = False, indent = 4, separators = (',', ': '))
        print(jsonObj)
    except:
        pass
    finally:
        process.closed()

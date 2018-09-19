# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException
from urllib.parse import unquote
# from app.weibo_project.log import Log

import re, json, uuid, sys, threading, time


class Weibo:
    def __init__(self, browser):
        self.browser = browser
        self.namespace = uuid.NAMESPACE_URL

    # Mock weibo login
    def login(self):
        username = ['']
        password = ''

    def loadHTML(self, url, page = 1):
        # log = Log()
        # log.create()
        # log.config()
        info = list()
        self.browser.get(url)
        try:
            # Mock mouse click 'see more'
            clicks = self.browser.find_elements_by_css_selector('a.WB_text_opt')
            for more in clicks:
                more.click()
                time.sleep(0.1)

            try:
                feedList = self.browser.find_element_by_css_selector('div#pl_weibo_direct')  # div.search_feed
            except NoSuchElementException:
                print('Not found feed list tag !')
                sys.exit(1)

            blocks = feedList.find_elements_by_css_selector('div.search_feed>div[node-type="feed_list"]>div.WB_cardwrap.S_bg2.clearfix')
        except NoSuchElementException as e:
            print('Load html function throw: ' + str(e))
            data = dict(errno = '1', error = 'Web page can not open')

            return data
        else:
            for block in blocks:
                data = self.blockParse(block)
                info.append(data)

        return info

    # Parse one of block information
    def blockParse(self, block):
        detail = None
        imgUrls = list()
        forwardNumber = commentsNumber = like = 0
        nickname = verify = avatar = video = id = userID = time = timestamp = deviceID = ''
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
        except (NoSuchElementException, NoSuchAttributeException):
            verify = ''

        try:
            avatarTag = detail.find_element_by_css_selector('img.W_face_radius')
            avatarAlt = avatarTag.get_attribute('alt')
            if avatarAlt == nickname:
                avatar = avatarTag.get_attribute('src')

            try:
                text = detail.find_element_by_css_selector('div.feed_content.wbcon>p[node-type="feed_list_content_full"]')
                content = self.contentFilter(text)
                contentLink = self.getContentLink(text)
            except NoSuchElementException:
                try:
                    text = detail.find_element_by_css_selector('div.feed_content>p.comment_txt')
                    content = self.contentFilter(text)
                    contentLink = self.getContentLink(text)
                except NoSuchElementException:
                    content = ''
                    contentLink = ''
            try:
                media = detail.find_element_by_css_selector('div.feed_content.wbcon>div.WB_media_wrap.clearfix')
                mediaBox = media.find_element_by_css_selector('div.media_box')
            except NoSuchElementException:
                pass
            else:
                try:
                    nodeType = mediaBox.get_attribute('node-type')
                    # Pictures list display, more than one picture
                    if nodeType == 'fl_pic_list':
                        li = mediaBox.find_elements_by_css_selector('li.WB_pic')  # Get a list of picture
                        for img in li:
                            src = img.find_element_by_tag_name('img').get_attribute('src')  # Obtain image url
                            url = self.replaceBigPic(src)
                            imgUrls.append(url)
                    else:
                        # It only has just one single media, one picture or a video frame
                        try:
                            # Obtain image url
                            img = mediaBox.find_element_by_css_selector('ul.WB_media_a>li>img')
                            src = img.get_attribute('src')
                            url = self.replaceBigPic(src)
                            imgUrls.append(url)
                            video = ''
                        except (NoSuchElementException, NoSuchAttributeException):
                            # Obtain video url
                            try:
                                div = mediaBox.find_element_by_css_selector('div.media_box_video_1>div.media_box_video_pic')
                                a = div.find_element_by_css_selector('a.WB_video.S_bg1.WB_video_a')
                                src = a.get_attribute('action-data')
                                video = self.getVideoLink(src)
                                imgUrls = []
                            except (NoSuchElementException, NoSuchAttributeException) as e:
                                pass
                except NoSuchElementException:
                    pass
            try:
                # Obtain time, timestamp and device id
                polymerization = detail.find_element_by_css_selector('div.feed_from.W_textb')
                timeInfo = polymerization.find_element_by_css_selector('a[node-type="feed_list_item_date"]')
                time = timeInfo.get_attribute('title')
                timestamp = timeInfo.get_attribute('date')
                try:
                    deviceID = polymerization.find_element_by_css_selector('a[rel="nofollow"]').text
                except NoSuchElementException:
                    pass
            except (NoSuchElementException, NoSuchAttributeException) as e:
                pass
            else:
                # Obtain forward number, comments number and like number
                try:
                    feedAction = block.find_element_by_css_selector('ul.feed_action_info.feed_action_row4')
                    li = feedAction.find_elements_by_tag_name('li>a')
                    # Forward number
                    try:
                        forward = li[1].find_element_by_tag_name('em').text
                        forwardNumber = 0 if forward == '' else int(forward)
                    except NoSuchElementException:
                        forwardNumber = 0

                    # Comments number
                    try:
                        comments = li[2].find_element_by_tag_name('em').text
                        commentsNumber = 0 if comments == '' else int(comments)
                    except NoSuchElementException:
                        commentsNumber = 0

                    # Like number
                    try:
                        likes = li[3].find_element_by_tag_name('em').text
                        like = 0 if likes == '' else int(likes)
                    except NoSuchElementException:
                        like = 0
                except NoSuchElementException:
                    pass

            data = dict(id = id, userID = userID, avatar = avatar, nickname = nickname, verification = verify,
                        text = content, contentLink = contentLink, time = time, timestamp = timestamp,
                        deviceID = deviceID, forwardNumber = forwardNumber, commentsNumber = commentsNumber,
                        like = like, video = video, imgUrls = imgUrls)
            return data
        except (NoSuchElementException, NoSuchAttributeException) as e:
            print('All Information error: ' + nickname + ' | ' + str(e))

    def replaceBigPic(self, src):
        url = src.replace('thumbnail', 'bmiddle')
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
        userID = userID.replace('u/', '')

        return userID

    def contentFilter(self, text):
        content = text.text.replace('收起全文d', '')
        content = content.replace('|', '')
        try:
            em = text.find_element_by_css_selector('em.W_autocut.W_linkb').text
        except NoSuchElementException:
            pass
        else:
            content = content.replace(em, '')

        try:
            videoLink = text.find_elements_by_css_selector('a.video_link')
        except NoSuchElementException:
            pass
        else:
            for link in videoLink:
                str = link.text
                content = content.replace(str, '')

        return content.strip()

    def getContentLink(self, text):
        try:
            contentLink = text.find_element_by_css_selector('a.W_btn_c6').get_attribute('href')
        except (NoSuchElementException, NoSuchAttributeException):
            contentLink = ''

        return contentLink

    def getVideoLink(self, src):
        utf8 = unquote(src, 'utf-8')
        find = re.findall(r'video_src=//(.*)&cover_img', utf8, re.S)

        return ''.join(find)

    def closed(self):
        self.browser.quit()
        print('\nBrowser closed !')


if __name__ == '__main__':
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.privatebrowsing.autostart", True)
    browser = webdriver.Firefox(firefox_profile = profile)

    process = Weibo(browser)
    try:
        url = 'http://s.weibo.com/weibo/nvidia%2520rtx'
        data = process.loadHTML(url, 1)
        jsonObj = json.dumps(data, ensure_ascii = False, indent = 4, separators = (',', ': '))
        print(jsonObj)
    except TimeoutException:
        pass
    finally:
        process.closed()

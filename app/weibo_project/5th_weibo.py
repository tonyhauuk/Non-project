# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptionsimport NoSuchElementException, NoSuchAttributeException, TimeoutException, StaleElementReferenceException, WebDriverException
from urllib.parse import unquote
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.byimport By
from selenium.webdriver.common.keysimport Keys
import re, json, uuid, time, datetime, sys


class WEIBO_SINA:
    url = ''
    tasktype = ''
    driver = ''
    returnDataType = ''

    index = 1

    def __init__(self, url, tasktype, driver, returnDataType):
        self.url = url
        self.tasktype = tasktype
        self.driver = driver
        self.returnDataType = returnDataType
        self.index = 1
        # self.namespace = uuid.NAMESPACE_URL
        self.timestamp = int(time.time())
        self.status = True

    # ***********************************************************
    # 微博页面下载
    # ***********************************************************
    def crawl(self):
        s1 = time.time()
        print("\t", self.index, sys._getframe().f_code.co_name, "begin")
        try:
            self.driver.get(self.url)
        except:  # TimeoutException as e:
            print("\t", self.index, "Browser timeout")
            return 'error'
        else:
            print("\t", "%-25s" % 'first load page', "%8.3f" % (time.time() - s1), "'s")
            data = self.get_web()
            result = json.dumps(data, ensure_ascii = False, indent = 4, separators = (',', ': '))

        return result

    # ***********************************************************
    # 微博页面处理
    # ***********************************************************
    def get_web(self):
        allInfo, info = dict(), dict()
        j = 1

        # 判断当前页返回信息是否正常
        error = self.checkResult()
        if error != 'success':
            allInfo = dict(errno = 1, error = error)
            return allInfo

        # 循环翻页，直到当前页没有满足的信息返回
        while True:
            # 判断是否有pl_feedlist_index块
            try:
                feedList = self.driver.find_element_by_css_selector('div.m-wrap>div#pl_feedlist_index')
            except:
                print("\t", self.index, 'pl_feedlist_index error')
                return 'error'

            # 提取所有 card-wrap 子块
            try:
                blocks = feedList.find_elements_by_css_selector('div.card-wrap')
            except:
                print('\t', self.index, "card-wrap   get error")
                return 'no info'

            index = 1
            for block in blocks:
                try:
                    mid = block.get_attribute('mid')  # 获取mid值
                    if not mid:  # 如果没有mid值，说明不是微博信息
                        continue
                except NoSuchAttributeException:
                    continue
                else:
                    data = self.blockParse(block, index)
                    if self.status:  # 满足条件才往info字典里加入
                        info[index] = data
                        index += 1

            if len(info) == 0 and j == 1:  # 如果当前第一页没有信息，直接跳出
                allInfo = dict(errno = 2, error = 'No results!')
                break
            elif len(info) == 0:  # 如果当前页没有信息，直接跳出，不再翻页
                break
            else:
                allInfo[j] = info

            try:
                # self.driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/div[1]/div[2]/div/a').click()  # 按照xpath方式提取，这种方式是最准确的
                self.driver.find_element_by_css_selector('a.next').click()  # 翻页
            except NoSuchElementException:
                break
            j += 1
            info = {}

        return allInfo

    # ***********************************************************
    # 解析每个块
    # ***********************************************************
    def blockParse(self, block, index):
        imgUrls, contentLink = list(), list()
        # 1、获取card-feed
        try:
            card_feed = block.find_element_by_css_selector('div.card>div.card-feed')
            class_content = card_feed.find_element_by_css_selector('div.content')
            # 下边这2行执行
            # from_hrefs = block.find_elements_by_css_selector('div.card>div.card-feed>div.content>p.from>a')#->div.content->p.from>a  div.card-feed
            from_hrefs = class_content.find_elements_by_css_selector('p.from>a')
            # 必须有2个a标签，否则返回
            length = len(from_hrefs)
            if 0 == length:
                print("\t", "%-25s" % 'p.from>a error  len=', "%d" % length)
                return ''
        except:
            print("\t", index, "%-25s" % '.card-feed error ')
            return ''

        # 1、获取时间,判断时间是否符合要求，及原始链接
        # *******************************************
        datetime = (from_hrefs[0].get_attribute('text')).strip()
        date = self.calcDate(datetime)

        # 时间不符合要求就返回
        if self.isOneDay(date) == False:
            self.status = False
            print('\t', index, "isOneDay timeout")
            return ''
        else:
            self.status = True


        if length > 1:
            deviceID = (from_hrefs[0].get_attribute('text')).strip()
            contentUrl = from_hrefs[0].get_attribute('href')
            contentUrl = self.urlFilter(contentUrl)
        else:
            deviceID = 'none'
            contentUrl = ''

        avatar = 'none'
        try:
            avatar = card_feed.find_element_by_css_selector('div.card-feed>div.avator>a>img').get_attribute('src')
        except:
            pass


        nickname = userID = verify = 'none'
        try:
            divs = class_content.find_elements_by_css_selector('div.info>div')
            a_s = divs[1].find_elements_by_css_selector('a')
            length = len(a_s)
            if length > 0:
                nickname = a_s[0].get_attribute('nick-name')
                userID = a_s[0].get_attribute('href').split('?')[0].split('/')[-1]
                if length > 1:
                    verify = a_s[1].get_attribute('title')
        except:
            pass

        try:
            # Mock mouse click 'see more'
            more = block.find_element_by_css_selector('p.txt>a[action-type="fl_unfold"]')
            more.click()
        except:
            pass

        try:
            p_txts = class_content.find_elements_by_css_selector('p.txt')
        except:
            return ''
        else:
            length = len(p_txts)
            if length > 0:
                text = p_txts[length - 1]
                content = self.contentFilter(text)
                contentLink = self.getContentLink(text)
            else:
                print("\t", "%-25s" % '.txterror  len=', "%d" % length)
                return ''


        video = ''
        try:
            media = class_content.find_element_by_css_selector('div[node-type="feed_list_media_prev"]')
        except NoSuchElementException:
            pass
        else:
            #  Obtain video url
            try:
                a = media.find_element_by_css_selector('div.thumbnail>a.WB_video_h5')
                src = a.get_attribute('action-data')
                video = self.getVideoLink(src)  # 过滤链接中杂乱信息
            except (NoSuchElementException, NoSuchAttributeException):
                # Pictures list display, one picture or picture list
                try:
                    div = media.find_element_by_css_selector('div.media-piclist')
                    li = div.find_elements_by_css_selector('ul>li')
                    for img in li:
                        #  Obtain image url
                        src = img.find_element_by_tag_name('img').get_attribute('src')  # Obtain image url
                        url = self.replaceBigPic(src)  # 替换大图片
                        imgUrls.append(url)
                except (NoSuchElementException, NoSuchAttributeException):
                    pass


        forwardNumber = commentsNumber = like = 0
        try:
            href_s = block.find_elements_by_css_selector('div.card>div.card-act>ul>li>a')
        except NoSuchElementException:
            print("\t", index, "%-25s" % 'div.card>div.card-act>ul->li->a error ')
        else:
            try:
                # Forward number
                forward = href_s[1].text
                forwardNumber = self.getDigit(forward)

                # Comments number
                comments = href_s[2].text
                commentsNumber = self.getDigit(comments)

                # Like number
                likes = href_s[3].find_element_by_tag_name('em').text
                like = 0 if likes == '' else int(likes)

            except (NoSuchElementException, IndexError):
                print("\t", index, "%-25s" % 'forward & comment & like error ')


        data = dict(userID = userID, avatar = avatar, nickname = nickname, verification = verify, text = content,
                    contentLink = contentLink, time = date, url = contentUrl, deviceID = deviceID, forwardNumber = forwardNumber,
                    commentsNumber = commentsNumber, like = like, video = video, imgUrls = imgUrls)

        return data

    def calcDate(self, timeInfo):
        getTime = datetime.datetime.now()
        year = getTime.year
        month = getTime.month
        day = getTime.day

        if '今天' in timeInfo:
            string = timeInfo.replace('今天', ' ')
            date = str(year) + '-' + str(month) + '-' + str(day) + '' + string + ':00'
        elif '分钟前' in timeInfo:
            before = self.getDigit(timeInfo)
            currentTime = int(time.time())
            second = before * 60
            real = currentTime - second
            local = time.localtime(real)
            date = time.strftime('%Y-%m-%d %H:%M:%S', local)
        elif '秒前' in timeInfo:
            before = getDigit(timeInfo)
            currentTime = int(time.time()) - before
            local = time.localtime(currentTime)
            date = time.strftime('%Y-%m-%d %H:%M:%S', local)
        else:
            year = str(datetime.datetime.now().year) + '-'
            date = year + timeInfo.replace('月', '-').replace('日', '') + ':00'

        return date


    @staticmethod
    def getDigit(text):
        try:
            number = int(re.sub('\D', '', text))
        except ValueError:
            number = 0

        return number

    def isOneDay(self, date):
        try:
            array = time.strptime(date, '%Y-%m-%d %H:%M:%S')
            st = time.mktime(array)
            oneDay = 24 * 60 * 60
            diff = self.timestamp - int(st)
            if diff < oneDay:
                return True
            else:
                return False
        except ValueError:
            return False


    @staticmethod
    def contentFilter(string):
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

    @staticmethod
    def getContentLink(text):
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

    @staticmethod
    def getVideoLink(src):
        utf8 = unquote(src, 'utf-8')
        find = re.findall(r'video_src=//(.*)&cover_img', utf8, re.S)

        return ''.join(find)

    @staticmethod
    def urlFilter(url):
        contentUrl = url.split('?refer')
        result = contentUrl[0]

        return result

    @staticmethod
    def replaceBigPic(src):
        url = src.replace('thumb150', 'bmiddle')
        url = url.replace('square', 'bmiddle')

        return url

    def checkResult(self):
        try:
            error = self.driver.find_element_by_css_selector('div.card-wrap>div.card-no-result>p').text
        except NoSuchElementException:
            error = 'success'

        return error


# ***********************************************************
# 打开一个浏览器
# ***********************************************************
def start_driver(timeout = 10):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable--gpu')

    count = 1
    while 1:
        try:
            driver = webdriver.Chrome(chrome_options = chrome_options)
        except:
            print(self.index, sys._getframe().f_code.co_name, ' init_web_driver error', 'count=', count)
            time.sleep(1)
        # return ''
        else:
            driver.set_page_load_timeout(timeout)
            driver.set_script_timeout(timeout)
            break
    return driver


if __name__ == '__main__':
    try:
        keyword = sys.argv[1]
    except IndexError:
        obj = dict(errno = 5, error = 'Argument is missing')
        jsonObj = json.dumps(obj, ensure_ascii = False, indent = 4, separators = (',', ': '))
        print(jsonObj)
    else:
        driver = start_driver(20)
        url = 'https://s.weibo.com/weibo?q=' + keyword
        tasktype = ''
        returnDataType = ''
        try:
            weibo_sina = WEIBO_SINA(url , tasktype , driver , returnDataType)
            myreturn = weibo_sina.crawl()
            print(myreturn)
        finally:
            driver.close()

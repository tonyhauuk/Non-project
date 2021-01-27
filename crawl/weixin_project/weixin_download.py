import requests, json
from PIL import Image
from PIL import ImageEnhance
import pytesseract, cv2
import numpy as np
import time, datetime, re, hashlib, os, sys
from time import sleep
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent

import requests, random, execjs

class WeixinApi:
    def __init__(self):
        self.url = 'http://api.tianapi.com/txapi/wxsearch/index'
        self.response = ''


    def doGet(self, kw):
        data = {
            'key': 'e2e7cf3c0c0aa44dacaf53b64d7a233f',
            'word': kw
        }

        # response = requests.get(self.url, params = data)
        # self.response = response.text

        # with open('tianMAO_json.json', 'w+', encoding = 'utf-8') as f:
        #     f.write(self.response)


        with open('tian_json.json', 'r', encoding = 'utf-8') as f:
            self.response = f.read()
            f.close()

        # return response.text
        # print(self.response)




    def obtain(self):
        content = json.loads(self.response, strict = False)
        code = content.get('code')
        urlList = []

        if code == 200:
            newsList = content.get('newslist')
            for item in newsList:
                try:
                    ctime = item.get('ctime')
                    title = item.get('title')
                    desc = item.get('description')
                    picUrl = item.get('picUrl')
                    link = item.get('url')

                    # print(ctime, title, desc, picUrl, link)
                    urlList.append(link.strip())
                except:
                    continue

        # print(urlList)
        self.getURL(urlList)

    def getURL(self, url):
        # with open('./blank.html', 'a+', encoding = 'utf-8') as f:
        #     f.write('<div>\n')
        #
        # for link in url:
        #     self.writeBlank(link)
        #
        # with open('./blank.html', 'a+', encoding = 'utf-8') as f:
        #     f.write('</div>')
        #
        # self.openUrl('file:///D://PyProject//Non-project//crawl//weixin_project//blank.html')


        for link in url:
            try:
                self.openUrl(link)
                break
            except Exception as e:
                print('Exception: ', e)
                continue



    def writeBlank(self, url):
        with open('./blank.html', 'a+', encoding = 'utf-8') as f:
            f.write('<a target="_blank" href="' + url + '">t</a>\n')



    def openUrl(self, url):
        # options = webdriver.FirefoxOptions()
        # userAgent = ['MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
        #              'Mozilla/5.0 (Linux; U; Android 4.1; en-us; GT-N7100 Build/JRO03C) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
        #             ]
        # options.add_argument('user-agent=%s' % userAgent[1])
        # script = 'Object.defineProperties(navigator, {webdriver:{get:()=>undefined}})'
        #
        # self.browser = webdriver.Firefox()
        # self.browser.execute_script(script)
        # self.browser.set_window_position(x = 630, y = 0)

        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        mobile_emulation = {
            "userAgent": 'Mozilla/5.0 (Linux; Android 4.0.3; HTC One X Build/IML74K) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19'
        }
        options.add_experimental_option("mobileEmulation", mobile_emulation)

        phoneAgent = [
            "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
            "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
            "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
            "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
            "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
            "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
            "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
            "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
            "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
            "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
            "UCWEB7.0.2.37/28/999",
            "Openwave/ UCWEB7.0.2.37/28/999",
            "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999"
        ]

        options.add_argument('user-agent=%s' % phoneAgent[10])
        self.browser = webdriver.Chrome(options = options, executable_path = r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        self.browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
          """
        })
        self.browser.set_window_position(x = 630, y = 0)

        try:
            # url = '''https://mp.weixin.qq.com/s?src=11&timestamp=1609816613&ver=2809&signature=mANNSjONrRLyR4WwpU2YLEPjmvXQ2gxWntG*rvRTW9yzsnEmNYK2m9t4-Af3XWhYCtTvTk9fBqQejhRqgrc9S1wZenMBxJBoO3LjP*AdbdSYawY1Mwc4FNy6IqdxLLLF&new=1'''
            # print(url, '\n')

            self.browser.get(url)
            sleep(1)
        except TimeoutException:
            pass


        pageHTML = ''
        try:
            pageHTML = self.browser.find_element_by_css_selector('div.rich_media_content').get_attribute('innerHTML')
        except NoSuchElementException:
            try:
                # verife = self.browser.find_element_by_css_selector('div.content-box > p.p3 > label').text
                verife = self.browser.find_element_by_css_selector('#verify-form > p:nth-child(5)').text
                if '验证码' in verife:
                    print('有验证码')

            except NoSuchElementException:
                pageHTML = self.browser.page_source

        # prefix = int(time.time())
        # with open(str(prefix) + '_weixin.html', 'w+', encoding = 'utf-8') as f:
        #     f.write(pageHTML)
        #     f.write('\n')

        self.browser.quit()



    def downloadFile(self, store_path):
        imgObj = self.browser.find_element_by_css_selector('p.p4 span.s1 a img#seccodeImage')

        url = imgObj.get_attribute('src')
        print('url:',url)
        filename = url.split('tc=')[-1]
        filepath = os.path.join(store_path, filename) + '.png'
        imgObj.screenshot(filepath)


        # imgData = requests.get(url, allow_redirects = True).content
        # with open(filepath, 'wb') as handler:
        #     handler.write(imgData)

        return filepath



    def ocrCode(self):

        # filename = 'D:\PyProject\/Non-project\crawl\weixin_project\/1609228332.png'
        # img = cv2.imread(filename, 0)
        # print(np.shape(img))
        # kernel = np.ones((1, 1), np.uint8)
        # dilate = cv2.dilate(img, kernel, iterations = 1)
        # cv2.imwrite('D:\PyProject\/Non-project\crawl\weixin_project\/new_1609228332.png', dilate)

        img = Image.open('D:\PyProject\/Non-project\crawl\weixin_project\/new_1609228332.png')
        img = img.convert('L')  # 这里也可以尝试使用L
        # img.show()
        enhancer = ImageEnhance.Color(img)
        enhancer = enhancer.enhance(0)
        enhancer = ImageEnhance.Brightness(enhancer)
        enhancer = enhancer.enhance(2)
        enhancer = ImageEnhance.Contrast(enhancer)
        enhancer = enhancer.enhance(8)
        enhancer = ImageEnhance.Sharpness(enhancer)
        img = enhancer.enhance(20)
        code = pytesseract.image_to_string(img)

        # threshold = 140
        # table = []
        # for i in range(256):
        #     if i < threshold:
        #         table.append(0)
        #     else:
        #         table.append(1)
        #
        # out = img.point(table, '1')
        # img = img.convert('RGB')
        # print(pytesseract.image_to_string(img))
        # print('ocr str:', code.strip())
        print('The code: %s' % code.strip())


    


if __name__ == '__main__':
    keyword = '茅台'

    wx = WeixinApi()
    # wx.doGet(keyword)
    # r = wx.obtain()
    wx.otherWay()

    # print(r)

import requests, json
from PIL import Image
from PIL import ImageEnhance
import pytesseract, cv2
import numpy as np
import time, datetime, re, hashlib, os, sys, shutil
from time import sleep
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent

class WeixinApi:
    def __init__(self):
        self.url = 'https://api.newrank.cn/api/sync/weixin/data/combine/search'
        self.response = ''


    def doGet(self, kw):
        key = {'Key': '183860ef3cd34f42ba8a757cc',}
        data = {
            'includeAllWords': kw,
            'from': '2020-01-05 15:00:00',
            'to': '2020-01-05 15:50:00',
            'size': 5,
        }

        # response = requests.post(url = self.url, data = data, headers = key)
        # self.response = response.text

        with open('newrand.json', 'r', encoding = 'utf-8') as f:
            self.response = f.read()
            f.close()

        # with open('newrand.json', 'w+', encoding = 'utf-8') as f:
            # f.write(self.response)
            # f.write('\n')

        # return response.text
        # print(self.response)




    def obtain(self):
        content = json.loads(self.response, strict = False)
        code = content.get('code')
        urlList = []

        if code == 0:
            newsList = content.get('data')
            for item in newsList:
                try:
                    ctime = item.get('updateTime')
                    title = item.get('title')
                    summary = item.get('summary')
                    imageUrl = item.get('imageUrl')
                    link = item.get('url')

                    # print(ctime, title, desc, picUrl, link)
                    urlList.append(link.strip())
                except:
                    continue

        # print(urlList)
        self.getURL(urlList)
        self.browser.quit()

    def getURL(self, url):
        options = webdriver.FirefoxOptions()
        userAgent = ['MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
                     'Mozilla/5.0 (Linux; U; Android 4.1; en-us; GT-N7100 Build/JRO03C) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
                    ]
        options.add_argument('user-agent=%s' % userAgent[1])
        script = 'Object.defineProperties(navigator, {webdriver:{get:()=>undefined}})'

        self.browser = webdriver.Firefox()
        self.browser.execute_script(script)

        # options = webdriver.ChromeOptions()
        # options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # options.add_experimental_option('useAutomationExtension', False)
        # userAgent = [
        #     'MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
        #     'Mozilla/5.0 (Linux; U; Android 4.1; en-us; GT-N7100 Build/JRO03C) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
        # ]
        # options.add_argument('user-agent=%s' % userAgent[1])
        # self.browser = webdriver.Chrome(options = options, executable_path = r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        # self.browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        #     "source": """
        #             Object.defineProperty(navigator, 'webdriver', {
        #               get: () => undefined
        #             })
        #           """
        # })

        self.browser.set_window_position(x = 630, y = 0)
        # element = self.browser.find_element_by_tag_name('body')
        # element.send_keys(Keys.CONTROL + 't')

        for link in url:
            try:
                self.openUrl(link)
                # break
            except Exception as e:
                print('Exception: ', e)
                continue


    def openUrl(self, url):
        try:
            # url = '''https://mp.weixin.qq.com/s?src=11&timestamp=1609816613&ver=2809&signature=mANNSjONrRLyR4WwpU2YLEPjmvXQ2gxWntG*rvRTW9yzsnEmNYK2m9t4-Af3XWhYCtTvTk9fBqQejhRqgrc9S1wZenMBxJBoO3LjP*AdbdSYawY1Mwc4FNy6IqdxLLLF&new=1'''
            # print(url, '\n')
            self.browser.get(url)
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
                    return
            except NoSuchElementException:
                pageHTML = self.browser.page_source

        prefix = int(time.time())
        htmlPath = './html/' + str(prefix) + '_weixin.html'
        with open(htmlPath, 'w+', encoding = 'utf-8') as f:
            f.write(pageHTML)
            # f.write('\n')

        # self.browser.quit()
        sleep(2)

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
        img = img.convert('RGB')  # L
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


    def removeHTML(self):
        filepath = './html'
        del_list = os.listdir(filepath)
        for f in del_list:
            file_path = os.path.join(filepath, f)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)



if __name__ == '__main__':
    keyword = '茅台'

    wx = WeixinApi()
    # wx.removeHTML()
    wx.doGet(keyword)
    r = wx.obtain()

    # print(r)

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

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
userAgent = [
    'MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
    'Mozilla/5.0 (Linux; U; Android 4.1; en-us; GT-N7100 Build/JRO03C) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
    ]
options.add_argument('user-agent=%s' % userAgent[1])
browser = webdriver.Chrome(options = options,
                          executable_path = r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
})

# url = '''https://mp.weixin.qq.com/s?src=11&timestamp=1609816613&ver=2809&signature=mANNSjONrRLyR4WwpU2YLEPjmvXQ2gxWntG*rvRTW9yzsnEmNYK2m9t4-Af3XWhYCtTvTk9fBqQejhRqgrc9S1wZenMBxJBoO3LjP*AdbdSYawY1Mwc4FNy6IqdxLLLF&new=1'''
url = '''
https://weixin.sogou.com/link?url=dn9a_-gY295K0Rci_xozVXfdMkSQTLW6cwJThYulHEtVjXrGTiVgS_FSfYk6v-_OeNG3qKrc2LT3vGBEN7MirVqXa8Fplpd9
kZa2__goD0ckID92mytav7shKVdcE3ntKqwPqj3O5Ehg-KLPdXHggDzFeM4e4yNHltKcOnAxYJBQoZ_OCIV0ZwSNtk3dHixPJeK_iGvzSyMycPd2jVpuKpCnyd7WxmdCcC
XHQ4rDjrydFzp3GeREgIyORLUFh2iq6j0bYj6DmUirCDCayYmfpA..&type=2&query=intel&token=1254355E2E56C4C9D3D66AF2F46F8FE9D3B18D305FF4045F
'''
browser.get(url)
try:
    pageHTML = browser.find_element_by_css_selector('div.rich_media_content').get_attribute('innerHTML')
    print(pageHTML)
except NoSuchElementException:
    try:
        # verife = browser.find_element_by_css_selector('div.content-box > p.p3 > label').text
        verife = browser.find_element_by_css_selector('#verify-form > p:nth-child(5)').text

        if '验证码' in verife:
            print('有验证码')
    except NoSuchElementException:
        pageHTML = browser.page_source

# browser.quit()


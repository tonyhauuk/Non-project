
from PIL import Image
import ddddocr
import time, hashlib, os, datetime
from time import sleep
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



url  = 'https://weixin.sogou.com/antispider/?from=%2fweixin%3Ftype%3d1%26query%3d%E6%BE%B6%E2%95%82%E8%A7%A612345%26ie%3dutf8%26s_from%3dinput%26_sug_%3dy%26_sug_type_%3d'

browser = webdriver.Firefox()
browser.set_window_position(x = 630, y = 0)
browser.get(url)

imgFile = 'codeImage.png'


if 'antispider' in browser.current_url:
    for i in range(5):

        if 'antispider' in browser.current_url:
            if i > 0:
                browser.find_element(by = By.CSS_SELECTOR, value = 'a#change-img').click()      # 点击换一张
                sleep(2)

            browser.execute_script('document.body.style.zoom="0.8"')
            verify = browser.find_element(by = By.CSS_SELECTOR, value = 'img#seccodeImage')
            verify.screenshot(imgFile)

            ocr = ddddocr.DdddOcr(show_ad = False)

            with open(imgFile, 'rb') as f:
                byte = f.read()

            res = ocr.classification(byte)
            print('Submit verify code times:', i + 1, '. The Code: ' + res + '\n')

            os.remove(imgFile)
            browser.find_element(by = By.CSS_SELECTOR, value = 'input#seccodeInput').send_keys(res) # 输入验证码
            sleep(2)
            browser.find_element(by = By.CSS_SELECTOR, value = 'a#submit').click()  # 点击‘提交’按钮
        else:
            break

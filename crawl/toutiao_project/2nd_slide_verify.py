# coding = utf-8
from selenium import webdriver
import time
import random
import uuid
from selenium.webdriver import ActionChains
from PIL import Image as Im
import os
import cv2.cv2 as cv2
import numpy as np
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def picDownload(url, type):
    url = url
    root = './'
    path = root + type + '.png'
    try:
        if not os.path.exists(root):
            os.mkdir(root)

        if os.path.exists(path):
            os.remove(path)

        r = requests.get(url)
        r.raise_for_status()

        with open(path, 'wb') as f:  # 开始写文件，wb代表写二进制文件
            f.write(r.content)

        return f.name

    except Exception as e:
        print('获取失败!' + str(e))


def getDistance(small, big):
    # 引用上面的图片下载
    otemp = picDownload(small, 'small')

    time.sleep(2)

    # 引用上面的图片下载
    oblk = picDownload(big, 'big')

    # 计算拼图还原距离
    target = cv2.imread(otemp, 0)
    template = cv2.imread(oblk, 0)
    w, h = target.shape[::-1]
    temp = 'temp.jpg'
    targ = 'targ.jpg'
    cv2.imwrite(temp, template)
    cv2.imwrite(targ, target)
    target = cv2.imread(targ)
    target = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
    target = abs(255 - target)
    cv2.imwrite(targ, target)
    target = cv2.imread(targ)
    template = cv2.imread(temp)
    result = cv2.matchTemplate(target, template, cv2.TM_CCOEFF_NORMED)
    x, y = np.unravel_index(result.argmax(), result.shape)
    # 缺口位置
    print((y, x, y + w, x + h))

    # 调用PIL Image 做测试
    image = Im.open(oblk)

    xy = (y + 20, x + 20, y + w - 20, x + h - 20)
    # 切割
    imagecrop = image.crop(xy)
    # 保存切割的缺口
    imagecrop.save("./new_image.jpg")
    return y


def mergePic():
    try:
        browser = webdriver.Firefox()
        browser.get("https://www.toutiao.com/search/?keyword=nvidia")
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'verify-bar-box')))
        # 先切换frame回到默认
        # browser.switch_to.default_content()

        # 将frame切换到 login_frame(也就是之前的登录frame)
        # browser.switch_to.frame("verify-bar-box")

        # 根据xpath获取到含有安全提示的标签然后将其中文本获取到打印出来 如果异常就进except块 说明没有验证码
        code = browser.find_element_by_id('verify-bar-box')
        # browser.refresh()
        # 如果后面拖动失败 我们就再次循环 所以用while
        while True:
            # 切换frame
            # browser.switch_to.default_content()
            #
            # # 切换frame
            # browser.switch_to.frame('login_frame')

            # 切换带有刷新按钮的frame
            # browser.switch_to.frame(browser.find_element_by_xpath('//*[@id="newVcodeIframe"]/iframe'))
            #
            # # 点击刷新 id为e_reload
            # browser.find_element_by_id('e_reload').click()

            # 获取图片链接
            big = browser.find_element_by_id('validate-big').get_attribute('src')
            small = browser.find_element_by_class_name('validate-block').get_attribute('src')

            # 下载图片并计算拼图还原的距离
            y = getDistance(small, big)

            # 获取当前网页链接，用于判断拖动验证码后是否成功,如果拖动后地址没变则为失败
            # url1 = browser.current_url

            # 获取蓝色拖动按钮对象
            element = browser.find_element_by_class_name('drag-button')

            # 计算distance
            distance = y * (55 / 268)
            # distance = y * 1 - 20
            print('distance:', distance)

            has_gone_dist = 0
            remaining_dist = distance
            # distance += randint(-10, 10)
            # 按下鼠标左键
            ActionChains(browser).click_and_hold(element).perform()
            time.sleep(0.5)

            while remaining_dist > 0:
                ratio = remaining_dist / distance
                if ratio < 0.2:
                    # 开始阶段移动较慢
                    span = random.randint(5, 8)
                elif ratio > 0.8:
                    # 结束阶段移动较慢
                    span = random.randint(5, 8)
                else:
                    # 中间部分移动快
                    span = random.randint(10, 16)

                ActionChains(browser).move_by_offset(span, random.randint(-5, 5)).perform()
                remaining_dist -= span
                has_gone_dist += span
                time.sleep(random.randint(5, 20) / 100)

            ActionChains(browser).move_by_offset(remaining_dist, random.randint(-5, 5)).perform()
            ActionChains(browser).release(on_element=element).perform()
            sections = browser.find_elements_by_css_selector('div.y-left.index-middle div.feedBox div')

            if len(sections) > 0:
                break
            # url2 = browser.current_url

            # frame切回到上一层
            # browser.switch_to.parent_frame()

            # 判断拖动按钮后网页地址是否有改变,如果变了则说明登录成功（失败则停留在该页面）
            # if url1 == url2:
            #     try:
            #         print(browser.find_element_by_class_name('tcaptcha-title').text)
            #         print('滑动失败!')
            #     except:
            #         print('帐号密码有误!')
            # else:
            #     print('登录成功!')
    except IOError:
        print('无安全验证码!')


if __name__ == '__main__':
    mergePic()
from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
import time, requests
import cv2.cv2 as cv2
from PIL import Image
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from io import BytesIO
import numpy as np

# https://blog.csdn.net/markme/article/details/94294724
# 首先定义一个破解滑块的类，这个是重点请仔细看
class Crackslide():
    '''
        通过浏览器截图，识别验证码中缺口位置，获取需要滑动距离，并模仿人类行为破解滑动验证码
    '''

    def __init__(self):
        super(Crackslide, self).__init__()
        self.browser = webdriver.Firefox()
        self.wait = WebDriverWait(self.browser, 20)
        self.zoom = 2


    # 定义一个获得目标图片和滑动模块的图片的获得
    def get_pic(self):
        time.sleep(2)
        target = self.browser.find_element_by_id('validate-big')
        template = self.browser.find_element_by_class_name('validate-block')
        target_link = target.get_attribute('src')
        template_link = template.get_attribute('src')
        target_img = Image.open(BytesIO(requests.get(target_link).content))
        template_img = Image.open(BytesIO(requests.get(template_link).content))
        target_img.save('./target.png')
        template_img.save('./template.png')
        size_orign = target.size
        local_img = Image.open('target.png')
        size_loc = local_img.size
        self.zoom = 320 / int(size_loc[0])

    # 定义等下行走的路径，用于模拟人类拖动滑块的行为
    def get_tracks(self, distance):
        print(distance)
        distance += 20
        v = 0
        t = 0.2
        forward_tracks = []
        current = 0
        mid = distance * 3 / 5
        while current < distance:
            if current < mid:
                a = 2
            else:
                a = -3
            s = v * t + 0.5 * a * (t ** 2)
            v = v + a * t
            current += s
            forward_tracks.append(round(s))
        back_track = [-3, -3, -2, -2, -2, -2, -2, -1, -1, -1]
        return {'forward_tracks': forward_tracks, 'back_tracks': back_track}

    # 把图片转化成矩阵，为上一个模拟路径提供相应的参数
    def match(self, target, template):
        loc = []
        img_rgb = cv2.imread(target)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(template, 0)
        run = 1
        w, h = template.shape[::-1]
        # print(w, h)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)

        # 使用二分法查找阈值的精确值
        L = 0
        R = 1
        while run < 20:
            run += 1
            threshold = (R + L) / 2
            if threshold < 0:
                print('Error')
                return None
            loc = np.where(res >= threshold)
            # print(len(loc[1]))
            if len(loc[1]) > 1:
                L += (R - L) / 2
            elif len(loc[1]) == 1:
                print('目标区域起点x坐标为：%d' % loc[1][0])
                break
            elif len(loc[1]) < 1:
                R -= (R - L) / 2

        return loc[1][0]

    # 开始模拟匹配
    def crack_slider(self):
        self.browser.get('https://www.toutiao.com/search/?keyword=nvidia')

        target =  './target.png'
        template = './template.png'
        self.get_pic()
        distance = self.match(target, template)
        zoo = 1  # 缩放系数，需要自己调整大小
        tracks = self.get_tracks((distance + 4) * zoo)  # 对位移的缩放计算
        # print(tracks)
        slider = self.browser.find_element_by_class_name('drag-button')
        ActionChains(self.browser).click_and_hold(slider).perform()

        for track in tracks['forward_tracks']:
            ActionChains(self.browser).move_by_offset(xoffset=track, yoffset=0).perform()

        time.sleep(0.5)
        for back_tracks in tracks['back_tracks']:
            ActionChains(self.browser).move_by_offset(xoffset=back_tracks, yoffset=0).perform()

        ActionChains(self.browser).move_by_offset(xoffset=-3, yoffset=0).perform()
        ActionChains(self.browser).move_by_offset(xoffset=3, yoffset=0).perform()
        time.sleep(0.5)
        ActionChains(self.browser).release().perform()
        try:
            failure = WebDriverWait(self.browser, 5).until(EC.text_to_be_present_in_element((By.ID, 'validate-prompt'), '按住左边按钮拖动完成上方拼图'))
            print(failure)
        except:
            print('验证成功')
            return None

        if failure:
            self.crack_slider()

    def close(self):
        time.sleep(5)
        self.browser.close()


if __name__ == '__main__':

    c = Crackslide()
    c.crack_slider()


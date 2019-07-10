from io import BytesIO
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
import time

EMAIL = ''
PASSWORD = ''


class SlideVerify():
    def __init__(self):
        self.url = 'https://account.geetest.com/login'
        self.browser = webdriver.Firefox()
        self.wait = WebDriverWait(self.browser, 20)
        self.email = EMAIL
        self.password = PASSWORD

    def getButton(self):
        button = self.wait.until(EC.element_to_be_clickable(By.CLASS_NAME, 'geetest_radar_tip'))

        return button

    def takeScreenshot(self):
        screenshot = self.browser.get_screenshot_as_png()
        pic = Image.open(BytesIO(screenshot))

        return pic

    def getPosition(self):
        img = self.wait.until(EC.presence_of_element_located(By.CLASS_NAME, 'geetest_canvas_img'))
        time.sleep(2)
        location = img.location
        size = img.size
        top = location['y']
        bottom = top + size['height']
        left = location['x']
        right = left + size['width']

        return (top, bottom, left, right)

    def getImage(self, name = 'captcha.png'):
        top, bottom, left, right = self.getPosition()
        print('pic position: ', top, bottom, left, right)
        screenshot = self.takeScreenshot()
        captcha = screenshot.crop((left, top, right, bottom))

        return captcha

    def getSlide(self):
        slider = self.wait.until(EC.element_to_be_clickable(By.CLASS_NAME, 'geetest_slider_button'))

        return slider

    def isEqual(self, img1, img2, x, y):
        pixel1 = img1.load()[x, y]
        pixel2 = img2.load()[x, y]
        threshold = 60
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(pixel1[2] - pixel2[2]) < threshold:
            return True
        else:
            return False

    def getGap(self, img1, img2):
        left = 60
        for i  in range(left, img1.size[0]):
            for j in range(img1.size[1]):
                if not  self.isEqual(img1, img2, i, j):
                    left = i
                    return left

        return left

    def setTrack(self, distance):
        track = []
        current = 0
        mid = distance * 4 / 5
        t = 0.2
        v = 0

        while current < distance:
            if current < mid:
                a = 2
            else:
                a = -3

            v0 = v
            # current speed: v = v0 + at
            v = v0 + a * t
            # track distance: x = v0t + 1/2 * a * t^2
            move = v0 * t + 1 / 2 * a * t * t
            # current offset
            current += move
            track.append(round(move))

            return track

    def moveToTrack(self, slider, tracks):
        ActionChains(self.browser).click_and_hold(slider).preform()
        for i in tracks:
            ActionChains(self.browser).move_by_offset(xoffset=i, yoffset=0).perform()
            time.sleep(0.5)

        ActionChains(self.browser).release().perform()

    def start(self):
        self.browser.get(self.url)
        email = self.browser.find_element_by_id('email')
        password = self.browser.find_element_by_id('password')
        email.send_keys(self.email)
        password.send_keys(self.password)

    def login(self):
        submit = self.wait.until(EC.element_to_be_clickable(By.CLASS_NAME, 'login-btn'))
        submit.click()
        time.sleep(5)
        print('login success')

    def crack(self):
        self.start()
        img1Name = ''
        img2Name = ''

        button = self.getButton()
        button.click()

        image1 = self.getImage(img1Name)
        slider = self.getSlide()
        slider.click()

        image2 = self.getImage(img2Name)
        gap = self.getGap(image1, image2)
        print('gap position ', gap)
        gap -= 6
        track = self.setTrack(gap)
        print('move slider ', track)
        self.moveToTrack(slider, track)

        success = self.wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, 'geetest_success_radar_tip_content'), '验证成功'))
        print(success)

        if not success:
            self.crack()
        else:
            self.login()

    def quit(self):
        self.browser.quit()


if __name__ == '__main__':
    crack = SlideVerify()
    crack.start()
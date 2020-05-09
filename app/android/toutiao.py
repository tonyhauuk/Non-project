from appium import webdriver
from time import sleep
from appium.common.exceptions import *


class Toutiao:
    def __init__(self):
        self.desiredCaps = {
            'platformName': 'Android',
            'deviceName': '127.0.0.1:7555',
            'appPackage': 'com.ss.android.article.lite',
            'appActivity': '.activity.SplashActivity',
        }

        self.server = 'http://localhost:4723/wd/hub'
        self.driver = webdriver.Remote(self.server, self.desiredCaps)

    def getSize(self):
        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        return (x, y)


    def swipeUp(self):
        l = self.getSize()
        x1 = int(l[0] * 0.5)
        y1 = int(l[1] * 0.75)
        y2 = int(l[1] * 0.25)

        self.driver.swipe(x1, y1, x1, y2, 500)

    def swipeDown(self):
        l = self.getSize()
        x1 = int(l[0] * 0.5)
        y1 = int(l[1] * 0.25)
        y2 = int(l[1] * 0.75)

        self.driver.swipe(x1, y1, x1, y2, 1000)

    def exec(self):
        print(self.driver.page_source)
        exit()

        results = self.driver.find_elements_by_xpath("//android.widget.TextView")
        for item in results:
            print(item.text)

    def tap(self):
        # 用户信息请求
        self.driver.find_element_by_id('com.ss.android.article.lite:id/q2').click()
        sleep(2)
        # 权限请求
        try:
            for i in range(2):
                self.driver.find_element_by_id('com.android.packageinstaller:id/permission_allow_button').click()
                sleep(2)
        except:
            sleep(2)
            self.driver.find_element_by_id('com.android.packageinstaller:id/permission_allow_button').click()
        # 红包
        self.driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.ImageView[1]').click()
        sleep(2)
        # 如果弹出更新，就点击
        try:
            self.driver.find_element_by_id('com.ss.android.article.lite:id/b7b').click()
        except:
            pass


if __name__ == '__main__':
    toutiao = Toutiao()
    toutiao.tap()
    sleep(5)
    try:
        for i in range(10):
            toutiao.swipeUp()
            sleep(2)

        # toutiao.exec()
    except Exception as e:
        print('Exception: ', e)


'''

我知道了：[210,1003][599,1037]
权限请求：[614,760][722,851]
红包：	[582,382][658,458]

'''
from appium import webdriver
from time import sleep


class KuaiShou:
    def __init__(self):
        self.desiredCaps = {
            'platformName': 'Android',
            'deviceName': '127.0.0.1:7555',
            'appPackage': 'com.kuaishou.nebula',
            'appActivity': 'com.yxcorp.gifshow.HomeActivity',
        }

        self.server = 'http://localhost:4723/wd/hub'
        self.driver = webdriver.Remote(self.server, self.desiredCaps)

    def getSize(self):
        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        return (x, y)

    def swipeUp(self):
        l = self.getSize()
        x1 = int(l[0] * 0.5)  # x坐标
        y1 = int(l[1] * 0.75)  # 起始y坐标
        y2 = int(l[1] * 0.25)  # 终点y坐标
        i = 0
        if i == 0:
            sleep(60)
            i += 1
        self.driver.swipe(x1, y1, x1, y2, 1000)


if __name__ == '__main__':
    kuaishou = KuaiShou()
    try:

        while 1:
            kuaishou.swipeUp()
            sleep(5)
    except Exception as e:
        kuaishou.swipeUp()
        sleep(5)
        print('Exception: ', e)

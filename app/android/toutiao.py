from appium import webdriver
from time import sleep


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

        self.driver.swipe(x1, y1, x1, y2, 1000)

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


if __name__ == '__main__':
    toutiao = Toutiao()
    sleep(10)
    try:
        for i in range(5):
            toutiao.swipeUp()
            sleep(2)

        toutiao.exec()
        sleep(120)
    except Exception as e:
        print('Exception: ', e)

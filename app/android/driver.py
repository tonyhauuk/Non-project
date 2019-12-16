from appium import webdriver
from time import sleep


class Action:
    def __init__(self):
        self.desiredCaps = {
            "platformName": "Android",
            "deviceName": "Android_SDK_built_for_arm64",
            "appPackage": "com.google.android.dialer",
            "appActivity": ".extensions.GoogleDialtactsActivity",
            "uiautomator2ServerInstallTimeout": 200000
        }

        self.server = 'http://localhost:4723/wd/hub'
        self.driver = webdriver.Remote(self.server, self.desiredCaps)

        self.startX = 200
        self.startY = 200
        self.distance = 50

    def doAction(self):
        print('tap \n')
        self.driver.tap([(500, 1200)], 500)
        sleep(2)
        self.driver.swipe(self.startX, self.startY, self.startY, self.startX - self.distance)
        sleep(2)
        self.driver.swipe(self.startX, self.startY, self.startY, self.startX - self.distance)
        print('swiped over! ')

if __name__ == '__main__':
    try:
        action = Action()
        action.doAction()
    except Exception as e:
        print('Exception: ', e)

# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException, StaleElementReferenceException, WebDriverException
from urllib.parse import unquote
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re, json, time, sys

class Tieba:
    def __init__(self, browser, timestamp):
        self.browser = browser
        self.timestamp = timestamp

    def main(self, url):
            try:
                self.browser.get(url)
                self.browser.find_element_by_xpath('/html/body').send_keys(Keys.END)
            except:
                return dict(errno = 2, error = 'Page can not open')
            else:
                pass

    def closed(self):
        self.browser.close()

    def quit(self):
        self.browser.quit()


if __name__ == '__main__':
    try:
        keyword = sys.argv[1]
    except IndexError:
        obj = dict(errno = 4, error = 'Argument is missing')
        jsonObj = json.dumps(obj, ensure_ascii = False, indent = 4, separators = (',', ': '))
        print(jsonObj)
    else:
        opts = webdriver.FirefoxOptions()
        # opts.add_argument('--headless')  # Headless browser
        # opts.add_argument('--disable-gpu')  # Disable gpu acceleration
        profile = webdriver.FirefoxProfile()
        profile.set_preference('browser.privatebrowsing.autostart', True)  # Start a private browsing
        browser = webdriver.Firefox(firefox_profile = profile, options = opts)

        timestamp = int(time.time())
        process = Tieba(browser, timestamp)
        try:
            url = 'http://tieba.baidu.com/f?ie=utf-8&kw=' + keyword +'&fr=search'
            obj = process.main(url)
            jsonObj = json.dumps(obj, ensure_ascii = False, indent = 4, separators = (',', ': '))
            print(jsonObj)
        except TimeoutException:
            obj = dict(errno = 6, error = 'The connection has timed out!')
            jsonObj = json.dumps(obj, ensure_ascii = False, indent = 4, separators = (',', ': '))
            print(jsonObj)
        finally:
            process.quit()
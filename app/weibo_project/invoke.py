from second_weibo_parser import Weibo
import re, json, uuid, sys, threading, time, datetime, sys
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException

try:
    keyword = sys.argv[1]
    page = int(sys.argv[2])
except IndexError:
    data = dict(errno = 4, error = 'Argument is missing')
    jsonObj = json.dumps(data, ensure_ascii = False, indent = 4, separators = (',', ': '))
    print(jsonObj)
except ValueError:
    data = dict(errno = 5, error = 'Argument incorrect')
    jsonObj = json.dumps(data, ensure_ascii = False, indent = 4, separators = (',', ': '))
    print(jsonObj)
else:
    profile = webdriver.FirefoxProfile()
    profile.set_preference('browser.privatebrowsing.autostart', True)
    browser = webdriver.Firefox(firefox_profile = profile)
    # browser.maximize_window()

    process = Weibo(browser)

    try:
        url = 'https://s.weibo.com/weibo?q=' + keyword
        data = process.loadHTML(url, page)
        jsonObj = json.dumps(data, ensure_ascii = False, indent = 4, separators = (',', ': '))
        print(jsonObj)
    except TimeoutException:
        data = dict(errno = 6, error = 'The connection has timed out!')
        jsonObj = json.dumps(data, ensure_ascii = False, indent = 4, separators = (',', ': '))
        print(jsonObj)
    finally:
        process.closed()
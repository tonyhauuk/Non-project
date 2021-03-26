# coding: utf-8
import requests, random, re, time, hashlib, os, sys, json
from http import cookiejar
from urllib import request, parse
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import time, os, datetime, subprocess
from apscheduler.schedulers.blocking import BlockingScheduler
from selenium import webdriver

sys.path.append('..')
from crawlerfun import ClearCache


def clean(browser):
    subprocess.Popen('rm -rf /dev/shm/cache', shell = True, stdout = subprocess.PIPE)
    subprocess.Popen('rm nohup.out -rf', shell = True, stdout = subprocess.PIPE)
    subprocess.Popen('tmpwatch 1 /tmp/', shell = True, stdout = subprocess.PIPE)
    ClearCache(browser)


def startBrowser():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-logging')
    options.add_argument("--disable-infobars")
    options.add_argument(
        'user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.103 Safari/537.36"')
    options.add_argument('--disk-cache-dir=%s' % '/dev/shm/cache')
    browser = webdriver.Chrome(chrome_options = options)
    browser.set_window_size(1050, 685)
    browser.set_window_position(x = 225, y = 0)
    clean(browser)

    return browser


def getUserList():
    d = getAccountList()

    with open('../../kw_weixin_more.txt', mode = 'r', encoding = 'utf-8') as f:
        keywords = f.readlines()

    browser = startBrowser()

    for keyword in keywords:
        keyword = keyword.strip()
        if keyword == '':
            continue
        keyword = parse.unquote(keyword, encoding = 'utf-8', errors = 'replace')
        # keyword = parse.quote(keyword)
        try:
            userList = d[keyword]
        except KeyError:
            userSet = set()
        else:
            userSet = set(userList)

        url = 'https://weixin.sogou.com/weixin?type=2&s_from=input&query=' + keyword + '&ie=utf8'
        browser.get(url)

        for i in range(10):
            itemList = browser.find_elements_by_css_selector('div.news-box > ul.news-list > li')
            for item in itemList:
                account = item.find_element_by_css_selector('div.txt-box > div.s-p > a').text
                userSet.add(account)

            if i == 10:
                break

            try:
                browser.find_element_by_partial_link_text('下一页').click()
            except NoSuchElementException:
                break

        userList = list(userSet)
        d[keyword] = userList

    browser.quit()
    print('=' * 10, 'mp account finished!', '=' * 10)

    # 更新txt文件
    try:
        fileName = './userList.json'
        jsonStr = json.dumps(d, indent = 4, ensure_ascii = False).replace("'", '"')
        with open(fileName, 'w') as json_file:
            json_file.write(jsonStr)

    except Exception as e:
        print('expire exception: ', e)


def getAccountList():
    d = {}
    file = './userList.json'
    try:
        with open(file, mode = 'r') as f:
            jsonStr = json.load(f)
            if jsonStr != '':
                d = eval(str(jsonStr))  # 直接把字符串转成字典格式

        return d
    except Exception as e:
        # 如果没有文件，则直接创建文件
        fd = open(file, mode = 'a+', encoding = 'utf-8')
        fd.close()

        return d


if __name__ == '__main__':
    getUserList()

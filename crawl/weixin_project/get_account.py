import requests, random, re, execjs, time, hashlib, os
from http import cookiejar
from urllib import request, parse
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def getUserList():
    d = {}
    with open('./mp_weixin/keywords') as f:
        keywords = f.readlines()

    browser = webdriver.Firefox()
    browser.set_window_position(x = 630, y = 0)

    for keyword in keywords:
        keyword = keyword.strip()
        # keyword = parse.quote(keyword)
        url = 'https://weixin.sogou.com/weixin?type=2&s_from=input&query=' + keyword + '&ie=utf8'
        browser.get(url)
        userSet = set()

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


    # 更新txt文件
    try:
        fileName = './mp_weixin/userList.json'
        # os.remove(fileName)
        with open(fileName, 'w') as f:
            f.write(str(d))
    except Exception as e:
        print('expire exception: ', e)







if __name__ == '__main__':
    getUserList()

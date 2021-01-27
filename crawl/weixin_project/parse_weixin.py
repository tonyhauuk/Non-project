import requests, random, re, execjs, time
from http import cookiejar
from urllib import request, parse
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def otherWay(keyword, link):
    s = parse.quote(keyword)
    cookie = getCookies(s)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6788.400 QQBrowser/10.3.2843.400',
        'Referer': 'https://weixin.sogou.com/weixin?type=2&s_from=input&query=' + s + '&ie=utf8',
        # 'Cookie': 'SNUID=308390CEB3B60A58629B2F6DB3059D07; SUID=598982DE3108990A000000005E12CF25; SUV=1578290991881935; sortcookie=1; LSTMV=466%2C77; LCLKINT=6458; ABTEST=1|1609224462|v1; weixinIndexVisited=1; IPLOC=CN1100; JSESSIONID=aaa65j_AInKVcdDe8zHBx',
        'Cookie': cookie,
    }

    url = url_decode(link)

    resp = requests.get(url, headers = headers)
    jsCode = resp.content.decode('utf8')
    # comment = re.compile('<script>(.*?)</script>', re.DOTALL)
    comment = re.compile('setTimeout(.*?)},100', re.DOTALL)
    jsCode = 'f = function(){%s}' % (comment.findall(jsCode)[0].replace('window.location.replace(url)', 'return url;'))
    jsCode = jsCode.replace('(function () {', '')

    print(jsCode)
    result = execjs.compile(jsCode).call('f')

    browser = webdriver.Firefox()
    browser.set_window_position(x = 630, y = 0)
    browser.get(result)
    time.sleep(5)

    # cookie = browser.get_cookies()
    # print(cookie)
    browser.quit()


def getCookies(keyword):
    url = 'https://weixin.sogou.com/weixin?type=2&s_from=input&query=' + keyword + '&ie=utf8'
    cookie = cookiejar.CookieJar()
    cookieHandler = request.HTTPCookieProcessor(cookie)
    httpHandler = request.HTTPHandler()
    httpsHandler = request.HTTPSHandler()

    opener = request.build_opener(cookieHandler, httpHandler, httpsHandler)
    response = opener.open(url)
    c = ''
    for item in cookie:
        # print('Name = %s' % item.name, ' | Value = %s' % item.value)
        c += item.name + '=' + item.value + '; '

    return c

    # req = requests.get(url)
    # cookies = requests.utils.dict_from_cookiejar(req.cookies)

    # Hostreferer = {
    #     # 'Host':'***',
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
    # }
    # html = requests.get(url, headers = Hostreferer, verify = True)
    # if html.status_code == 200:
    #     print(html.cookies)


def url_decode(r):
    url = 'https://weixin.sogou.com' + r
    b = random.randint(0, 99)
    a = url.index('url=')
    a = url[a + 30 + b: a + 31 + b:]
    url += '&k=' + str(b) + '&h=' + a

    return url


def openWeb():
    browser = webdriver.Firefox()
    browser.get('')


if __name__ == '__main__':
    keyword = '茅台'
    link = '/link?url=dn9a_-gY295K0Rci_xozVXfdMkSQTLW6cwJThYulHEtVjXrGTiVgS6s_dlq_R1ePdaUOflFypRHNlBDk6J7AilqXa8Fplpd9Hp-0Xf8pS0yCTiM_mZ9F2dQnYkaqz6O8EVYjlOoi3deWsPSniRW85H6p1ngoP46XrDgVJ15F4AGOdfrfPKRk2JixLxRGSjvCX7CPToefKXqzCLvuziEw4kmji06VhxrebPo-jg01wy7j4g9vnypLD7SKl0d1ZikT-6hmAQNF5YyTJmCU1UgHwQ..&type=2&query=880%E4%B8%87%E7%93%B6%E8%8C%85%E5%8F%B0%E5%93%84%E6%8A%A2%E7%9C%9F%E7%9B%B8:%E6%B2%A1%E4%BA%BA%E5%96%9D,%E9%83%BD%E6%83%B3%E5%80%92%E5%8D%96&token=5AF3BE97C677673B4543FC64E3979E4B46EB54C160052E1C'

    otherWay(keyword, link)
    # getCookies()

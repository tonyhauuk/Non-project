import requests
import json
import random
import time
# from requests.packages.urllib3.exceptions import InsecureRequestWarning
# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  ###禁止提醒SSL警告
import hashlib
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import Request
from selenium import webdriver
import re
import html
import redis
import urllib

s = requests.session()


def get_search_article(keyword, offset=0):
    page = 0
    # keyword = urllib.request.quote(keyword)
    req_url = "https://www.toutiao.com/search_content/?offset={}&format=json&keyword={}&autoload=true&count=20&cur_tab=1&from=search_tab".format(
        offset, keyword)
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Connection': 'keep-alive',
        'authority': 'www.toutiao.com',
        'referer': "https://www.toutiao.com/search/?keyword={}".format(keyword),
        'method': 'GET',
        'path': "https://www.toutiao.com/search/?keyword={}".format(keyword),
        'scheme': 'https'
    }
    s.headers.update(headers)
    req = s.get(req_url, proxies=get_proxy_ip())

    time.sleep(random.random() * 2 + 3)
    data = json.loads(req.text)
    items = data['data']
    print(data)
    if data['has_more'] == 1:
        page = page + 1
        offset = 20 * page
        # parse_data(items)
        time.sleep(2)
        get_search_article(keyword, offset)
    # else:
        # parse_data(items)
        # toutiaodb.save(search_item_list)


def get_ip_list(obj):
    ip_text = obj.findAll('tr', {'class': 'odd'})
    ip_list = []
    for i in range(len(ip_text)):
        ip_tag = ip_text[i].findAll('td')
        ip_port = ip_tag[1].get_text() + ':' + ip_tag[2].get_text()
        ip_list.append(ip_port)
    # print("共收集到了{}个代理IP".format(len(ip_list)))
    # print(ip_list)
    return ip_list


def get_random_ip(bsObj):
    ip_list = get_ip_list(bsObj)
    import random
    random_ip = 'http://' + random.choice(ip_list)
    proxy_ip = {'http:': random_ip}
    return proxy_ip

def get_proxy_ip():
    url = 'http://www.xicidaili.com/'
    headers = {
        'User-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}
    request = Request(url, headers=headers)
    response = urlopen(request)
    bsObj = BeautifulSoup(response, 'lxml')
    random_ip = get_random_ip(bsObj)
    return random_ip


if __name__ == '__main__':
    get_search_article('nvidia')
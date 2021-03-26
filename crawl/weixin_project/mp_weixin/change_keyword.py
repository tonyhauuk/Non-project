import requests, random, re, execjs, time, hashlib, os, sys, json, gc
from http import cookiejar
from urllib import request, parse
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import configparser

def getAccountList(file):
    with open(file, mode = 'r') as f:
        jsonStr = json.load(f)
        if jsonStr != '':
            d = eval(str(jsonStr))  # 直接把字符串转成字典格式


        # jsonStr = json.load(str(jsonStr))
        # print(jsonStr)

        # json解析并按key排序
        json_str = json.dumps(jsonStr, sort_keys = True)
        # 将 JSON 对象转换为 Python 字典
        params_json = json.loads(json_str)

        items = params_json.items()
        for key, value in items:
            # print(str(key) + '=' +
            keyword = parse.unquote(key, encoding = 'utf-8', errors = 'replace')
            print(str(key), ' | ', keyword)



if __name__ == '__main__':
    fileName = 'userList.json'
    getAccountList(fileName)

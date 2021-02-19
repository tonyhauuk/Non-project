import requests, random, re, execjs, time, hashlib, os, sys, json, gc
from http import cookiejar
from urllib import request, parse
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import configparser


def getUserList():
    configFile = 'weixin.ini'
    conf = configparser.ConfigParser()
    conf.read(configFile)
    sections = conf.sections()
    option = conf.options(sections[0])

    mode = conf.get(sections[0], option[0])             # 采集模式：全采集，精确采集
    mpPage = int(conf.get(sections[0],option[1]))       # 是否采集公众号搜索页面, 0:关闭，1：开启
    delOld = int(conf.get(sections[0],option[2]))       # 是否保留删除的公众号信息, 0:关闭，1：开启

    fileName = 'userList.json'
    d = getAccountList(fileName)

    with open('keywords', mode = 'r', encoding = 'utf-8') as f:
        keywords = f.readlines()

    if delOld == 1:
        d = saveDelKeyword(d, keywords)

    exit()
    browser = webdriver.Firefox()
    browser.set_window_position(x = 630, y = 0)

    try:
        if mpPage == 1:
            d = getMpPage(d, browser, keywords)

        d = normalPage(d, browser, keywords, mode)
    except Exception as e:
        print('page exception:', e)
    finally:
        pass
        browser.quit()

    # 更新txt文件
    try:
        fileName = 'userList.json'
        jsonStr = json.dumps(d, indent = 4, ensure_ascii = False).replace("'", '"')
        with open(fileName, 'w') as json_file:
            json_file.write(jsonStr)
    except Exception as e:
        print('\nupdate json exception: ', e)


# 获取json文件的公众号列表
def getAccountList(file):
    d = {}
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


# 公众号页面采集
def getMpPage(d, browser, keywords):
    for keyword in keywords:
        keyword = keyword.strip()
        if keyword == '':
            continue

        lst = []
        url = 'https://weixin.sogou.com/weixin?type=1&s_from=input&query=' + keyword + '&ie=utf8'
        browser.get(url)
        time.sleep(1)

        while True:
            itemList = browser.find_elements_by_css_selector('div.news-box > ul.news-list2 > li')
            for item in itemList:
                nickName = item.find_element_by_css_selector('p.tit > a').text              # 微信名
                account = item.find_element_by_css_selector('p.info  > label').text         # 微信账号
                mpInfo = item.find_element_by_css_selector('p.info').text                   # 每个月发布文章数量

                if '月发文' in mpInfo:
                    count = mpInfo.split('月发文')[1]
                    preMonth = re.sub('\D', '', count)
                    preMonth = int(preMonth)
                else:
                    preMonth = 0

                info = dict()
                info['nickname'] = nickName
                info['account'] = account
                info['preMonth'] = preMonth

                lst.append(info)

            try:
                browser.find_element_by_partial_link_text('下一页').click()
            except NoSuchElementException:
                break


        # 去重合并新的值
        userList = mergeDuplicate(d[keyword], lst)
        d[keyword] = userList

    return d


# 正常网页爬取
def normalPage(d, browser, keywords, mode):
    for keyword in keywords:
        keyword = keyword.strip()
        if keyword == '':
            continue

        lst = []
        url = 'https://weixin.sogou.com/weixin?type=2&s_from=input&query=' + keyword + '&ie=utf8'
        browser.get(url)

        for i in range(10):
            itemList = browser.find_elements_by_css_selector('div.news-box > ul.news-list > li')
            for item in itemList:
                nickName = item.find_element_by_css_selector('div.s-p > a.account').text    # 微信名

                info = dict()
                info['nickname'] = nickName
                info['account'] = ''

                lst.append(info)

            if mode == 'full':
                try:
                    browser.find_element_by_partial_link_text('下一页').click()
                except NoSuchElementException:
                    break
            elif mode == 'short':
                break

        # merge&dup dict
        userList = mergeDuplicate(d[keyword], lst)
        d[keyword] = userList

    return d


def mergeDuplicate(oldList, newList):
    tempList = list()
    userSet = set()

    for oldDict in oldList:
        oldNickName = oldDict.get('nickname')   # Obtain old list's nickname
        userSet.add(oldNickName)                # Put oldnickname into userSet

    for newDict in newList:
        newNickName = newDict.get('nickname')   # Obtain new list's nickname

        if newNickName in userSet:              # If new list's value exist in old list, then update old list 'preMonth' fiels
            if newDict.get('account') != '':    # If new list's 'account' field is empty, make known crawl from mp_page, need to update current field
                for oldDict in oldList:
                    if oldDict.get('nickname') == newNickName:  # Find the index from old list
                        oldDict['preMonth'] = newDict.get('preMonth')
                        break
            else:
                continue
        else:
            userSet.add(newNickName)        # If does not exist, then push the new value into set()
            tempList.append(newDict)        # Record the new value into a temporary list()


    # for newDict in newList:
    #     newNickName = newDict.get('nickname')       # 获取要插入列表的nickname
    #     for oldDict in oldList:
    #         oldNickName = oldDict.get('nickname')   # 获取老列表的nickname
    #         userSet.add(oldNickName)                # 把老列表的值插入set里
    #
    #         if newNickName in userSet:              # 如果新列表的值在老列表当中，就更新老列表的preMonth字段
    #             if newDict.get('account') != '':
    #                 oldDict['preMonth'] = newDict.get('preMonth')
    #             break
    #         else:
    #             userSet.add(newNickName)        # 如果不存在，记录新值
    #             tempList.append(newDict)        # 并且把老列表没有的值，记录在一个临时的列表当中
    #             break

    origin = oldList + tempList
    userSet = tempList = None

    return origin


# 保留删除关键词有关的微信公众号
def saveDelKeyword(d, keywords):
    delKeyword = []
    newDict = {}
    origin = d

    for k, v in d.items():
        if k not in keywords:
            newDict[k] = v
            delKeyword.append(k)

    fileName = 'saveDel.json'
    saveDict = getAccountList(fileName)
    saveDict.update(newDict)

    # 更新爬取信息的关键词列表
    for key in delKeyword:
        try:
            d.pop(key)
        except:
            continue

    # 更新txt文件
    try:
        fileName = '/home/zran/src/crawler/32/manzhua/crawlpy3/mp_weixin/' + fileName
        os.remove(fileName)
        with open(fileName, 'a+') as f:
            f.write(str(saveDict))

        return d
    except Exception as e:
        print('write save old keyword error:', e)

        return origin



if __name__ == '__main__':
    # getUserList()

    a = [{"nickname": "IntelShenzhen","account": "IntelShenzhen","preMonth": 0},
         {"nickname": "IIIIII","account": "MergerIntel","preMonth": 888},
         {"nickname": "xjintel","account": "xjintelsoda","preMonth": 369},
         {"nickname": "bbbbbbbbb", "account": "bbbbbbbbbb", "preMonth": 1}]

    b = [{"nickname": "IntelShenzhen", "account": "IntelShenzhen", "preMonth": 2},
         {"nickname": "IIIIII", "account": "MergerIntel", "preMonth": 2},
         {"nickname": "nv", "account": "nv", "preMonth": 2},
         {"nickname": "nvidia", "account": "nv_vhina", "preMonth": 2},
         {"nickname": "bbbbbbbbb", "account": "bbbbbbbbbb", "preMonth": 2}]

    r = mergeDuplicate(a, b)

    # exit()
    for x in r:
        print(x)
        # print('-'*20)
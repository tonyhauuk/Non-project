# -*- coding: utf-8 -*-

import threading
import sys
import os
from bs4 import BeautifulSoup
import re, json, uuid

import hashlib  # md5
import time
import random
import socket
import struct
from w3lib.html import remove_comments
from w3lib import html


# 生成md5信息
def makeMD5(link):
    m = hashlib.md5()
    b = link.encode(encoding = 'utf-8')
    m.update(b)
    enc = m.hexdigest()

    return enc


# 重新修改文件夹名称
def renameNew():
    try:
        root = '/estar/newhuike2/1/'
        lst = os.listdir(root)
        for l in lst:
            if '_' in l:
                os.rename(root + l, root + l.strip('_'))
    except:
        pass


# 删除过期的记录
def expire(date, d, name):
    # 检查过期数据
    li = []
    current = date.split(' ')[0]
    for k, v in d.items():
        if current != v:
            li.append(k)

    # 删除字典里过期的数据
    for i in li:
        d.pop(i)

    # 更新txt文件
    try:
        fileName = '/home/zran/src/crawler/33/manzhua/crawlpy3/record/' + name + '_md5.txt'
        os.remove(fileName)
        with open(fileName, 'a+') as f:
            f.write(str(d))
    except Exception as e:
        print('expire exception: ', e)


def initDict(name):
    d = {}
    file = '/home/zran/src/crawler/33/manzhua/crawlpy3/record/' + name + '_md5.txt'
    try:
        with open(file, mode = 'r') as f:
            line = f.readline()
            if line != '':
                d = eval(str(line))  # 直接把字符串转成字典格式

        return d
    except:
        # 如果没有文件，则直接创建文件
        fd = open(file, mode = 'a+', encoding = 'utf-8')
        fd.close()

        return d


def deleteFiles(projectName):
    filePath = '/root/estar_save/' + projectName + '/'
    timeStamp = time.time()
    timeArray = time.localtime(timeStamp)
    current = time.strftime("%Y-%m-%d", timeArray)
    name = os.listdir(filePath)

    for i in name:
        try:
            fileName = filePath + i
            fileInfo = os.stat(fileName)
        except FileNotFoundError:
            continue
        ts = fileInfo.st_mtime
        timeArr = time.localtime(ts)
        date = time.strftime("%Y-%m-%d", timeArr)
        if current != date:
            os.remove(fileName)


def filteHTML(string):
    content = remove_comments(string)  # 过滤注释
    content = html.unescape(content)  # 去掉实体字符
    content = content.replace('&ensp;', '')
    content = content.replace('&emsp;', '')
    content = content.replace('&nbsp;', '')

    return content


# 过滤时间的字符串
def getTime(dateTime):
    t = dateTime.replace('[', '')
    t = t.replace(']', '')

    if '年' in dateTime or '月' in dateTime or '日' in dateTime:
        t = t.replace('年', '-')
        t = t.replace('月', '-')
        t = t.replace('日', '')

    if '发布时间：' in dateTime:
        t = t.replace('发布时间：', '')

    if '.' in dateTime:
        t = t.replace('.', '-')

    return t


def ip2num(ip):
    return socket.ntohl(struct.unpack("I", socket.inet_aton(str(ip)))[0])


def write_file(filename, page_source, ifdisplay = 0):
    # 写文件
    try:
        f = open(filename, 'w')  # 若是'wb'就表示写二进制文件
    except:
        return 0
    else:
        f.write(page_source)
        f.close()
        if 1 == ifdisplay:
            print(filename, ' write ok')
        return 1


def get_timestamp(ifmillisecond = 0):
    tm = time.time()
    tm_s = int(tm)
    if 1 == ifmillisecond:
        tm_millisecond = int(tm * 1000) % 1000
        return tm_s, tm_millisecond
    else:
        return tm_s



def mkdir(dir):
	try:
		os.mkdir(dir)
	except:
		return 0
	else:
		return 1
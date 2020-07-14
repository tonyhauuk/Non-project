# -*- coding=utf-8 -*- #

import pysnooper
import urllib.request
import re
import hashlib
import xlwt
import time
import os
from bs4 import BeautifulSoup
from user import User


class Crawler:
    def __init__(self, basePath):
        self.nameList = list()
        self.webList = list()
        self.path = basePath
        self.webList = self.getData(self.path + 'website.txt')
        self.nameList = self.getData(self.path + 'nameList.txt')

    def getData(self, path):
        dataList = list()
        with open(path, 'r') as f:
            for line in f.readlines():
                dataList.append(line.replace('\n', ''))

        return dataList

    def doJob(self):
        md5Codes = self.getMd5()
        md = list()

        for url in self.webList:
            try:
                string = urllib.request.urlopen(url, timeout = 5).read()
            except Exception:
                continue

            a = self.split(string)
            if len(a) <= 0:
                continue

            for name in self.nameList:
                for link in a:
                    try:
                        title = ''.join(link.get_text().split())
                        title.index(name)
                    except ValueError:
                        continue

                    urls = self.checkUrl(link, url)
                    if urls is None or urls == None:
                        urls = ''

                    md5 = self.encrypMd5(urls)
                    if len(md5Codes) > 0:
                        for code in md5Codes:
                            if code != md5:
                                user = User(url, name, urls, title, md5)
                                md.append(md5)
                                self.generateFile(user)
                    else:
                        user = User(url, name, urls, title, md5)
                        md.append(md5)
                        self.generateFile(user)
        count = len(md)
        if count > 0:
            self.appendMd5(md)
            self.createExcel()
        else:
            self.createEmptyExcel()

        return count

    def split(self, string):
        clear = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)
        try:
            s = str(string, encoding = 'gbk')
        except UnicodeDecodeError:
            s = str(string, encoding = 'utf-8')

        s = clear.sub('', s)
        soup = BeautifulSoup(s, 'html.parser')
        a = soup.find_all('a')

        return a

    def encrypMd5(self, string):
        md5 = hashlib.md5()
        b = string.encode(encoding = 'utf-8')
        md5.update(b)
        stringMd5 = md5.hexdigest()

        return stringMd5

    def getMd5(self):
        dataList = list()
        path = self.path + 'md5.txt'
        with open(path, 'r', encoding = 'utf-8') as f:
            for line in f.readlines():
                dataList.append(line.replace('\n', ''))

        return dataList

    def generateFile(self, user):
        path = self.path + 'list.csv'
        with open(path, 'a') as f:
            f.write(user.webname + ', ' + user.username + ', ' + user.link + ', ' + user.title)
            f.write('\r')

    def appendMd5(self, codes):
        path = self.path + 'md5.txt'
        with open(path, 'a') as f:
            for md5 in codes:
                f.write(md5)
                f.write('\r')

    def checkUrl(self, link, website):
        currentUrl = link.get('href')
        if 'http' in currentUrl:
            url = currentUrl
        else:
            if '/' == currentUrl[0]:
                url = website + currentUrl
            else:
                url = website + '/' + currentUrl

        return url

    def createExcel(self):
        i = 0
        path = self.path + 'list.csv'
        wb = xlwt.Workbook(encoding = 'ascii')
        sheet = wb.add_sheet('list')

        font = xlwt.Font()
        font.name = 'Courier New'
        font.height = 260

        style = xlwt.XFStyle()
        style.font = font

        with open(path, 'r') as f:
            for line in f.readlines():
                string = line.split(',')
                link = 'HYPERLINK("%s";"%s")' % (string[2], string[2])
                sheet.write(i, 0, string[0], style)
                sheet.write(i, 1, string[1], style)
                sheet.write(i, 2, xlwt.Formula(link))
                sheet.write(i, 3, string[3], style)
                i += 1

        fileName = time.strftime("%Y-%m-%d", time.localtime())
        wb.save(self.path + 'excel/' + fileName + '.xls')
        os.remove(path)

    def createEmptyExcel(self):
        wb = xlwt.Workbook()
        fileName = time.strftime("%Y-%m-%d", time.localtime())
        sheet = wb.add_sheet('empty')
        sheet.write(0, 0, '')
        wb.save(self.path + 'excel/' + fileName + '.xls')

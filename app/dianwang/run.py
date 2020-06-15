# -*- coding=utf-8 -*- #

from crawler import Crawler
import time, os
from apscheduler.schedulers.blocking import BlockingScheduler


def initDict():
    d = {}
    file = './md5.txt'
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


def deleteFiles():
    filePath = '/root/estar_save/'
    timeStamp = time.time()
    timeArray = time.localtime(timeStamp)
    current = time.strftime("%Y-%m-%d", timeArray)
    name = os.listdir(filePath)

    for i in name:
        try:
            fileInfo = os.stat(filePath + i)
        except FileNotFoundError:
            continue
        timeStamp = fileInfo.st_mtime
        timeArray = time.localtime(timeStamp)
        date = time.strftime("%Y-%m-%d", timeArray)
        if current != date:
            os.remove(filePath + i)


def crawl(d):
    c = Crawler(d)
    c.doJob()


if __name__ == '__main__':
    crawlItrv = 60 * 10
    deleteItrv = 60 * 60
    d = initDict()

    scheduler = BlockingScheduler()

    scheduler.add_job(crawl, 'interval', seconds = crawlItrv, id = 'crawl', args = [d])
    scheduler.add_job(deleteFiles, 'interval', seconds = deleteItrv, id = 'deleteFiles')

    scheduler.start()

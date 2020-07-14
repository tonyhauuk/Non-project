# coding: utf-8

from crawler import Crawler
import time, os, datetime, json
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
            fileName = filePath + i
            fileInfo = os.stat(fileName)
        except FileNotFoundError:
            continue
        ts = fileInfo.st_mtime
        timeArr = time.localtime(ts)
        date = time.strftime("%Y-%m-%d", timeArr)
        if current != date:
            os.remove(fileName)


def crawl(d):
    c = Crawler(d)
    c.doJob()


if __name__ == '__main__':
    crawl({})
    # d = initDict()
    #
    # scheduler = BlockingScheduler()
    #
    # scheduler.add_job(crawl, 'interval', minutes = 10, id = 'crawl', args = [d])
    # scheduler.add_job(deleteFiles, 'cron', day_of_week = 'mon-fri', hour = 5, id = 'deleteFiles')
    #
    # try:
    #     scheduler.start()
    # except (KeyboardInterrupt, SystemError):
    #     scheduler.shutdown(wait = False)

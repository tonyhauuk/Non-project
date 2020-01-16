import threading, time
from datetime import datetime, date, timedelta
import datetime, os

from baijiahao import Baijiahao


# 写入dict记录
def writeDict():
    try:
        threads = []
        t1 = threading.Thread(target=deleteExpire, args=())
        threads.append(t1)
        threads[0].setDaemon(True)
        threads[0].start()
        threads[0].join()
    except Exception as e:
        print('write dict file error: ', e)


# 删除过期记录
def deleteExpire():
    now = datetime.datetime.now()
    nextTime = now + datetime.timedelta(days=1)
    nextYear = nextTime.date().year
    nextMonth = nextTime.date().month
    nextDay = nextTime.date().day
    # 时间设置成凌晨3点，这个时间段信息相对来说比较少，更新文件冲突较少
    nextDayTime = datetime.datetime.strptime(str(nextYear) + '-' + str(nextMonth) + '-' + str(nextDay) + ' 03:00:00', '%Y-%m-%d %H:%M:%S')
    timerStartTime = (nextDayTime - now).total_seconds()
    timer = threading.Timer(timerStartTime, expire)
    timer.start()


# 内存字典：每天凌晨3点执行这个程序，程序检查文件当中的过期数据
def expire():
    d1 = Baijiahao.returnDict()

    dictList = [d1]

    current = int(time.time())
    for i in dictList:
        # 检查过期数据
        li = []
        fileName = ''

        day = 60 * 60 * 24
        for k, v in dictList[i].items():
            if current - int(v) > day:  # 如果时间戳的差大于1天的秒数，就删除
                li.append(k)

        # 删除字典里过期的数据
        for i in li:
            dictList[i].pop(i)

        # 更新txt文件
        try:
            className = dictList[i].__class__.__name__
            if 'baijiahao' in className.lower():
                fileName = './record/baijiahao.txt'
            elif 'toutiao' in className.lower():
                fileName = './record/toutiao.txt'

            os.remove(fileName)
            with open(fileName, 'a+') as f:
                f.write(str(dictList[i]))
        except:
            pass

    end = int(time.time()) - current
    interval = 86400 - end  # 下一次间隔多久来执行这个程序，每次的执行时间不固定，所以得用总时间来减去当前所用的时间，得出的差就是执行下次一次需要的秒数
    timer = threading.Timer(interval, expire)
    timer.start()


if __name__ == '__main__':
    try:
        writeDict()
    except Exception as e:
        print(e)

    # command:   nohup python3 persistence.py > dictData.file 2>&1 &
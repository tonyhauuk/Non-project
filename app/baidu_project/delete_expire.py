import threading
import datetime
import time
import os

def deleteExpire():
    now = datetime.datetime.now()
    nextTime = now + datetime.timedelta(days = +1)
    nextYear = nextTime.date().year
    nextMonth = nextTime.date().month
    nextDay = nextTime.date().day
    # 时间设置成凌晨3点，这个时间段信息相对来说比较少，更新文件冲突较少
    nextDayTime = datetime.datetime.strptime(str(nextYear) + '-' + str(nextMonth) + '-' + str(nextDay) + ' 03:00:00', '%Y-%m-%d %H:%M:%S')
    timerStartTime = (nextDayTime - now).total_seconds()
    timer = threading.Timer(timerStartTime, expire)
    timer.start()


# 每天凌晨3点执行这个程序，程序检查baijiahao.txt文件里面的国企记录
def expire():
    try:
        lst = list()
        current = int(time.time())
        # 读取当前的文件
        with open('./record/baijiahao.txt', mode = 'r') as f:
            lines = f.readlines()
            day = 60 * 60 * 24
            if len(lines) > 0:
                for line in lines:
                    t = int(line.split('_')[0])
                    if current - t < day:  # 判断如果时间在一天之内，加入到数组中
                        lst.append(line)

        # 写一个新的文件，记录的都是删除过期记录的信息
        with open('./record/tmp_baijiahao.txt', mode = 'a+', encoding = 'utf-8') as f:
            for text in lst:
                f.write(text)

        # 删除旧文件，把tmp文件名修改成刚才删除文件的名称
        os.remove('./record/baijiahao.txt')
        os.rename('./record/tmp_baijiahao.txt', './record/baijiahao.txt')

        end = int(time.time()) - current
        interval = 86400 - end  # 下一次间隔多久来执行这个程序，每次的执行时间不固定，所以得用总时间来减去当前所用的时间，得出的差就是执行下次一次需要的秒数
        timer = threading.Timer(interval, expire)
        timer.start()
    except:
        pass

deleteExpire()
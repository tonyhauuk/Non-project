# -*- coding: utf-8 -*-

import os
import threading
import datetime
from time import sleep
from subprocess import call


def restart():
    frequency = 20 * 60  # minute * second
    i, j = 0, 0
    fileSize = checkSize()
    while i <= frequency:
        if fileSize == checkSize():
            j += 1
        else:
            j = 0
        if j == 480:
            call('sh ./goserver.sh', shell = True)
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print('restart... ' + '\n')
            break
        i += 1
        sleep(1)

    interval = 86400 - i
    timer = threading.Timer(interval, restart)
    timer.start()




now = datetime.datetime.now()
nextTime = now + datetime.timedelta(days = +1)
nextYear = nextTime.date().year
nextMonth = nextTime.date().month
nextDay = nextTime.date().day

nextDayTime = datetime.datetime.strptime(str(nextYear) + '-' + str(nextMonth) + '-' + str(nextDay) + ' 03:00:00', '%Y-%m-%d %H:%M:%S')
timerStartTime = (nextDayTime - now).total_seconds()

print(timerStartTime)
print('\t')
print(nextDayTime)

# timer = threading.Timer(timerStartTime, restart)
# timer.start()

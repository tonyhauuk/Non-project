from crawler import Crawler
from send_email import SendEmail
import time
import threading
import datetime


def sendEmail():
    start = int(time.time())

    path = r''
    receiver1 = ['xxxxxxxxxxx', 'xxxxxxxxxxxx', 'xxxxxxxxxx']

    c = Crawler(path)
    count = c.doJob()

    send = SendEmail()
    send.getInstanse(receiver1, count)

    i = int(time.time()) - start

    interval = 86400 - i
    timer = threading.Timer(interval, sendEmail)
    timer.start()


timeStr = 14
now = datetime.datetime.now()
nextTime = now + datetime.timedelta(days = +1)
nextYear = nextTime.date().year
nextMonth = nextTime.date().month
nextDay = nextTime.date().day

nextDayTime = datetime.datetime.strptime(str(nextYear) + '-' + str(nextMonth) + '-' + str(nextDay) + ' ' + str(timeStr) + ':00:00', '%Y-%m-%d %H:%M:%S')
timerStartTime = (nextDayTime - now).total_seconds()

print(timerStartTime)
print(nextDayTime)

timer = threading.Timer(timerStartTime, sendEmail)
timer.start()
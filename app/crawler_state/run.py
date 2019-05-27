from crawler import Crawler
from send_email import SendEmail

path = './'
c = Crawler(path)
count = c.doJob()
print('count: ' + str(count))
# send = SendEmail()
# send.getInstanse()

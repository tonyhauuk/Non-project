import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from smtplib import SMTPException
import time


class SendEmail():
    def getInstanse(self, recv, count):
        host = 'smtp.mxhichina.com'
        user = ''       # sender email
        password = ''   # password
        port = 465  # SSL port

        sender = '' # sender email
        receiver = recv

        content = time.strftime("%Y-%m-%d", time.localtime())
        text = content + ' ' + str(count) + '篇统计'

        msg = MIMEMultipart()
        msg['From'] = Header(sender, 'UTF-8')
        msg['To'] = Header(','.join(receiver), 'UTF-8')
        subject = '五矿统计'
        msg['Subject'] = Header(subject, 'UTF-8')
        msg.attach(MIMEText(text, 'plain', 'UTF-8'))

        filePath = r'/' + content + '.xls'
        attachment = MIMEText(open(filePath, 'rb').read(), 'base64', 'UTF-8')
        attachment['Content-Type'] = 'application/octet-stream'
        attachment['Content-Disposition'] = 'attachment; filename="' + content + '.xls' + '"'
        msg.attach(attachment)

        client = smtplib.SMTP_SSL(host, port)
        try:
            # client = smtplib.SMTP()
            # client.connect(host, port)
            client.login(user, password)
            client.sendmail(sender, receiver, msg.as_string())
        except SMTPException as e:
            print('Exception: ' + str(e))
        finally:
            client.quit()

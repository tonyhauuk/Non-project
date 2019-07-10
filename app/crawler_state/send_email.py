import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from smtplib import SMTPException
import time

class SendEmail():
    def getInstanse(self):
        host = 'smtp.mxhichina.com'
        user = ''               # email
        password = ''           # password
        port = 465

        sender = ''             # sender email
        receiver = ''           # receiver email

        content = time.strftime("%Y-%m-%d", time.localtime())

        msg = MIMEMultipart()
        msg['From'] = Header(sender, 'UTF-8')
        msg['To'] = Header(receiver, 'UTF-8')
        subject = '五矿统计'
        msg['Subject'] = Header(subject, 'UTF-8')
        msg.attach(MIMEText(content, 'plain', 'UTF-8'))

        filePath = './' + content + '.xls'
        attachment = MIMEText(open(filePath, 'rb').read(), 'base64', 'UTF-8')
        attachment['Content-Type'] = 'application/octet-stream'
        attachment['Content-Disposition'] = 'attachment; filename="' + filePath +'"'
        msg.attach(attachment)

        try:
            client = smtplib.SMTP_SSL(host, port)
            # client = smtplib.SMTP()
            # client.connect(host, port)
            client.login(user, password)
            client.sendmail(sender, receiver, msg.as_string())
            client.quit()
        except SMTPException as e:
           print('Exception: ' + str(e))

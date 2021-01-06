import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from smtplib import SMTPException
import time


class SendEmail():
    def getInstanse1(self):
        host = 'smtp.mxhichina.com'
        user = 'wangxiao@estarinfo.net'
        password = '800915aAa'
        port = 465  # SSL port

        sender = 'wangxiao@estarinfo.net'
        receiver = '595292945@qq.com'

        content = time.strftime("%Y-%m-%d", time.localtime())
        text = content + ' ' + ' 测试邮件，smtps 465端口'

        msg = MIMEMultipart()
        msg['From'] = Header(sender, 'UTF-8')
        msg['To'] = Header(','.join(receiver), 'UTF-8')
        subject = '测试邮件'
        msg['Subject'] = Header(subject, 'UTF-8')
        msg.attach(MIMEText(text, 'plain', 'UTF-8'))

        # filePath = r'/home/web_dev/tools/crawl_state-owned/excel/' + content + '.xls'
        # attachment = MIMEText(open(filePath, 'rb').read(), 'base64', 'UTF-8')
        # attachment['Content-Type'] = 'application/octet-stream'
        # attachment['Content-Disposition'] = 'attachment; filename="' + content + '.xls' + '"'
        # msg.attach(attachment)

        client = smtplib.SMTP_SSL(host, port)
        try:
            '''
                Use 25 port             
            client = smtplib.SMTP()
            client.connect(host, port)
            '''
            client.login(user, password)
            client.sendmail(sender, receiver, msg.as_string())
        except SMTPException as e:
            print('Exception: ', e)
        finally:
            client.quit()


    def getInstanse2(self):
        host = 'mail4.estar360.com'
        user = 'estar@estar360.com'
        password = '123456'
        port = 465  # SSL port

        sender = 'estar@estar360.com'
        receiver = '595292945@qq.com'

        content = time.strftime("%Y-%m-%d", time.localtime())
        text = content + ' ' + ' 测试邮件，smtps 465端口'

        msg = MIMEMultipart()
        msg['From'] = Header(sender, 'UTF-8')
        msg['To'] = Header(','.join(receiver), 'UTF-8')
        subject = '测试邮件'
        msg['Subject'] = Header(subject, 'UTF-8')
        msg.attach(MIMEText(text, 'plain', 'UTF-8'))

        # filePath = r'/home/web_dev/tools/crawl_state-owned/excel/' + content + '.xls'
        # attachment = MIMEText(open(filePath, 'rb').read(), 'base64', 'UTF-8')
        # attachment['Content-Type'] = 'application/octet-stream'
        # attachment['Content-Disposition'] = 'attachment; filename="' + content + '.xls' + '"'
        # msg.attach(attachment)

        client = smtplib.SMTP_SSL(host, port)
        try:
            '''
                Use 25 port             
            client = smtplib.SMTP()
            client.connect(host, port)
            '''
            client.login(user, password)
            client.sendmail(sender, receiver, msg.as_string())
        except SMTPException as e:
            print('Exception: ', e)
        finally:
            client.quit()



if __name__ == '__main__':
    send = SendEmail()
    send.getInstanse2()
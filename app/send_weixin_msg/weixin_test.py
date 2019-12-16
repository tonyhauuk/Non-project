import sys

sys.path.append('./weworkapi_python/api/src')

from CorpApi import *


class Weixin:
    def __init__(self):
        self.corpid = 'wxece8093f497e1c76'
        self.corpsecret = 'MS5fDIeNc5aPa_BCnuGDAwtWh55TAurD9tAbVcPt8YnzZ8SJLkkvqiK_WYalAZYA'
        self.appsecret = 'Y-20mJQQAvpefDfPHeF_jP27sAlowq-T2WRWpinHqek'

    def weixinInfo(self):
        touser = 'wangxiao@estarinfo.net|zran@estarinfo.net'
        content = 'Send weixin message via Python api'
        title = 'python test'
        msgtype = 'news'
        agentid = 0
        articles = list()
        a = dict(title = title, description = content, url = 'http://www.qq.com', picurl = 'http://res.mail.qq.com/node/ww/wwopenmng/images/independent/doc/test_pic_msg1.png')
        articles.append(a)

        news = dict(articles = articles)
        jsonStr = dict(touser = touser, msgtype = msgtype, agentid = agentid, news = news)

        self.weixin_alarm(jsonStr)

    def weixin_alarm(self, jsonObj):
        api = CorpApi(self.corpid, self.appsecret)
        try:
            response = api.httpCall(CORP_API_TYPE['MESSAGE_SEND'], jsonObj)
            print(response)
        except ApiException as e:
            print(e.errCode, e.errMsg)


if __name__ == '__main__':
    w = Weixin()
    w.weixinInfo()

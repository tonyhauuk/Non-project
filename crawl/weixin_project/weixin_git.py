import wechatsogou, json

# 可配置参数

# 直连
wx = wechatsogou.WechatSogouAPI()

# 验证码输入错误的重试次数，默认为1
# wx = wechatsogou.WechatSogouAPI(captcha_break_time = 3)

# # 所有requests库的参数都能在这用
# # 如 配置代理，代理列表中至少需包含1个 HTTPS 协议的代理, 并确保代理可用
# wx = wechatsogou.WechatSogouAPI(proxies = {
#     "http": "127.0.0.1:8888",
#     "https": "127.0.0.1:8888",
# })
#
# # 如 设置超时
# wx = wechatsogou.WechatSogouAPI(timeout = 0.1)
r0 = wx.search_article('intel')
r1 = wx.get_gzh_article_by_history('茅台')

# j = json.loads(r1)
print(r0)
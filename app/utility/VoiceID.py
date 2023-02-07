# pip3 install browsermob-proxy

# You need to start browser proxy and configure the proxy in chrome option of chrome driver,

from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time, json, pprint

server = Server('D:\\PyProject\\Non-project\\app\\utility\\browsermob-proxy-2.1.4\\bin\\browsermob-proxy.bat')
server.start()
proxy = server.create_proxy()


# Configure the browser proxy in chrome options
# options = webdriver.FirefoxOptions()
options = Options()
options.add_argument('--proxy-server={0}'.format(proxy.proxy))
options.add_argument('ignore-certificate-errors')
# browser = webdriver.Firefox(options = options)
browser = webdriver.Chrome(options = options)
browser.set_window_position(x = 630, y = 0)

#tag the har(network logs) with a name

proxy.new_har('', options = {'captureContent': True, 'captureHeaders': True})

# Then you can navigate to page using selenium

browser.get('https://mp.weixin.qq.com/mp/audio?_wxindex_=0&scene=104&__biz=MzA4NTE5MTk5NQ==&mid=2247485018&idx=1&voice_id=MzA4NTE5MTk5NV8yMjQ3NDg1MDE3&sn=2d76154c25fb94b55e8e631748a13c84')
time.sleep(2)
browser.find_element(By.CSS_SELECTOR, 'span#voice_play > em.weui-wa-hotarea.weui-audio-btn').click()
time.sleep(3)
browser.find_element(By.CSS_SELECTOR, 'span#voice_play > em.weui-wa-hotarea.weui-audio-btn').click()

# After navigation, you can get the network logs in json format from the proxy

# print(proxy.har) # returns a Network logs (HAR) as JSON
# pprint.pprint(proxy.har)

for entry in proxy.har['log']['entries']:
    url = entry['request']['url']
    if 'getvoice?mediaid' in url:
        print('Url:', url)


# Also before quitting the driver, stop the proxy server as well at the end,
server.stop()
browser.quit()
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import json

enable = True
i = 0
while enable:
    i += 1
    print(i)
    if i == 5:
        enable = False
        print('process break')

exit()
profile = webdriver.FirefoxProfile()
profile.set_preference('browser.privatebrowsing.autostart', True)
browser = webdriver.Firefox(firefox_profile = profile)

browser.get("http://www.baidu.com")

ActionChains(browser).key_down(Keys.COMMAND).send_keys('t').key_up(Keys.COMMAND).perform()

from time import sleep

sleep(5)
browser.quit()
print('close')

'''


info = dict()
for i in range(5):
    multi = dict(a = 'sss', b = 'aaaa', c = i)
    info.update(multi)

print(info)




def getDigit(text):
    try:
        number = int(re.sub('\D', '', text))
    except ValueError:
        number = 0

    return number


a = ''
forwardNumber = 0 if a.isalnum() or a.isdigit() else getDigit(a)
print('转发： ')
print(forwardNumber)

b = '评论 1d000'
comment = 0 if b.isalnum() else getDigit(b)
print('评论： ')
print(comment)
'''

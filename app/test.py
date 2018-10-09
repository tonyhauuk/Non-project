from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import json, time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException






i = 1
t = True
while True:
    if i == 5:
        break
    print('i: ' + str(i))
    i += 1




exit()
a = dict(a = 'dddd', b='22222')
b = dict(error = 0, data = a)
c = True
i = 0
t = time.time()
while c:
    # a.popitem()
    i += 1
    print(i)

    if i == 100:
        c = False

print('----------------------')
print(time.time() - t)

# jsonObj = json.dumps(b, ensure_ascii = False, indent = 4, separators = (',', ': '))
# print(jsonObj)











def isOneDay(date):
    array = time.strptime(date, '%Y年%m月%d日 %H:%M')
    st = time.mktime(array)
    oneDay = 24 * 60 * 60
    diff = int(time.time()) - int(st)
    print(diff)
    if diff < oneDay:
        return True
    else:
        return False

print(type(isOneDay('2018年10月29日 21:25')))


import datetime, time
y = datetime.datetime.now().year
m = datetime.datetime.now().month
d = datetime.datetime.now().day

t = time.time()
n = 9
st = n * 60
real = int(t) - st

local =  time.localtime(real)
dt = time.strftime('%Y年%m月%d日 %H:%M', local)
print(dt)






profile = webdriver.FirefoxProfile()
profile.set_preference('browser.privatebrowsing.autostart', True)
browser = webdriver.Firefox(firefox_profile = profile)

try:
    browser.get("https://s.weibo.com/weibo?q=intel")
    feedList = browser.find_element_by_css_selector('div.m-wrap div#pl_feedlist_index')
    blocks = feedList.find_elements_by_css_selector('div div.card-wrap')

    info = dict()

    for detail in blocks:
        try:
            mid = detail.get_attribute('mid')
            if not mid:
                continue
        except NoSuchAttributeException:
            continue
        else:
            nickname  = ''
            try:
                # allClick = WebDriverWait(browser, 1).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'p.txt a[action-type="fl_unfold"]')))
                allClick = browser.find_elements_by_css_selector('p.txt a[action-type="fl_unfold"]')
                for more in allClick:

                    more.click()

                profile = detail.find_element_by_css_selector('div.content div.info')
                nickname = profile.find_element_by_css_selector('a.name').text


            except:
                content=''

            try:
                profile = detail.find_element_by_css_selector('div.content div.info')
                nickname = profile.find_element_by_css_selector('a.name').text

                text = detail.find_element_by_css_selector('div.content p[node-type="feed_list_content_full"]')

                content = text.text
            except NoSuchElementException:
                try:
                    text = detail.find_element_by_css_selector('div.content p[node-type="feed_list_content"]')

                    content = text.text
                except NoSuchElementException:
                    try:
                        # txt = detail.find_elements_by_css_selector('div.content p.txt')
                        # text = txt[0]
                        text = detail.find_element_by_css_selector('div.content p.txt')
                        # text = detail.find_element_by_css_selector('div.content p[nick-name="' + nickname + '"]')
                        # if text.get_attribute('nick-name') == nickname:
                        content = text.text
                    except NoSuchElementException:
                        try:
                            txt = detail.find_elements_by_css_selector('div.content p[nick-name="' +nickname + '"]')
                            text = txt[0]
                            content = text.text
                        except NoSuchElementException:
                            pass

            if content != '':
                t = content
            else:
                t = 'NullNullNullNullNullNullNullNullNullNullNullNull'
            print(nickname+'  :  '+t)
except:
    pass
finally:
    browser.quit()



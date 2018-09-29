from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException



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


exit()



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



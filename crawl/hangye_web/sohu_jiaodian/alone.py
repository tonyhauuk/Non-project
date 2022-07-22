# coding: utf-8
from crawlerfun import ClearCache
import time, os, datetime, subprocess
from selenium import webdriver
from selenium.webdriver.opera.options import Options as operaOptions

from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

from liuyan_people import Liuyan_people
from direct_qq import Qie
from jinzhai_anwser_gov import JinZhai_a_gov
from mpsohu import MpSohu




def rename():
    try:
        root = '/estar/newhuike2/1/'
        lst = os.listdir(root)
        for l in lst:
            if '_' in l:
                os.rename(root + l, root + l.strip('_'))
    except:
        pass


def clean(browser):
    subprocess.Popen('rm -rf /dev/shm/cache', shell = True, stdout = subprocess.PIPE)
    subprocess.Popen('rm nohup.out -rf', shell = True, stdout = subprocess.PIPE)
    subprocess.Popen('tmpwatch 1 /tmp/', shell = True, stdout = subprocess.PIPE)
    ClearCache(browser)


def startBrowser():
    # options = webdriver.ChromeOptions()
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-gpu')
    # options.add_argument('--disable-logging')
    # options.add_argument('--disable-infobars')
    # options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.103 Safari/537.36"')
    # options.add_argument('--disk-cache-dir=%s' % '/dev/shm/cache')
    # browser = webdriver.Chrome(chrome_options = options)
    # browser.set_window_size(1050, 685)
    # browser.set_window_position(x = 225, y = 0)
    # clean(browser)

    # options = operaOptions()
    # options.binary_location = '/usr/lib64/opera/opera'
    # options.add_argument('--disable-gpu')
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-dev-shm-usage')
    # options.add_argument('--disable-logging')
    # options.add_argument('--disable-plugins')
    # options.add_argument('--disable-java')
    # browser = webdriver.Opera(options = options, executable_path = '/usr/bin/operadriver')
    # browser.set_window_size(1200, 685)
    # browser.set_window_position(x = 150, y = 0)

    # options = webdriver.ChromeOptions()
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-gpu')
    # options.add_argument('--disable-logging')
    # options.add_argument('--disable-infobars')
    # options.add_argument('--disable-extensions')
    # options.add_argument('--ignore-certificate-errors-spki-list')
    # options.add_experimental_option('debuggerAddress', '127.0.0.1:8080')
    #
    # browser = webdriver.Chrome(options = options)
    # browser.set_window_size(1150, 690)
    # browser.set_window_position(x = 200, y = 0)
    #
    # clean(browser)

    # Start a Firefox via Remote command prompt
    options = Options()
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-logging')
    options.add_argument('--disable-plugins')
    options.add_argument('--disable-java')
    options.set_preference("javascript.enabled", False)
    # options.add_experimental_option('debuggerAddress', '127.0.0.1:8080')
    # options.add_experimental_option('javascript.enabled', False)

    browser = webdriver.Firefox(options = options)
    browser.set_window_size(1200, 685)
    browser.set_window_position(x = 150, y = 0)

    return browser






def loopCrawl():
    while True:
        browser = startBrowser()
        try:
            # l = Liuyan_people(browser)  # 人民网-留言
            # l.crawl()
            #
            # q = Qie(browser)            # 腾讯号
            # q.crawl()
            #
            # j = JinZhai_a_gov(browser)  # 金寨县县长信箱
            # j.crawl()

            m = MpSohu(browser)
            m.crawl()

        except Exception as e:
            print(e)
            continue
        finally:
            # browser.quit()
            time.sleep(60)


if __name__ == '__main__':
    rename()
    loopCrawl()

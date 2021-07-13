# -*- coding: utf-8 -*-

import time, hashlib, os, datetime
from time import sleep
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Bjd:
    def __init__(self):
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        self.date = time.strftime('%Y-%m-%d', timeArray)
        self.d = {}
        self.dir = self._dir = ''
        self.debug = True
        self.browser = webdriver.Firefox()
        self.browser.set_window_position(x = 600, y = 0)


    def crawl(self):
        webLst = ['https://bjrbdzb.bjd.com.cn/bjrb/paperindex.htm',
                  'https://bjrbdzb.bjd.com.cn/bjwb/paperindex.htm',
                  'https://bjrbdzb.bjd.com.cn/fzxb/paperindex.htm']

        for url in webLst[1:]:
            self.i = 0
            try:
                self.browser.get(url)
                sleep(1)
            except TimeoutException:
                return

            self.browser.find_element_by_css_selector('li > a.b_list').click()
            loop = self.browser.find_elements_by_css_selector('ul#picList > li')    # 计算翻页的次数
            self.browser.find_element_by_css_selector('div.over-layer.over-layer-bm').click()   # 再点回去
            length = len(loop)
            sleep(1)

            for i in range(length):
                self.browser.find_element_by_link_text('目录').click()        # 点击目录，出现下拉条
                block = self.browser.find_elements_by_css_selector('div.nav-items')[i]
                itemList = block.find_elements_by_css_selector('ul.nav-list-group > li')  # 取第几页的下拉条

                if len(itemList) > 0:
                    for j in range(len(itemList)):      # 循环item list，每一页的条数
                        blocks = self.browser.find_elements_by_css_selector('div.nav-items')[i]
                        item = blocks.find_elements_by_css_selector('ul.nav-list-group > li')[j]
                        link = item.find_element_by_tag_name('a').get_attribute('data-href')

                        md5 = self.makeMD5(link)
                        if md5 in self.d:
                            break
                        else:
                            self.d[md5] = self.date.split(' ')[0]  # 往dict里插入记录
                            self.i += 1
                            self.extract(item)

                            if j < len(itemList) - 1:
                                self.browser.find_element_by_link_text('目录').click()
                else:
                    sleep(1)
                    self.browser.find_element_by_link_text('目录').click()


                self.browser.find_element_by_partial_link_text('下一版').click()

    # 提取信息，一条的
    def extract(self, info):
        title = info.find_element_by_tag_name('a').text
        info.find_element_by_tag_name('a').click()

        sleep(1)  # 等个几秒钟
        self.source, url = self.getPageText()  # 拿到网页源码
        print(url, title)
        # self.write_new_file(url, title, self.source, self.i, self.date, 414705)
        self.browser.back()


    # 生成md5信息
    def makeMD5(self, title):
        m = hashlib.md5()
        b = title.encode(encoding = 'utf-8')
        m.update(b)
        enc = m.hexdigest()

        return enc

    def getPageText(self):
        url = self.browser.current_url
        try:
            content = self.browser.find_element_by_css_selector('div#content').get_attribute('innerHTML')
        except NoSuchElementException:
            content = self.browser.page_source

        return content, url

if __name__ == '__main__':
    c = Bjd()
    c.crawl()
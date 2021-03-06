import time, os, hashlib
from time import sleep
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver


class Nfncb:
    def __init__(self, d):
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        self.date = time.strftime('%Y-%m-%d', timeArray)
        self.d = d
        self.dir = self._dir = ''
        self.debug = True


    def crawl(self):
        self.browser = webdriver.Firefox()
        self.browser.set_window_position(x = 650, y = 0)

        file = 'weblist.txt'
        with open(file, mode = 'r') as f:
            url = f.readlines()
            for x in url:
                self.doCrawl(x)


    def doCrawl(self, url):
        self.total = 0
        try:
            self.browser.get(url)
        except TimeoutException:
            return 'interrupt', 'none', 'error'

        while True:
            newsList = self.browser.find_elements_by_css_selector('div.ul_lists > ul > li')
            for item in newsList:
                dateTime = item.find_elements_by_css_selector('div.li_right > p.li_message > span')[1].text
                if dateTime in self.date:
                    self.extract(item, dateTime)
                else:
                    break

            if self.total < len(newsList):  # 如果当前抓取的数量小于页面展示的数量，就不往下滚动
                break
            else:
                self.browser.find_element_by_xpath('/html/body').send_keys(Keys.END)
                sleep(2)
        #
        # if self.total > 0:
        #     # self.rename()
        #     # self.expire()
        #
        #     return 'complete', str(self.total), 'ok'


    # 提取信息，一条的
    def extract(self, item, dateTime):
        titleInfo = item.find_element_by_css_selector('p.li_title > a')

        try:
            href = titleInfo.get_attribute('href')
            md5 = self.makeMD5(href)

            # dict filter
            if md5 in self.d:
                return
            else:
                self.d[md5] = dateTime  # 往dict里插入记录
                self.total += 1

            title = titleInfo.text

            handle = self.browser.current_window_handle  # 拿到当前页面的handle
            titleInfo.click()

            # switch tab window
            WebDriverWait(self.browser, 10).until(EC.number_of_windows_to_be(2))
            handles = self.browser.window_handles
            for newHandle in handles:
                if newHandle != handle:
                    self.browser.switch_to.window(newHandle)    # 切换到新标签
                    sleep(1)                                    # 等个几秒钟
                    self.source = self.getPageText()            # 拿到网页源码
                    self.browser.close()                        # 关闭当前标签页
                    self.browser.switch_to.window(handle)       # 切换到之前的标签页
                    break

            # self.write_new_file(href, title, self.source, self.i, self.date)
        except (NoSuchElementException, NoSuchAttributeException) as e:
            print('Element error:', e)
        except Exception:
            pass


    def getPageText(self):  # 获取网页正文
        html = self.browser.find_element_by_css_selector('div.main_content > div.news_detail').get_attribute('innerHTML')

        return html


    # 生成md5信息
    def makeMD5(self, title):
        m = hashlib.md5()
        b = title.encode(encoding = 'utf-8')
        m.update(b)
        enc = m.hexdigest()

        return enc


    # 删除过期的记录
    def expire(self):
        # 检查过期数据
        li = []
        current = self.date.split(' ')[0]
        for k, v in self.d.items():
            if current != v:
                li.append(k)

        # 删除字典里过期的数据
        for i in li:
            self.d.pop(i)

        # 更新txt文件
        try:
            fileName = '/home/zran/src/crawler/33/manzhua/crawlpy3/record/nfncb_md5.txt'
            os.remove(fileName)
            with open(fileName, 'a+') as f:
                f.write(str(self.d))
        except Exception as e:
            print(e)


    # 重新修改文件夹名称
    def rename(self):
        try:
            root = '/estar/newhuike2/1/'
            lst = os.listdir(root)
            for l in lst:
                if '_' in l:
                    os.rename(root + l, root + l.strip('_'))
        except:
            pass


if __name__ == '__main__':
    n = Nfncb({})
    n.crawl()
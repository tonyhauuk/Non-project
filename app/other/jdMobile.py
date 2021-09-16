# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time

class JDMobile:
    def __init__(self):
        pass


    def crawl(self):
        self.i = self.total = 0
        self.browser = webdriver.Firefox()
        self.browser.set_window_position(x = 630, y = 0)
        record = ''

        try:
            url = 'https://reselleve.jd.com/zslhyx.action?cardWid=4006241&bType=86&serviceOperatorId=4&provinceId=1&cityId=1&enc=14C11B5289C91A06&t=0.3576853939393497'
            self.browser.get(url)
            time.sleep(15)
        except Exception as e:
            print(e)

        pid = self.browser.find_element_by_css_selector('select#pId')
        selectPid = Select(pid)
        for select in selectPid.options:
            province = select.text
            select.click()
            cid = self.browser.find_element_by_css_selector('select#cId')
            selectCid = Select(cid)

            for selectChild in selectCid.options:
                city = selectChild.text
                selectChild.click()
                time.sleep(1)

                try:
                    area = self.browser.find_element_by_css_selector('tbody#step-1-1-left')
                    num = area.find_element_by_class_name('phone-num').text
                except:
                    continue
                else:
                    record += province + ' --- > ' + city + '\n'

        with open('./jd_mobile.txt', 'a+') as f:
            f.write(record)

        self.browser.quit()

if __name__ == '__main__':
    j = JDMobile()
    j.crawl()
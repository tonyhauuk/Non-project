import datetime, html
from w3lib.html import remove_comments
from html.parser import HTMLParser
from selenium import webdriver


def filteHTML(string):
    content = html.unescape(string)  # 去掉实体字符
    content = remove_comments(content)  # 过滤注释
    content = content.replace('&ensp;', '')
    content = content.replace('&emsp;', '')
    content = content.replace('&nbsp;', '')

    return content.strip()


def filter(string):
    html_tag = {'&#xA;': '\n', '&quot;': '\"', '&amp;': '', '&lt;': '<', '&gt;': '>',
                '&apos;': "'", '&nbsp;': ' ', '&yen;': '¥', '&copy;': '©', '&divide;': '÷'
        , '&times;': 'x', '&trade;': '™', '&reg;': '®', '&sect;': '§', '&euro;': '€',
                '&pound;': '£', '&cent;': '￠', '&raquo;': '»'
                }

    for k, v in html_tag.items():
        string = string.replace(k, v)
        string = string.replace(k[1:], v)

    return string


url = 'https://jxt.sc.gov.cn/scjxt/zyxxzz/2020/7/31/c1e7d02e8dd34c009d7ada4aa6daf063.shtml'
browser = webdriver.Firefox()
browser.set_window_position(x = 650, y = 0)
browser.get(url)
content = browser.find_element_by_css_selector('div#NewsContent').get_attribute('innerHTML')
# print(type(content))
html_parser = HTMLParser()
s =  html.unescape(content)
with open('./ttt.html', mode = 'w', encoding = 'utf-8') as f:
    f.write(s)

browser.quit()

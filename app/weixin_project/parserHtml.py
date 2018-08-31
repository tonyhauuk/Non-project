from bs4 import BeautifulSoup
import re, json, uuid

namespace = uuid.NAMESPACE_URL


def parserHTML(filePath, url):
    accountID = accountDesc = ''

    htmlDoc = open(filePath, 'r', encoding = 'UTF-8')
    soup = BeautifulSoup(htmlDoc, 'html.parser')
    html = soup.find(id = 'img-content')
    title = html.find(id = 'activity-name').get_text().strip()
    nickname = html.find(class_ = 'profile_nickname').get_text()
    account = html.find_all('p', class_ = 'profile_meta')

    for i in range(len(account)):
        accountStr = account[i].find('label', class_ = 'profile_meta_label').get_text()
        if accountStr == '微信号' or accountStr == 'WeChat ID':
            accountID = account[i].find('span', class_ = 'profile_meta_value').get_text()
            continue
        elif accountStr == '功能介绍' or accountStr == 'Intro':
            accountDesc = account[i].find('span', class_ = 'profile_meta_value').get_text()
            continue

    content = html.find('div', id = 'js_content').prettify()
    text = retainImgTag(content)
    publishDate = getDate(soup)
    uid = getUID(title)

    data = dict(uid = uid, title = title, nickname = nickname, accountID = accountID,
                accountDesc = accountDesc, url = url, publishData = publishDate, text = text)

    return data


def getUID(title):
    uid = uuid.uuid3(namespace, title)
    code = str(uid).split('-')
    s = ''.join(code)

    return s


def getDate(soup):
    time = ''
    js = soup.find_all('script')
    for str in js:
        text = str.get_text()
        find = re.findall(r'createDate/?.*?1000', text)
        target = ''.join(find)

        if 'createDate' in target:
            date = target.split('Date(')
            raw = date[1].split('*')
            time = raw[0].replace('"', '')
            break

    return int(time)


def retainImgTag(img):
    all = re.findall(r'</?.*?>', img)
    save = re.findall(r'</?(?:img).*?>', img)

    for e in all:
        if e not in save:
            match = img.replace(e, '\n')
            img = match
    result = ' '.join(img.split())
    result = filterAttrs(result)

    return result


def filterAttrs(str):
    filter1 = re.compile('(class=".*?)"', re.S | re.MULTILINE)
    filter2 = re.compile('(data-copyright=".*?)"', re.S | re.MULTILINE)
    filter3 = re.compile('(data-ratio=".*?)"', re.S | re.MULTILINE)
    filter4 = re.compile('(data-s=".*?)"', re.S | re.MULTILINE)
    filter5 = re.compile('(data-type=".*?)"', re.S | re.MULTILINE)
    filter6 = re.compile('(data-w=".*?)"', re.S | re.MULTILINE)
    filter7 = re.compile('(style=".*?)"', re.S | re.MULTILINE)
    filter8 = re.compile('(data-croporisrc=".*?)"', re.S | re.MULTILINE)
    filter9 = re.compile('(data-crop.+?=".*?)"', re.S | re.MULTILINE)

    text = filter1.sub('', str)
    text = filter2.sub('', text)
    text = filter3.sub('', text)
    text = filter4.sub('', text)
    text = filter5.sub('', text)
    text = filter6.sub('', text)
    text = filter7.sub('', text)
    text = filter8.sub('', text)
    text = filter9.sub('', text)

    filterText = ' '.join(text.split())
    result = filterText.replace('data-src', 'src')

    return result


def foo():
    fileList = ['./q1.htm', './q2.html', './w3.html']
    url = ['https://www.q1q1q1.com', 'https://www.1111.com', 'http://qq.com']
    info = []
    index = 0
    for path in fileList:
        data = parserHTML(path, url[index])
        info.append(data)
        index += 1

    jsonObj = json.dumps(info, ensure_ascii = False, indent = 4, separators = (',', ': '))
    print(jsonObj)


foo()

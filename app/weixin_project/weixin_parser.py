from bs4 import BeautifulSoup
import re, json, uuid


class WeixinParser:
    def __init__(self):
        self.namespace = uuid.NAMESPACE_URL

    def loadHTML(self, filePath, url):
        htmlDoc = open(filePath, 'r', encoding = 'UTF-8')
        htmlStr = htmlDoc.read()
        data = self.parserHTML(htmlStr, url)
        htmlDoc.close()
        return data

    def parserHTML(self, htmlDoc, url):
        soup = BeautifulSoup(htmlDoc, 'html.parser')
        html = soup.find(id = 'img-content', class_ = 'original_page')

        if html == None:
            html = soup.find(id = 'img-content')
            data = self.originHTML(html, soup, url)
        else:
            html = soup.find(id = 'img-content', class_ = 'original_page')
            data = self.sharedHTML(html, soup, url)

        return data

    def originHTML(self, html, soup, url):
        accountID = accountDesc = ''
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
        text = self.retainImgTag(content)
        publishDate = self.getDate(soup)
        uid = self.getUID(title)

        data = dict(uid = uid, title = title, nickname = nickname, accountID = accountID,
                    accountDesc = accountDesc, url = url, publishData = publishDate,
                    share = False, text = text)

        return data

    def sharedHTML(self, html, soup, url):
        accountID = accountDesc = ''
        title = html.find('div', class_ = "original_panel_title").get_text().strip()
        nickname = html.find(class_ = 'account_nickname').get_text().strip()
        account = html.find_all('p', class_ = 'profile_meta')

        for i in range(len(account)):
            accountStr = account[i].find('label', class_ = 'profile_meta_label').get_text()
            if accountStr == '微信号' or accountStr == 'WeChat ID':
                accountID = account[i].find('span', class_ = 'profile_meta_value').get_text()
                continue
            elif accountStr == '功能介绍' or accountStr == 'Intro':
                accountDesc = account[i].find('span', class_ = 'profile_meta_value').get_text()
                continue

        content = html.find('p', id = 'js_share_notice').prettify()
        text = self.retainImgTag(content)
        publishDate = self.getDate(soup)
        uid = self.getUID(title)

        data = dict(uid = uid, title = title, nickname = nickname, accountID = accountID,
                    accountDesc = accountDesc, url = url, publishData = publishDate,
                    share = True, text = text)

        return data

    def getUID(self, title):
        uid = uuid.uuid3(self.namespace, title)
        code = str(uid).split('-')
        s = ''.join(code)

        return s

    def getDate(self, soup):
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

    def retainImgTag(self, img):
        all = re.findall(r'</?.*?>', img)
        save = re.findall(r'</?(?:img).*?/>', img)

        for e in all:
            if e not in save:
                match = img.replace(e, '')
                img = match
        result = ' '.join(img.split())
        result = self.filterAttrs(result)
        result = result.replace('。 <img', '。\n<img')
        result = result.replace(' <img', '\n<img')
        result = result.replace('/> ', '/> \n')
        result = result.replace('。 ', '。 \n')

        return result

    def filterAttrs(self, str):
        filter1 = re.compile('(class=".*?)"', re.S | re.M)
        filter2 = re.compile('(data-copyright=".*?)"', re.S | re.M)
        filter3 = re.compile('(data-ratio=".*?)"', re.S | re.M)
        filter4 = re.compile('(data-s=".*?)"', re.S | re.M)
        filter5 = re.compile('(data-type=".*?)"', re.S | re.M)
        filter6 = re.compile('(data-w=".*?)"', re.S | re.M)
        filter7 = re.compile('(style=".*?)"', re.S | re.M)
        filter8 = re.compile('(data-croporisrc=".*?)"', re.S | re.M)
        filter9 = re.compile('(data-crop.+?=".*?)"', re.S | re.M)
        filter10 = re.compile('(width=".*?)"', re.S | re.M)
        filter11 = re.compile('(style=\'.*?)\'', re.S | re.M)
        filter12 = re.compile('(data-b.*?=.+?)"', re.S | re.M)

        text = filter1.sub('', str)
        text = filter2.sub('', text)
        text = filter3.sub('', text)
        text = filter4.sub('', text)
        text = filter5.sub('', text)
        text = filter6.sub('', text)
        text = filter7.sub('', text)
        text = filter8.sub('', text)
        text = filter9.sub('', text)
        text = filter10.sub('', text)
        text = filter11.sub('', text)
        text = filter12.sub('', text)

        filterText = ' '.join(text.split())
        result = filterText.replace('data-src', 'src')
        result = result.replace('style=""', '')
        result = result.replace('"', '\'')

        return result


if __name__ == '__main__':
    p = WeixinParser()
    fileList = ['./q1.htm', './q2.html', './w3.html']
    url = ['https://www.q1q1q1.com', 'https://www.1111.com', 'http://qq.com']
    info = []
    index = 0
    for path in fileList:
        data = p.loadHTML(path, url[index])
        info.append(data)
        index += 1

    jsonObj = json.dumps(info, ensure_ascii = False, indent = 4, separators = (',', ': '))
    print(jsonObj)

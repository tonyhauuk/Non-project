from bs4 import BeautifulSoup
import time, requests, bs4, datetime, re, hashlib, os, sys
from template import Temp

sys.path.append('../')
import crawlerfun


class Crawler:
    def __init__(self, d):
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        self.date = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        self.d = d
        self.dir = self._dir = ''
        self.ipnum = crawlerfun.ip2num('54.36.226.229')
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0",
        }


    def doJob(self):
        for url in self.schedule():
            self.doCrawl(url)


    def doCrawl(self, req):
        self.i = self.total = 0
        page = 1
        compare = self.dictPath(req)

        while True:
            print('\nurl:', compare, ' ======= ', req, '========\n')
            try:
                response = requests.get(req, headers = self.headers)
            except:
                continue

            bs = BeautifulSoup(response.content.decode('utf-8'), 'lxml')
            titleList = bs.find(Temp.arr[compare]['div'], Temp.arr[compare]['divCls'])
            li = titleList.find_all(Temp.arr[compare]['li'])

            for item in li:
                time = item.find(Temp.arr[compare]['timeDiv'], Temp.arr[compare]['timeCls'])
                if time.text in self.date:
                    self.open(item, compare)
                else:
                    if compare == 1 and page == 1:  # 如果当前是南方电网并且在第一页，直接跳过不符合的日期，继续采
                        continue
                    else:
                        break

            if self.i == 0:
                break

            page += 1
            req = req.replace(str(page - 1), str(page))
            self.i = 0

        if self.total > 0:
            crawlerfun.rename(self._dir, self.dir)
            self.expire()


    def open(self, item, compare):
        if compare == 0:
            div = item.find(Temp.arr[compare]['div'])
            title = div.find('a').get('title')
            md5 = self.makeMD5(title)
            # dict filter
            if md5 in self.d:
                return
            else:
                self.d[md5] = self.date.split(' ')[0]  # 往dict里插入记录
                self.i += 1
                self.total += 1

            nextPage = div.find('a').get('onclick')
            pages = nextPage.split(',')
            a = re.sub('\D', '', pages[0])
            b = re.sub('\D', '', pages[1])
            url = 'http://ecp.sgcc.com.cn/html/news/' + a + '/' + b + '.html'

            self.reopen(url, title, 1170771, compare)
        elif compare == 1:
            a = item.find_all('a')[2]
            title = a.text
            md5 = self.makeMD5(title)

            # dict filter
            if md5 in self.d:
                return
            else:
                self.d[md5] = self.date.split(' ')[0]  # 往dict里插入记录
                self.i += 1
                self.total += 1

            urlSuffix = a['href']
            url = 'http://www.bidding.csg.cn' + urlSuffix

            self.reopen(url, title, 1170773, compare)


    def reopen(self, url, title, id, compare):
        try:
            response = requests.get(url, headers = self.headers)
        except requests.exceptions.ConnectionError as e:
            time.sleep(30)
            response = requests.get(url, headers = self.headers)

        bs = BeautifulSoup(response.content.decode('utf-8'), 'lxml')
        content = ''

        contents = bs.select(Temp.arr[compare]['contents1'])
        if len(contents) == 0:
            contents = bs.select(Temp.arr[compare]['contents2'])

        if len(contents) == 0:
            content = ''
        else:
            for i in range(len(contents)):
                content += contents[i].text

        if compare == 1:
            date = bs.find('div', 's-date')
            pattern = re.compile(r'[\u4e00-\u9fa5]')
            reg = re.sub(pattern, '', date.text)
            time = reg.replace('：', '').strip()
        else:
            time = self.date

        self.write_new_file(url, title, content, self.i, id, time)


    def dictPath(self, url):
        if 'sgcc' in url:
            return 0
        elif 'bidding' in url:
            return 1


    def makeMD5(self, title):
        m = hashlib.md5()
        b = title.encode(encoding = 'utf-8')
        m.update(b)
        enc = m.hexdigest()

        return enc


    def schedule(self):
        filName = './webList.txt'
        schedule = []
        with open(file = filName, mode = 'r') as f:
            for line in f.readlines():
                schedule.append(line.strip())

        return schedule


    # 写一个新文章
    def write_new_file(self, url, title, source, i, id, time):
        dct = {1170771: '国家电网有限公司', 1170773: '中国南方电网供应链统一服务平台'}

        ok = 0
        content = '''
                    <html>
                        <head> 
                           <meta charset="utf-8">
                           <meta name="keywords" content="estarinfo">
                        </head> 
                        <body>
                            <h1 class="title">''' + title + '''</h1>
                            <span class="time">''' + time + '''</span>
                            <span class="source">''' + dct[id] + '''</span>
                            <div class="article">''' + source + '''</div>
                        </body>
                    </html>
                '''
        page_text = url + '\n' + title + '\n' + str(id) + '\n\n\n' + content
        print(title)
        if '' == self._dir:
            self.guojiadianwang_mkdir()

        filename = self._dir + 'iask_' + str(i) + '_' + str(len(self.d)) + '.htm-2'
        for num in range(2):
            if 1 == crawlerfun.write_file(filename, page_text, ifdisplay = 0):
                filename = '/root/estar_save/' + 'iask_' + str(i) + '_' + str(len(self.d)) + '.htm-2'
                crawlerfun.write_file(filename, page_text, ifdisplay = 0)  # 再次保存到/root/estar_save目录下
                ok = 1
                break
            else:  # 有时目录会被c程序删掉
                crawlerfun.mkdir(self._dir)

        return ok


    # 制作百家号目录，注意不创建目录，只是生成目录信息
    def guojiadianwang_mkdir(self):
        dirroot = '/estar/newhuike2/1/'
        tm_s, tm_millisecond = crawlerfun.get_timestamp(ifmillisecond = 1)
        dirsmall = 'iask' + str(self.ipnum) + '.' + str(1) + '.' + str(tm_s) + '.' + str(tm_millisecond) + '/'
        self._dir = dirroot + '_' + dirsmall
        self.dir = dirroot + dirsmall

        return self._dir, self.dir


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
            fileName = './md5.txt'
            os.remove(fileName)
            with open(fileName, 'a+') as f:
                f.write(str(self.d))
        except Exception as e:
            print(e)

# coding: utf-8
# -*- coding: utf-8 -*-
# ***********************************************************
# server版
# 程序在后台运行 ，打开并保持一个浏览器，不断读取指定目录下的文件，寻找任务，任务是采集连接或关键词，
# 返回采集页面
# 浏览器不关闭，除非程序退出。
# 例程 https://www.cnblogs.com/NolaLi/p/8495081.html
# 关于Google Chrome 浏览器的一些命令及用法 https://www.cnblogs.com/donaldlee2008/p/5909586.html
# pip3 install web.py==0.40.dev0

# python SimpleHTTPServer
# python -m http.server 80

# 如果遇到编码错误：UnicodeEncodeError: 'ascii' codec can't encode characters in position
# 在linux下运行：echo 'export LANG=en_US.UTF-8' >> ~/.bashrc   并重启机器即可
# 或者运行：PYTHONIOENCODING=utf-8 python your_script.py 也可以
# sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach()) #解决编码问题，但加这句运行会特慢

'''
动态ip的vps关闭防火墙，减少系统负荷
centos7注意开启防火墙 5000端口
启动： systemctl start firewalld
关闭： systemctl stop firewalld
查看状态： systemctl status firewalld
添加
firewall-cmd --zone=public --add-port=80/tcp --permanent    （--permanent永久生效，没有此参数重启后失效）
重新载入
firewall-cmd --reload

编码：
国外服务器需要修改编码
/etc/locale.conf
LANG="en_US.UTF-8"   或  LANG="zh_CN.UTF-8"

frp
https://github.com/fatedier/frp/releases
'''
# ***********************************************************
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.opera.options import Options as operaOptions

import codecs
import time
import sys
import os
import configparser
import tldextract  # pip3 install tldextract
import base64
import importlib
import threading
# import web
import urllib.request
# importlib.reload(sys)

import paramiko  # sftp模块20190318
import shutil  # 删除文件夹
from crawlerfun import ClearCache
import crawlerfun

from baijiahao_2nd import Baijiahao
# from weibo_new import Weibo


# ***********************************************************
# 浏览器类
# ***********************************************************
class Browser:
    # 基本信息
    state = 0  # 浏览器是否被占用
    index = 0
    servernum = 0  # 这组浏览器个数
    runtype = ''  # 程序运行模式：webserver or dirserver

    # 浏览器设置
    proxy = ''
    proxyList = []
    headless = ''
    connection = ''  # 网络连接方式，direct or pppoe
    driver = ''  # 浏览器驱动，必须先启动driver，才能使用浏览器。

    # 任务参数  work,url,ifdomain,returnDataType
    # work = ''
    url = ''
    tasktype = ''
    ifdomain = ''  # 是否出域采集， in  or  out
    returnDataType = 'server'  # 数据返回方式，server和web ,server提供目录级的响应方式，web提供端口监控的直接返回方式

    # 目录及文件信息
    diroot = ''  # 入口目录
    name = ''
    _name = ''
    _output_file = ''
    output_file = ''

    # 返回信息
    weixinNewLink = ''
    # weixinLinkType = 'server'
    weixin_json = ''
    # 重启浏览器后清零计数，每采集一次累加1
    num_crawlpy = 0
    proxypub = ''
    ifimg = 0
    cache_dir = ''  # 缓存目录
    goodinfonum = 0
    browserchoice = ''  # 浏览器  'Chrome' ,'Firefox'
    limit = 'ok'
    timeout = 10
    ip = ''
    search_type = ''
    d = {}


    # def __init__(self, index, servernum, runtype, diroot, headless, connection, proxypub,ifimg,browserchoice,timeout,ip):
    def __init__(self, index, threadsNum, runtype, config):
        # threadsNum = int(config.getint(runtype, 'threadsNum'))
        # headless = config[runtype]['headless']
        # diroot = config[runtype]['dir']
        # connection = config[runtype]['connect']
        # proxypub = config[runtype]['proxypub']
        # ifimg = int(config[runtype]['ifimg'])
        # browserchoice = config[runtype]['browserchoice']
        # timeout = int(config[runtype]['timeout'])
        # ip = config[runtype]['ip']

        # 基本信息
        self.state = 0  # 浏览器是否被占用
        self.index = index
        self.servernum = threadsNum  # 这组浏览器个数
        self.runtype = runtype  # 程序运行模式：webserver or dirserver
        print(self.index, "/", self.servernum)

        # 浏览器设置
        self.proxy = ''
        self.headless = config['headless'].strip()  # head headless
        self.connection = config['connect'].strip()  # 网络连接方式，direct or pppoe
        self.proxypub = config['proxypub'].strip()  # none #127.0.0.1:8080
        self.ifimg = int(config['ifimg'].strip())  # 0 1
        self.browserchoice = config['browserchoice'].strip()  # 'Chrome' ,'Firefox' 'Opera' 'OperaRemote'
        # 目录及文件信息
        self.diroot = config['dir'].strip()  # 入口目录
        self.name = ''
        self._name = ''
        self._output_file = ''
        self.output_file = ''
        self.proxyList = []
        self.cache_dir = '/dev/shm/cache'
        self.limit = 'ok'
        if os.path.isdir(self.cache_dir) == True:
            shutil.rmtree(self.cache_dir)  # 递归删除文件夹
        self.goodinfonum = 0
        self.timeout = int(config['timeout'].strip())
        self.ip = config['ip']
        self.savetype = config['savetype'].strip()
        self.search_type = config['search_type'].strip()
        self.start_driver()  # self.driver = '' #浏览器
        self.d = {}


    def __del__(self):
        class_name = self.__class__.__name__


    # self.close_web_driver()
    # self.driver.quit()
    # self.driver.close()

    # ***********************************************************
    # 读取代理
    # 读取代理文件，放入队列，每次取一个
    # ***********************************************************
    def get_proxy(self):
        print("proxyList len = ", len(self.proxyList))
        if len(self.proxyList) > 0:
            self.proxy = self.proxyList.pop()
        else:
            while len(self.proxyList) == 0:
                nowtime = time.strftime('%Y-%m-%d_%H:%M', time.localtime(time.time() - 60))
                proxy_file = "../proxy/" + "pythonporxy"  # + nowtime  # 2018-11-09_06:05

                # 下载proxy文件
                host = '123.56.234.47'  # 主机
                port = 22  # 端口
                username = 'xuning'  # 用户名
                password = 'estar1981xuning64'  # 密码
                local = proxy_file  # 本地文件或目录，与远程一致，当前为windows目录格式，window目录中间需要使用双斜线
                remote = '/home/xuning/collector/proxy/' + nowtime  # 远程文件或目录，与本地一致，当前为linux目录格式
                print("now to download file :  " + nowtime)
                if 'ok' == sftp_download(host, port, username, password, local, remote):
                    try:
                        for proxy in open(proxy_file):
                            self.proxyList.append(proxy.strip())
                    except:
                        print("read file error " + proxy_file)
                        time.sleep(15)
                    else:
                        pass
                else:
                    time.sleep(15)

            self.proxy = self.proxyList.pop()


    # ***********************************************************
    # 启动谷歌浏览器
    # ***********************************************************
    def start_Chrome(self):
        # _____________________启动参数___________________________
        # h完整的启动参数可以到此网页查看： ttps://peter.sh/experiments/chromium-command-line-switches/
        prefs = {}
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-logging')  # 关闭日志记录 未测试
        # options.add_argument("window-size=1024,768")
        options.add_argument("--disable-infobars");  # 禁用浏览器正在被自动化程序控制的提示
        # window.navigator.webdriver，变成undefined。 http://www.cnseu.net/?p=85
        # 设置后，会引发ClearCache（）无法执行
        # options.add_experimental_option('excludeSwitches', ['enable-automation'])

        # User-Agent
        options.add_argument(
            'user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.103 Safari/537.36"')
        # 忽略证书。在忽略和不忽略之际切换，在不忽略情况下可以正常采集2、3次
        # options.add_argument("ignore-certificate-errors")
        # /usr/bin/google-chrome-stable %U --no-sandbox --proxy-server=127.0.0.1:8080 --ignore-certificate-errors

        # 不加载图片  添加实验性质的设置参数 (add_experimental_option)
        if 0 == self.ifimg:
            # 可以禁止图片显示
            # prefs = {"profile.managed_default_content_settings.images": 2}
            # options.add_experimental_option("prefs", prefs)

            # 这句来自opera的生效了可以禁止图片显示
            # options.add_argument('blink-settings=imagesEnabled=false')

            prefs.update({"profile.managed_default_content_settings.images": 2})  # 禁止图片
            prefs.update({"profile.content_settings.plugin_whitelist.adobe-flash-player": 2})  # flash，视频之类的多媒体
            prefs.update({"profile.content_settings.exceptions.plugins.*,*.per_resource.adobe-flash-player": 2})
            '''
            prefs = {
                "profile.managed_default_content_settings.images": 2, #禁止图片
                "profile.content_settings.plugin_whitelist.adobe-flash-player": 2, #flash，视频之类的多媒体
                "profile.content_settings.exceptions.plugins.*,*.per_resource.adobe-flash-player": 2,
            }
            options.add_experimental_option('prefs', prefs)
            '''
        # 设置缓存位置 options.add_argument('--disk-cache-dir=./cache')
        options.add_argument('--disk-cache-dir=%s' % self.cache_dir)
        # options.add_argument('--disk-cache-dir=/dev/shm/cache')
        # _____________________设置有头还是无头_____________________
        if 'headless' == self.headless:
            options.add_argument('--headless')

        # _____________________设置代理_____________________
        if "proxy" == self.connection:
            self.get_proxy()
            print("use proxy = " + self.proxy)
            # options.add_argument('--proxy-server=http://%s' % self.proxy)
            options.add_argument('--proxy-server=%s' % self.proxy)
        elif 'none' != self.proxypub:
            self.proxy = self.proxypub  # '127.0.0.1:8080'
            print("use proxy = " + self.proxy)
            # options.add_argument('--proxy-server=http://%s' % self.proxy)
            options.add_argument('--proxy-server=%s' % self.proxy)

        # _____________________禁用浏览器弹窗___未测试__________________
        '''
        prefs = {
            'profile.default_content_setting_values': {
                'notifications': 2
            }
        }
        options.add_experimental_option('prefs', prefs)
        '''
        # prefs.update({"profile.default_content_setting_values": { 'notifications': 2}})

        if len(prefs) > 0:
            options.add_experimental_option('prefs', prefs)
        self.driver = webdriver.Chrome(chrome_options = options)
        self.driver.set_window_size(1160, 690)
        self.driver.set_window_position(x = 200, y = 0)


    # ***********************************************************
    # 启动火狐浏览器
    # ***********************************************************
    def start_Firefox(self):
        options = webdriver.FirefoxOptions()
        options.add_argument('--disable-gpu')
        options.add_argument(
            'user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.103 Safari/537.36"')

        # _____________________不加载图片_____________________
        if 0 == self.ifimg:
            options.set_preference('permissions.default.image', 2)
        # _____________________设置有头还是无头_____________________
        if 'headless' == self.headless:
            options.add_argument('--headless')
        self.driver = webdriver.Firefox(options = options)


    # ***********************************************************
    # 启动Opera浏览器
    # ***********************************************************
    def start_Opera(self):
        # subprocess.Popen('ps -efww|grep opera|grep -v grep|cut -c 9-15|xargs kill', shell=True, stdout=subprocess.PIPE)

        # hselenium chrome启动项详解 ttps://blog.csdn.net/weixin_42038296/article/details/84112328
        options = operaOptions()
        options.binary_location = '/usr/lib64/opera/opera'
        # _____________________不加载图片_____________________
        # if 0 == self.ifimg:
        # prefs = {"profile.managed_default_content_settings.images": 2}#无效
        # options.add_experimental_option("prefs", prefs)#无效
        # options.add_argument('blink-settings=imagesEnabled=false')# 不加载图片, 提升速度 https://blog.csdn.net/weixin_38595982/article/details/83716771
        # options.add_argument('--disable-images')#无效

        # _____________________设置有头还是无头_____________________
        if 'headless' == self.headless:
            options.add_argument('--headless')

        options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
        options.add_argument('--no-sandbox')
        # In Chrome, I did not have enough resources allocated to my Docker Container. Adding the "--disable-dev-shm-usage" flag to Chrome fixed the issue. Since its using local /tmp instead of it's /dev/shm it has plenty of room.
        options.add_argument('--disable-dev-shm-usage')  # overcome limited resource problems  克服有限的资源问题

        '''
        #通过下边的设置，可以自己设置浏览器的配置，并且自动保存，但效果好像没有原装的快20190419
        options.add_argument('--user-data-dir=/opera/data')     #设置成用户自己的数据目录
        options.add_argument('--disk-cache-dir=/opera/cache')   #自定义缓存目录
        options.add_argument('--disk-cache-size=1024000')       #自定义缓存最大值（单位byte）
        options.add_argument('--media-cache-size=1024000')      # 自定义多媒体缓存最大值（单位byte
        '''
        # Selenium启动Chrome时配置选项 https://blog.csdn.net/liaojianqiu0115/article/details/78353267
        options.add_argument('--disable-logging')  # 关闭日志记录
        options.add_argument('--disable-plugins')  # 禁止加载所有插件，可以增加速度。可以通过about:plugins页面查看效果
        options.add_argument('--disable-java')  # 禁用java
        # options.add_argument('--incognito') #启动进入隐身模式 ，无效
        # chrome_options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面

        # 模拟 iphone6
        # 无效 options.add_argument('user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"')
        # 无效 options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.103 Safari/537.36"')
        try:
            self.driver = webdriver.Opera(options = options, executable_path = '/usr/bin/operadriver')
            self.driver.set_window_size(1000, 690)
            self.driver.set_window_position(x = 250, y = 0)
        except:
            self.driver = 'error'


    # ***********************************************************
    # 启动Opera浏览器，用远程浏览器方式
    # ***********************************************************
    def start_OperaRemote(self):
        from selenium.webdriver.chrome import service

        webdriver_service = service.Service('/usr/bin/operadriver')
        webdriver_service.start()
        capabilities = {'operaOptions': {'debuggerAddress': "localhost:4444"}}
        try:
            self.driver = webdriver.Remote(webdriver_service.service_url, capabilities)
        except:
            self.driver = 'error'


    # ***********************************************************

    # 打开一个浏览器
    # ***********************************************************
    def start_driver(self):
        # print(self.index, sys._getframe().f_code.co_name)
        print('\tstart_driver')
        self.num_crawlpy = 0
        # _____________________创建浏览器_____________________
        count = 1
        self.start_Opera()
        if 'error' == self.driver:
            print(self.index, sys._getframe().f_code.co_name, ' init_web_driver error', 'count=', count)
            time.sleep(1)
        else:
            # self.timeout = 10
            # self.driver.implicitly_wait(self.timeout)# 隐性等待，设置完毕后不生效
            # 设置后生效
            self.driver.set_page_load_timeout(self.timeout)
            self.driver.set_script_timeout(self.timeout)
            try:
                self.driver.delete_all_cookies()
            # shutil.rmtree(self.cache_dir)
            except:
                print('\tdelete_all_cookies error')
        return
        while 1:

            if 'Chrome' == self.browserchoice:
                self.start_Chrome()
            elif 'Firefox' == self.browserchoice:
                self.start_Firefox()
            elif 'Opera' == self.browserchoice:
                self.start_Opera()
            elif 'OperaRemote' == self.browserchoice:
                # 不知为何，用函数方式启动不了，
                # self.start_OperaRemote()
                from selenium.webdriver.chrome import service

                webdriver_service = service.Service('/usr/bin/operadriver')
                webdriver_service.start()
                capabilities = {
                    'operaOptions': {'debuggerAddress': "localhost:4444"}}  # , 'blink-settings': "imagesEnabled=false"
                try:
                    self.driver = webdriver.Remote(webdriver_service.service_url, capabilities)
                # self.driver.refresh()
                except:
                    self.driver = 'error'
            else:
                print("no browserchoice [%s]" % (self.browserchoice))
                time.sleep(100000)

            if 'error' == self.driver:
                print(self.index, sys._getframe().f_code.co_name, ' init_web_driver error', 'count=', count)
                time.sleep(1)
            else:
                # self.timeout = 10
                # self.driver.implicitly_wait(self.timeout)# 隐性等待，设置完毕后不生效
                # 设置后生效
                self.driver.set_page_load_timeout(self.timeout)
                self.driver.set_script_timeout(self.timeout)
                try:
                    self.driver.delete_all_cookies()
                # shutil.rmtree(self.cache_dir)
                except:
                    print('\tdelete_all_cookies error')

                break
            count = count + 1


    # ***********************************************************
    # 关闭浏览器
    # ***********************************************************
    def close_driver(self):
        print('\tclose_driver')
        '''
        这是close()的说明：

        Closes the current window.
        关闭当前窗口。

        这是quit()的说明：

        Quits the driver and closes every associated window.
        退出驱动并关闭所有关联的窗口。

        try:
            self.driver.delete_all_cookies()
            #shutil.rmtree(self.cache_dir)
        except:
            print('\tdelete_all_cookies error')
        '''
        '''
        try:
            self.driver.close()  # 只会在内存中不断残留chrome进程
        except:
            pass
        '''
        # 发现有时无法正常关闭浏览器，如果再启动浏览器系统会驻留内存，所有要多次关闭，并且强制内存清空20190904
        ok = 0
        for times in range(0, 2):
            try:
                self.driver.quit()
            except:
                print('\tdriver.quit() error ', times)
            else:
                ok = 1
                break
        if 0 == ok:
            pass
        # self.browserchoice


    # ***********************************************************
    # 重新启动浏览器
    # ***********************************************************
    def restart_driver(self):
        print('restart_driver start')
        # ClearCache(self.driver)
        self.close_driver()
        time.sleep(3)
        self.start_driver()
        print('restart_driver end')


    # ***********************************************************
    # 提取域名
    # ***********************************************************
    def get_domain(self, url):
        # pip3 install tldextract
        extracted = tldextract.extract(url)
        domain = "{}.{}".format(extracted.domain, extracted.suffix)
        return domain


    '''
    # ***********************************************************
    # 普通下载网页
    # ***********************************************************
    def web_crawl(self):
        print("\t",self.index ,sys._getframe().f_code.co_name ,"begin")
        #self.driver.implicitly_wait(20)
        try:
            self.driver.get(self.url)
        except:# TimeoutException as e:
            print("\t",self.index ,"Browser timeout")
            return 'error'
        else:
            #return self.driver.page_source
            try:
                page_source = self.driver.page_source
            except:
                print("\t",self.index ,"html error")
                return 'error'
            else:
                #判断连接是否出域
                if False == self.url_judge():
                if 'in' == self.ifdomain:
                    page_source = 'outDomain'
                #self.write_file(page_source)
                return page_source
    '''


    # ***********************************************************
    # 扫描任务大目录,递归
    # ***********************************************************
    def scanTaskDir(self, dir, count):
        myname = sys._getframe().f_code.co_name
        print(self.index, count, myname, ":", dir)
        try:
            files = os.listdir(dir)
            # files.sort()
            files = sorted(files, key = lambda x: os.path.getmtime(os.path.join(dir, x)))
        except:
            print("\t", "scanTaskDir , can't open ", dir)
            return
        for _name in files:
            fullname = os.path.join(dir, _name)
            if os.path.isdir(fullname):
                self.scanTaskDir(fullname, count)
            else:
                self.doOneDirTask(dir, _name, count)


    '''
    # ***********************************************************
    # 下载连接判断
    # ***********************************************************
    def url_judge(self):
        if 'in' == self.ifdomain:
            current_url = self.get_current_url()
            if self.get_domain(current_url) != self.get_domain(self.url):
                print (self.index ,"url goto: ", current_url)  # current_url 方法可以得到当前页面的URL
                return False
        return True
    '''


    # ***********************************************************
    # 获取浏览器当前的连接
    # ***********************************************************
    def get_current_url(self):
        try:
            current_url = self.driver.current_url
        except:
            print("\t get_current_url error")
            return ''
        else:
            return current_url


    # ***********************************************************
    # 写文件
    # ***********************************************************
    def write_file(self, page_source):
        # 写文件
        if os.path.exists(self._output_file):  # 有时会出现c的任务已经取消，python还再写文件，造成目录积压
            try:
                fd = codecs.open(self._output_file, 'w', encoding = 'utf-8')
            except:
                print("\t", self.index, "open file error:", self._output_file)
                return False
            else:
                try:
                    fd.write(page_source)
                    fd.close()
                    os.rename(self._output_file, self.output_file)
                    print("\t", self.index, "write_file ok--------------------------------\n")
                    return True
                except:
                    print("\t", self.index, "write_file error----------------", self._output_file, "\n")
                    return False
        else:
            return False


    # ***********************************************************
    # 执行一个目录任务
    # ***********************************************************
    def doOneDirTask(self, dir, _name, count):
        # 文件名判断，是否是任务文件   _estarmanzhuawget_1152937_d08691c8aaa8dd36091f8b25df008a09_ServerWeb_44858
        if not _name.startswith("_estarmanzhuawget"):
            return

        # if not _name.endswith("_Server_"):
        # if _name.find("_Server") == -1:
        if _name.find("_DirServer") == -1:  # 20190321
            return

        task_index = int(_name.split('_')[-1])
        # print (task_index)
        if self.index != task_index % self.servernum:
            return

        print(self.index, count, sys._getframe().f_code.co_name, ":", _name)

        # 任务基本初始化
        self._name = _name
        self._output_file = os.path.join(dir, self._name)
        # name = _name.replace("_estarmanzhuawget", "estarmanzhuawget")
        self.name = self._name.replace('_', '', 1)  # _name[1:1000]
        self.output_file = os.path.join(dir, self.name)

        # 有时会出现c的任务已经取消，python还再执行任务
        if not os.path.exists(self._output_file):
            return

        try:
            f = open(self._output_file, 'r')
        except:
            print("\t", self.index, "open _output_file error")
            return
        else:
            if f:
                # url = f.read()
                try:
                    strline = f.readline()
                except:
                    f.close()
                    print("\t", self.index, "read url file error")
                    try:
                        os.rename(self._output_file, self.output_file)
                    except:
                        print("\t", self.index, "rename error")
                    return
                f.close()
                # downloadweb@@@@@@in@@@@@@http://weixin.sogou.com/weixin?type=2&query=%E7%8B%AE%E7%8E%8B%E6%97%A5%E7%94%A8
                # print (strline)
                strline = strline.replace('\t', '').replace('\n', '')  # .replace(' ','')
                str_arr = strline.split('@@@@@@')
                tasktype = str_arr[0].replace(' ', '')  # downloadweb
                ifdomain = str_arr[1].replace(' ', '')  # in
                url = str_arr[
                    2]  # .replace(' ','') #http://weixin.sogou.com/weixin?type=2&query=%E7%8B%AE%E7%8E%8B%E6%97%A5%E7%94%A8
                if not url.startswith("http"):
                    return
                returnDataType = 'server'

                self.taskInitializtion(url, tasktype, ifdomain, returnDataType)
            else:
                print("\t", self.index, "f error")
                return

        self.browser_crawl()


    # ***********************************************************
    # 任务初始化参数
    # ***********************************************************
    def taskInitializtion(self, url, tasktype, ifdomain, returnDataType):
        # dirserver
        self.ifdomain = ifdomain
        self.url = url
        self.tasktype = tasktype
        self.returnDataType = returnDataType


    # ***********************************************************
    # 浏览器检查
    # ***********************************************************
    def torestart(self):
        # print("\t", self.index, "error:[", self.url, "]")
        print("\t", self.index, "torestart")
        self.restart_driver()
        # 2020-01-09 屏蔽拨号程序
        # if "pppoe" == self.connection and 0 == self.index and self.limit == 'error':
        #     # os.system('../pppoe.sh')
        #     # time.sleep(2)
        #     change_ip_for_vps()

        '''
        # Opera无需重启，只需清理cookies
        if self.browserchoice.find('Opera') > -1:
            # 在关闭浏览器时已经清理了cookies
            try:
                self.driver.delete_all_cookies()
            except:  # TimeoutException as e:
                print("\t", self.index, "delete_all_cookies error ")
                self.restart_driver()
        # 其他浏览器重启（可以只清理cookies试试）
        else:
            # 不重启浏览器，微信会跟踪cookie，会再出错，除非情况cookie
            # time.sleep(1)
            self.restart_driver()
        '''
        self.limit = 'ok'


    # ***********************************************************
    # 执行下载任务
    # ***********************************************************

    def browser_crawl(self):
        print('\n\n', self.index, '----------------browser_crawl begin----------------', )
        # 清理缓存目录
        # if os.path.isdir(self.cache_dir) == True:
        # shutil.rmtree(self.cache_dir)
        # 清理浏览器缓存
        if 0 == self.goodinfonum or self.goodinfonum > 50:
            subprocess.Popen('tmpwatch 1 /tmp/', shell = True, stdout = subprocess.PIPE)
            # if 'Chrome' == self.browserchoice :
            #     ClearCache(self.driver)

            self.goodinfonum = 1
        i = 0
        # 2次采集
        for times in range(0, 1):
            print('times = ',times)
            # 浏览器检查
            if 'ok' != self.limit:
                self.torestart()

            try:
                b = Baijiahao(self)
                completed, content, self.limit = b.crawl()
            except Exception as e:
                # print('program error: ', e)
                completed, content, self.limit = 'interrupt', 'none', 'no'

            print(self.index, '---------', 'completed =', completed, 'content len =', len(content), 'limit =',
                  self.limit)
            # if len(content) >100 :
            # time.sleep(10000)
            '''
            返回值说明
            completed，是否完成，'complete'是完成,'interrupt'中断。
            注意，只要有信息就认为是完成了，即使信息采集数量不完整（采集0篇文章很可能是某个关键词就是没有新文章，所以用文章数量是不能控制的。）
            content，返回的内容，'none'表示没有信息 '<html>...</html>',或其他是有信息
            limit,是否被反扒了，'error','no'，'ok'。其中no是浏览器没有反馈，只需要重启浏览器，不要重新拨号。如果错误意味一定信息没有采集完成，是中断状态。
            '''
            # 完成的退出机制，只要有信息就退出，有可能采集不完整，但就这样吧
            if completed == 'complete' or content != 'none':
                self.goodinfonum = self.goodinfonum + 1
                break

        # 返回机制
        if 'dirserver' == self.runtype:
            self.write_file(content)
            return ''
        elif 'webserver' == self.runtype:
            # mytime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            mytime = time.strftime("%Y_%m_%d %H:%M:%S", time.localtime())
            print(self.index, mytime, '  webserver----------------------ok---len = ', len(content))
            return content
        else:
            return ''


    # ***********************************************************
    # 定时清理，目录清理专用
    # ***********************************************************
    def clear(self, count):
        if 0 == count % 1800:
            try:
                # os.remove('./nohup.out')    #删除文件
                subprocess.Popen('rm nohup.out -rf', shell = True, stdout = subprocess.PIPE)
            except:
                print("remove error")


    # os.system('pkill -９ chrome')
    # self.restart_driver(timeout=20)
    # ***********************************************************
    # 等待执行任务
    # ***********************************************************
    def dirServer(self):
        count = 1
        while (1):
            self.scanTaskDir(self.diroot, count)
            count = count + 1
            self.clear(count)
            time.sleep(1)
            print("\n")
        # if count >2:
        #   break
        self.close_driver()


    # ***********************************************************
    # webServer激活函数
    # ***********************************************************
    def webServer(self):
        # https://blog.csdn.net/u011541946/article/details/77858538
        if 0 == self.index:
            dir = os.path.join(self.diroot, 'weixin')
            os.system("mkdir -p " + dir)
            dir = os.path.join(self.diroot, 'weixininfo')
            os.system("mkdir -p " + dir)
            # 启动5000端口监听,若不指定host='0.0.0.0'，则只允许本机访问  'webserver' ==
            # if config.getint('webserver', 'threadsNum') > 0:
            port = config.getint('webserver', 'port')  # 6081
            app.run(host = '0.0.0.0', port = port)


    # ***********************************************************
    # 完成一个web访问任务
    # ***********************************************************
    # @timeout_decorator.timeout(600, use_signals=False)
    def doOneWebTask(self, url, tasktype):
        if tasktype not in ['info', 'web', 'link']:
            print('tasktype error')
            self.state = 0
            return 'type error'

        url = base64.b64decode(url.encode('utf-8'))
        url = str(url, 'utf-8')

        '''
        if 'link' == tasktype:
            work = "weixingetlink"
        elif 'info' == tasktype:
            work = "weixingetinfo"
        else:
            return 'type error'
        '''
        ifdomain = 'out'
        returnDataType = "web"
        self.taskInitializtion(url, tasktype, ifdomain, returnDataType)
        self.state = 0

        myreturn = self.browser_crawl()

        return myreturn


    # ***********************************************************
    # 线程启动程序入口函数
    # ***********************************************************
    def browserRoot(self):
        # 循环扫描目录，获取任务，并执行
        if 'dirserver' == self.runtype:
            self.dirServer()
        # 以webserver方式提供服务器，监听端口，获取任务
        elif 'webserver' == self.runtype:
            self.webServer()
        # 其他
        else:
            print(self.index, "runtype error  runtype=", self.runtype)
            self.close_driver()


# ***********************************************************
# bytes to kb m g
# ***********************************************************
def formatSize(bytes):
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except:
        print("format error")
        return 0

    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return "%fG" % (G)
        else:
            return "%fM" % (M)
    else:
        return "%fkb" % (kb)


# ***********************************************************
# get file size
# ***********************************************************
def getDocSize(path):
    try:
        size = os.path.getsize(path)
        return formatSize(size)
    except Exception as err:
        print(err)
        return 0


# ***********************************************************
# 拨号
# https://www.92ez.com/?action=show&id=23447
# ***********************************************************
import subprocess
import re


def vpscmd():
    num = 0
    while num < 20:
        num = num + 1
        print(num, 'pppoe-status')
        try:
            pppoe_restart = subprocess.Popen('pppoe-status', shell = True, stdout = subprocess.PIPE)
        # pppoe_restart = subprocess.run("pppoe-status", shell=True, check=True)
        # pppoe_restart.wait()
        except:
            print(num, 'pppoe-status  error')
            time.sleep(1)
            continue

        print(num, 'adsl_ip')
        try:
            # pppoe_restart = str(pppoe_restart)
            # print (pppoe_restart)
            pppoe_log = pppoe_restart.communicate()[0]
            pppoe_log = str(pppoe_log)
            # print (pppoe_log)
            adsl_ip = re.findall(r'inet (.+?) peer ', pppoe_log)[0]
            print(num, '[*] New ip address : ' + adsl_ip)
            return True
        except:  # Exception, e:
            # print e
            print(num, 'adsl error')
            time.sleep(1)
            continue


def change_ip_for_vps():
    while 1:
        '''
        print ('pppoe-stop')
        try:
            subprocess.Popen('pppoe-stop', shell=True, stdout=subprocess.PIPE)
            #pppoe_restart = subprocess.run("pppoe-stop", shell=True, check=True)
        except:
            print ('pppoe-stop error')
            time.sleep(5)
            #num = num +1
            continue
        else:
            break

        time.sleep(1)



        print ('pppoe-start')
        try:
            subprocess.Popen('pppoe-start', shell=True, stdout=subprocess.PIPE)
            #subprocess.run("pppoe-start", shell=True, check=True)
        except:
            print ('pppoe-start error')
            time.sleep(5)
            continue

        time.sleep(1)
        '''
        subprocess.run("../pppoe.sh", shell = True, check = True)
        # time.sleep(5)
        # return True
        num = 0
        while num < 20:
            num = num + 1
            print(num, 'pppoe-status')
            try:
                pppoe_restart = subprocess.Popen('pppoe-status', shell = True, stdout = subprocess.PIPE)
            # pppoe_restart = subprocess.run("pppoe-status", shell=True, check=True)
            # pppoe_restart.wait()
            except:
                print(num, 'pppoe-status  error')
                time.sleep(1)
                continue

            print(num, 'adsl_ip')
            try:
                # pppoe_restart = str(pppoe_restart)
                # print (pppoe_restart)
                pppoe_log = pppoe_restart.communicate()[0]
                pppoe_log = str(pppoe_log)
                # print (pppoe_log)
                adsl_ip = re.findall(r'inet (.+?) peer ', pppoe_log)[0]
                print(num, '[*] New ip address : ' + adsl_ip)
                return True
            except:  # Exception, e:
                # print e
                print(num, 'adsl error')
                time.sleep(1)
                continue

        time.sleep(1)


# ***********************************************************
# 读config文件
# ***********************************************************
def readConfig(configfile):
    config = configparser.ConfigParser()
    config.read(configfile)
    for section in config.sections():
        for option in config[section]:
            print(section, option, config.get(section, option))
        print("")
    return config


# ***********************************************************
# 定时清理
# ***********************************************************
# 清理记录文件的时间戳
ClearLastTm = 0


def cleartm():
    global ClearLastTm
    tm = int(time.time())
    # print(tm)
    if tm - ClearLastTm > 3600:  # 每个小时清理一次
        ClearLastTm = tm
        try:
            # os.remove('./nohup.out')    #删除文件
            subprocess.Popen('rm nohup.out -rf', shell = True, stdout = subprocess.PIPE)
            print("remove nohup.out ok")
        except:
            print("remove nohup.out error")


# ***********************************************************
# webserver允许的ip
# ***********************************************************
acceptIP = ['10.31.146.59', '47.94.38.120', '47.94.43.69', '127.0.0.1', '142.44.224.29', '47.93.113.85']

# ***********************************************************
# webserver响应函数
# ***********************************************************
from flask import Flask
# from flask import jsonify
from flask import request

app = Flask(__name__)


@app.route('/webserver', methods = ['post', 'get'])
def webserver():
    # 清理文件
    cleartm()
    ip = request.remote_addr
    if ip not in acceptIP:
        print('no ip ', ip)
        return 'no ip'
    type = request.args.get('type')
    type = str(type)
    url = request.args.get('url')
    url = str(url)
    url = url.replace(" ", "+")
    # print (url)
    n = 0
    while 1:
        for i in range(0, config.getint('webserver', 'threadsNum')):
            # if 0 == read_runstate():
            #    break
            b = QLserver['webserver'].browser[i]
            if 0 == b.state or n > 1800:  # 超过半小时，可能是采集程序删除了任务造成
                b.state = 1
                return b.doOneWebTask(url, type)
        print(crawlerfun.get_date_time(0), 'webserver() waiting.......n =', n, '  b.state =', b.state, url)
        time.sleep(1)
        n = n + 1


# ***********************************************************
# 服务器队列，集成了浏览器和线程
# ***********************************************************
class QLSERVER:
    num = 0
    browser = []
    threads = []


    def __init__(self):
        self.num = 0
        self.browser = []
        self.threads = []


    # def add(self, index, servernum, runtype, diroot, headless, connection,proxypub,ifmg ,browserchoice,timeout,ip):
    def add(self, index, threadsNum, runtype, config):
        # b = Browser(index, servernum, runtype, diroot, headless, connection,proxypub,ifmg,browserchoice,timeout,ip)
        b = Browser(index, threadsNum, runtype, config)
        self.browser.append(b)
        t = threading.Thread(target = b.browserRoot, args = ())
        self.threads.append(t)
        self.num = self.num + 1


    def thread_start(self):
        '''
        for i in range(self.num):
            print ('\t',i ,'threads  start')
            self.threads[i].start()
        '''

        i = 0
        for thread in self.threads:
            print('\t', i, '/', self.num, '/', len(self.threads), 'threads  start')
            # thread.setDaemon(True)  # 2020-01-02 添加线程守护，主线程监控子线程
            thread.start()
            i = i + 1


    def thread_join(self):
        for i in range(self.num):
            self.threads[i].join()


# ***********************************************************
# sftp下载远程文件
# https://blog.csdn.net/tianpy5/article/details/52507324
# ***********************************************************
def sftp_download(host, port, username, password, local, remote):
    ok = 'no'
    sf = paramiko.Transport((host, port))
    sf.connect(username = username, password = password)
    sftp = paramiko.SFTPClient.from_transport(sf)
    try:
        if os.path.isdir(local):  # 判断本地参数是目录还是文件
            for f in sftp.listdir(remote):  # 遍历远程目录
                sftp.get(os.path.join(remote + f), os.path.join(local + f))  # 下载目录中文件
        else:
            sftp.get(remote, local)  # 下载文件
    except:  # Exception,e:
        print('download exception:', e)
    else:
        ok = 'ok'
    sf.close()
    return ok


# ***********************************************************
# __name__
# ***********************************************************
if __name__ == '__main__':

    print("")
    try:
        os.mkdir('./record')
    except:
        print('目录存在')
    # argv = sys.argv
    # port = argv[1]
    config = readConfig("config.cfg")
    # 定义字典
    QLserver = {}
    for section in config.sections():
        runtype = section
        threadsNum = int(config.getint(runtype, 'threadsNum'))
        '''
        headless = config[runtype]['headless']
        diroot = config[runtype]['dir']
        connection = config[runtype]['connect']
        proxypub = config[runtype]['proxypub']
        ifimg = int(config[runtype]['ifimg'])
        browserchoice = config[runtype]['browserchoice']
        timeout = int(config[runtype]['timeout'])
        ip = config[runtype]['ip']
        '''
        # if threadsNum > 0 and 'pppoe' == connection:
        #    change_ip_for_vps()

        QLserver[section] = QLSERVER()
        for i in range(threadsNum):
            print('add', section, i, threadsNum)
            # QLserver[section].add(i, threadsNum, runtype, diroot, headless, connection, proxypub, ifimg, browserchoice, timeout, ip)
            QLserver[section].add(i, threadsNum, runtype, config[runtype])
    # 启动线程
    for server in QLserver:
        print(server, QLserver[server].num)
        QLserver[server].thread_start()

    # 启动5000端口监听,若不指定host='0.0.0.0'，则只允许本机访问  'webserver' ==
    # if config.getint('webserver', 'threadsNum') > 0:
    #	app.run(host='0.0.0.0')

    for server in QLserver:
        QLserver[server].thread_join()

    print('over')

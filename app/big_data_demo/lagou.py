# -*- coding: utf-8 -*-

import requests
import pandas as pd
from matplotlib import pyplot as plt
from stylecloud import gen_stylecloud

def crawl():
    url = 'https://www.lagou.com/jobs/positionAjax.json?city=%E5%8C%97%E4%BA%AC&needAddtionalResult=false'

    data = {'first': False, 'pn': 1, 'kd': '项目经理', 'sid': 'd1751ba898e0499b89c09952cdb49d03'}

    headers = {
        'user-agent': '''Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36''',
        'cookie': '''JSESSIONID=ABAAAECABIEACCA3B5687573CC1805C47970AA3316F6A1C; WEBTJ-ID=2021092下午2:40:12144012-17ba53c85b0339-0df7382770f728-2363163-2073600-17ba53c85b1102; RECOMMEND_TIP=true; PRE_UTM=; PRE_HOST=; PRE_LAND=https://www.lagou.com/; user_trace_token=20210902144012-1dd475f8-bce1-4d13-ab4d-f447d36c8c0a; LGSID=20210902144012-aa193b7b-1e55-44cd-a158-f09374d7b01e; PRE_SITE=https://www.lagou.com; LGUID=20210902144012-018dd478-78cd-49ac-9d4f-00865800252c; privacyPolicyPopup=false; _ga=GA1.2.1183710088.1630564813; sajssdk_2015_cross_new_user=1; sensorsdata2015session={}; index_location_city=北京; TG-TRACK-CODE=index_search; __lg_stoken__=94d33d8c7e6a3f0c9fe45422bdc0bbc5a7e6b72f3f6fa6ae93fd3fc2b319757b2d93e8ea90da66e04cecf811acf0e75f5429356d3b9c1acb3bfb65c09f64dd69d26219bc5fc0; X_MIDDLE_TOKEN=cd9a46118b39980dd078aece92cd8226; SEARCH_ID=eca129a17397403c858f9e8bd4fda0d4; X_HTTP_TOKEN=4f6e433846814f8686946503614ada0bce210d8556; sensorsdata2015jssdkcross={'distinct_id':'17ba53c8c5c28d-016cac137898e7-2363163-2073600-17ba53c8c5d546','first_id':'','props':{'$latest_traffic_source_type':'直接流量','$latest_search_keyword':'未取到值_直接打开','$latest_referrer':'','$os':'Windows','$browser':'Chrome','$browser_version':'90.0.4430.212'},'$device_id':'17ba53c8c5c28d-016cac137898e7-2363163-2073600-17ba53c8c5d546'}; LGRID=20210902144303-80748a57-df91-45ea-9a6c-ad790af742b9''',
        'origin': '''https://www.lagou.com''',
        'referer': '''referer: https://www.lagou.com/jobs/list_%E9%A1%B9%E7%9B%AE%E7%BB%8F%E7%90%86?labelWords=&fromSearch=true&suginput='''
    }

    with open(file = 'jobs_pm.csv', mode = 'w', encoding = 'utf8') as f:

        f.write(
            'positionId, positionName, companyShortName, createTime, city, salary, salaryMonth, workYear, education\n')

        for page in range(1, 31):
            print('爬取第 {} 页 ...'.format(page))

            data['pn'] = page

            response = requests.post(url = url, data = data, headers = headers)

            positions = response.json()['content']['positionResult']['result']

            for pos in positions:
                print(pos['positionId'],
                      pos['positionName'],
                      pos['companyShortName'],
                      pos['createTime'],
                      pos['city'],
                      pos['salary'],
                      pos['salaryMonth'],
                      pos['workYear'],
                      pos['education'],
                      sep = ',',
                      end = '\n',
                      file = f)


def wordCloud():
    # 定义汉语显示字体
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    # 读取数据
    data = pd.read_csv(filepath_or_buffer = 'jobs_pm.csv', sep = ',', encoding = 'utf8')

    return data


def info(data):
    # 查看数据的信息
    data.info()

    # 查看前5行
    data.head(5)

    # 删除重复数据
    data.drop_duplicates(subset = ['positionId'], keep = 'first', inplace = True)
    print(data)

    return data


def salary(data):
    # 工资转换

    # 求平均工资
    salary = data['salary'].apply(func = lambda ele: sum([int(item) for item in ele.replace('k', '').split('-')]) / 2)

    # 计算系数
    salaryMonth = data['salaryMonth'].apply(func = lambda ele: 1 if ele == 0 else ele / 12)

    # 核算为12个月的工资
    data['new_salary'] = salary * salaryMonth

    # 打印数据
    data.info()

    return data


def dataAnalysis(data):
    # 时效性分析
    # 准备数据
    create_time = data['createTime'].apply(func = lambda item: item[:10]).value_counts().sort_index()
    print(create_time)

    # 绘图
    plt.barh(width = create_time.values, y = create_time.index, color = 'blue')

    # 标题
    plt.title(label = '时效性分析')

    # X轴标题
    plt.xlabel(xlabel = '数量')

    # Y轴标题
    plt.ylabel(ylabel = '日期')

    '''
        相关性分析
    '''

    # 准备数据
    names = data['positionName'].value_counts()
    print(names[:10])

    # 绘图
    plt.barh(width = names[:10].values, y = names[:10].index, color = 'green', height = 0.8)

    # 标题
    plt.title(label = '相关性分析')

    # X轴标题
    plt.xlabel(xlabel = '数量')

    # Y轴标题
    plt.ylabel(ylabel = '名称')

    # 生成图形
    gen_stylecloud(text = ' '.join(data['positionName']),
                   font_path = r'c:/Windows/Fonts/STHUPO.TTF',
                   background_color = 'white',
                   output_name = 'names.png',
                   palette = 'cartocolors.diverging.ArmyRose_2',
                   icon_name = 'fas fa-heart',
                   collocations = False)

    '''
        工资分析
    '''
    # 基本分析
    print(data['new_salary'].describe())

    # 直方图
    plt.hist(x = data['new_salary'], bins = 10, color = 'g')

    # 标题
    plt.title(label = '直方图分析')

    # X轴标题
    plt.xlabel(xlabel = '工资')

    # Y轴标题
    plt.ylabel(ylabel = '数量')

    '''
        公司分析
    '''
    # 数据统计
    companyShortName = data['companyShortName'].value_counts()
    print(companyShortName)

    # 绘图
    plt.barh(y = companyShortName[:10].index, width = companyShortName[:10].values, height = 0.5, color = 'blue')

    # 设置标题
    plt.title(label = '公司分析')

    # x轴坐标
    plt.xlabel(xlabel = '数量')

    # y轴坐标
    plt.ylabel(ylabel = '公司')

    '''
        学历要求
    '''
    # 数据统计
    education = data['education'].value_counts()
    print(education)

    # 绘图
    plt.pie(x = education.values, labels = education.index, autopct = '%.2f%%')

    # 设置标题
    plt.title(label = '学历要求')

    '''
        工作年限
    '''
    # 数据统计
    workYear = data['workYear'].value_counts()
    print(workYear)

    # 绘图
    plt.bar(x = workYear.index, height = workYear.values, width = 0.5, color = 'red')

    # 设置标题
    plt.title(label = '工作经验要求')

    # x轴坐标
    plt.xlabel(xlabel = '工作经验')

    # y轴坐标
    plt.ylabel(ylabel = '数量')




    '''
        多因素分析
    '''
    # 数据准备（只看北京和上海的）
    data1 = data[data['city'].isin(values = ('北京', '上海'))]

    # 绘制箱线图
    data1.boxplot(column = ['new_salary'], by = ['education', 'city'], fontsize = 12, figsize = (12, 8))




if __name__ == '__main__':
    crawl()
    data = wordCloud()
    data = info(data)

    data = salary(data)

    data = dataAnalysis(data)

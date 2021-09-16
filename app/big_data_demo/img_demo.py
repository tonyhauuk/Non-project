import numpy as np
from matplotlib import pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def bar():
    month = ['一月', '二月', '三月', '四月', '五月', '六月', '七月']
    income = [50, 66, 55, 65, 70, 80, 200]

    plt.bar(x = month, height = income, width = 0.5, color = 'm')

    # 3，设置标题
    plt.title(label = '上半年收入情况')

    # 4，设置X轴坐标标题
    plt.xlabel(xlabel = '月份')

    # 5，设置y轴坐标标题
    plt.ylabel(ylabel = '收入(元)')

    # 6，保存图形
    plt.savefig(fname = 'demo_for_bar.png')


def pie():
    # 1, 定义数据
    month = ['一月', '二月', '三月', '四月', '五月', '六月']
    income = [150, 66, 55, 65, 70, 80]

    # 2，绘图
    plt.pie(x = income, labels = month, autopct = '%.1f%%')

    # 3，设置标题
    plt.title(label = '上半年收入情况')

    # 4，保存图形
    plt.savefig(fname = 'demo_for_pie.png')


def scatter():
    # 1, 定义数据
    month = ['一月', '二月', '三月', '四月', '五月', '六月']
    income = [50, 66, 55, 65, 70, 80]

    # 2，绘图
    plt.scatter(x = month, y = income, s = 150, c = 'r', marker = '.')

    # 3，设置标题
    plt.title(label = '上半年收入情况')

    # 4，设置X轴标题
    plt.xlabel(xlabel = '月份')

    # 5，设置y轴标题
    plt.ylabel(ylabel = '收入')

    # 6，保存图形
    plt.savefig(fname = 'demo_for_scatter.png')


def plot():
    # 1, 定义数据
    month = ['一月', '二月', '三月', '四月', '五月', '六月']
    income = [50, 66, 55, 65, 70, 80]

    # 2，绘图
    plt.plot(month, income, c = 'b', linewidth = 1, marker = 'o')

    # 3，设置标题
    plt.title(label = '上半年收入情况')

    # 4，设置X轴标题
    plt.xlabel(xlabel = '月份')

    # 5，设置y轴标题
    plt.ylabel(ylabel = '收入')

    # 6，保存图形
    plt.savefig(fname = 'demo_for_plot.png')

if __name__ == '__main__':
    # bar()
    # pie()
    # scatter()
    # plot()

    pass



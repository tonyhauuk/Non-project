import pip
from pip._internal.utils.misc import  get_installed_distributions
from subprocess import call
import time

urlList = ['https://pypi.tuna.tsinghua.edu.cn/simple/', 'https://mirrors.aliyun.com/pypi/simple']

for dist in get_installed_distributions():
    print(dist.project_name)

for dist in get_installed_distributions():
    num = 20
    print('-' * num)
    print('updating:', dist.project_name, '\t')
    call('pip3 install --upgrade ' + dist.project_name + ' -i ' + urlList[0], shell = True)
    print('-' * num)
    print('\t\n')

    '''
    pip3 list --outdated
    pip3 freeze / pip3 list
    pip3 install --upgrade xxxxxxx  /   pip3 install -U xxxxxxxx
    pip3 search salt*
    
    '''

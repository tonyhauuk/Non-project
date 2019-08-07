import os, re

pipList = os.popen('pip3 list --outdated').readlines()

p = re.compile(r'\(.*?\)')

try:
    for i in pipList:
        content = p.sub('', i)
        print(content)
        os.system('pip3 install --upgrade ' + content)
except:
    print('Upgrade failed: ')




#!/usr/bin/python
# -*- coding:utf-8 -*-
from os import path
# Without GUI os must be add below two lines codes
import matplotlib as mpl

mpl.use('Agg')

from matplotlib import pyplot as plt
import jieba
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import imageio
import io
import sys
import time
import re
import os

stopwords = {}
fileName, imageName = '', ''
try:
    fileName = sys.argv[1]
    imageName = sys.argv[2]
except IndexError as e:
    sys.exit(1)


def importStopword(stopDict):
    global stopwords
    f = open(stopDict, 'r', encoding = 'utf-8')
    line = f.readline().rstrip()

    while line:
        stopwords.setdefault(line, 0)
        stopwords[line] = 1
        line = f.readline().rstrip()
    f.close()


def processChinese(content):
    proc = re.compile(r'<[^>]+>', re.S)
    text = proc.sub('', content)
    jieba.enable_parallel(4)
    segGenerator = jieba.cut(text)
    segList = [i for i in segGenerator if i not in stopwords]
    segList = [i for i in segList if i != u' ']
    segList = r' '.join(segList)

    return segList


def deleteFile(fileName):
    if os.path.isfile(fileName):
        os.remove(fileName)


stopDict = '/home/web_dev/tools/word_cloud/stopword.txt'
# importStopword(stopDict)
d = path.dirname(__file__)
text = open(path.join(d, fileName), encoding = 'gbk', errors = 'ignore').read()
text = processChinese(text)
background = imageio.imread('/home/web_dev/tools/word_cloud/test.png')

wc = WordCloud(font_path = '/home/web_dev/tools/word_cloud/msyh.ttf',
               background_color = 'white',
               max_words = 100,
               mask = background,
               random_state = 42)
wc.generate(text)
imgColors = ImageColorGenerator(background)
plt.figure()
plt.imshow(wc)
plt.axis('off')
# plt.show()

wc.to_file(imageName)
time.sleep(5)
deleteFile(fileName)

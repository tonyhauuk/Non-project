from os import path
from matplotlib import pyplot as plt
import jieba
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import imageio

stopwords = {}

def importStopword(fileName):
    global stopwords
    f = open(fileName, 'r', encoding = 'utf-8')
    line = f.readline().rstrip()

    while line:
        stopwords.setdefault(line, 0)
        stopwords[line] = 1
        line = f.readline().rstrip()
    f.close()

def processChinese(content):
    jieba.enable_parallel(4)
    segGenerator = jieba.cut(content)
    segList = [i for i in segGenerator if i not in stopwords]
    segList = [i for i in segList if i != u' ']
    segList = r' '.join(segList)

    return segList


fileName = 'stopword.txt'
importStopword(fileName)
d = path.dirname('')
text  = open(path.join(d, 'data.txt'), encoding = 'utf-8').read()
text = processChinese(text)
background = imageio.imread('test1.png')

wc = WordCloud(font_path = 'msyh.ttf',
               background_color = 'white',
               max_words = 100,
               mask = background,
               random_state = 42)
wc.generate(text)
imgColors = ImageColorGenerator(background)
plt.figure()
plt.imshow(wc)
plt.axis('off')
plt.show()

wc.to_file('word_cloud_generator.png')
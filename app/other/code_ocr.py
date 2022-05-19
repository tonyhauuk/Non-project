from PIL import Image
import pytesseract
import requests

CHS = 'chi_sim'

# imagePath = Image.open('D:\seccode.jpg')
# code = pytesseract.image_to_string(imagePath)
# print('string: ',code)

import sys
from pytesseract import *

# 二值化
threshold = 95
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)

    # 由于都是数字
# 对于识别成字母的 采用该表进行修正
rep = {'O': '0',
       'I': '1',
       'L': '1',
       'Z': '2',
       'S': '8'}


def getverify1(name):
    # 打开图片
    im = Image.open(name)
    # 转化到灰度图
    imgry = im.convert('L')
    # 保存图像
    imgry.save('g' + name)
    # 二值化，采用阈值分割法，threshold为分割点
    out = imgry.point(table, '1')
    out.save('b' + name)
    # 识别
    text = image_to_string(out)
    # 识别对吗
    text = text.strip()
    text = text.upper()
    for r in rep:
        text = text.replace(r, rep[r])
    print('ocr: ' + text)
    return text


getverify1('ooo.jpg')


def imageGrayscaleDeal(image):
    image = image.convert('L')
    # image.show()
    return image


def imageThresholding(image):
    threshold = 160
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)

    image = image.point(table, '1')
    # image.show()

    return image


def imageDownload(url):
    response = requests.get(url)
    with open(imagePath, 'wb') as f:
        f.write(response.content)

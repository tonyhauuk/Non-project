from PIL import Image
import pytesseract
import requests

CHS = 'chi_sim'

imagePath = Image.open('D:\ocr.jpg')
code = pytesseract.image_to_string(imagePath)
print('string: ',code)


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


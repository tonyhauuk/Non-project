import os, re

index = 0
path = 'E:/Download/0118/'
prefix = []
fileList = os.listdir(path)
for i in range(len(fileList)):
    oldName = path + fileList[i]
    # new = fileList[i].replace(prefix[index], '')
    new = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]", "", fileList[i])
    newName = path + new
    try:
        os.rename(oldName, newName)
    except FileExistsError:
        print('Failed file name:', oldName)
        continue
    print("文件%s重命名成功, 新的文件名为%s" % (oldName, newName))



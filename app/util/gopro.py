import os, re




def eachFile(filepath):
    pathDir =  os.listdir(filepath)
    for allDir in pathDir:
        child = os.path.join('%s%s' % (filepath, allDir))

        abPath = child + '/'
        fileList = os.listdir(abPath)
        for i in range(len(fileList)):
            oldName = abPath + fileList[i]
            # new = fileList[i].replace(prefix[index], '')
            if 'MP4' in oldName:
                continue
            new = re.sub(u'LRV', 'LRV.mp4', fileList[i])
            newName = abPath + new
            try:
                os.rename(oldName, newName)
            except FileExistsError:
                print('Failed file name:', oldName)
                continue
            print("文件%s 重命名成功, 新的文件名为 %s" % (oldName, newName))


path = r'E:/gopro/'
eachFile(path)

import os


def delete_particular_file(top, prefix, suffix):
    index = 1
    match = ''

    if prefix == '':
        match = suffix
        index = -1
    elif suffix == '':
        match = prefix
        index = 0



    for root, dirs, files in os.walk(top, topdown = False):
        for file_name in files:
            # print(file_name.split('.')[index])
            if file_name.split('.')[index] == match:
                delete_file_name = os.path.join(root, file_name)
                os.remove(delete_file_name)
                print(f'{delete_file_name} done...')
        # for name in dirs:
        #     os.rmdir(os.path.join(root, name))


if __name__ == '__main__':
    top = r'D:\PyProject\Non-project'
    prefix = 'geckodriver'
    suffix = ''

    delete_particular_file(top, prefix, suffix)

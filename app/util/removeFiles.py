import os


def delete_particular_file(top):
    for root, dirs, files in os.walk(top, topdown = False):
        for file_name in files:
            print(file_name.split('.')[0])
            if file_name.split('.')[0] == 'geckodriver':
                delete_file_name = os.path.join(root, file_name)
                os.remove(delete_file_name)
                print(f'{delete_file_name} done...')
        # for name in dirs:
        #     os.rmdir(os.path.join(root, name))


if __name__ == '__main__':
    top = 'E:\T'
    delete_particular_file(top)

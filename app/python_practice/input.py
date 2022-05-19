try:
    print('This is int test: %d, this is id: %15.2f' % (13, 3.141592657))

except (IndexError, IndexError) as e:
    print(e)


def sortAndPrint(myList):
    newList = [1,34,5,6,7,8]

    for lst in newList:
        myList.append(lst)

    result = sorted(myList)
    print(result)




if __name__ == '__main__':
    myList = [20, 40, 60, 1]
    sortAndPrint(myList)

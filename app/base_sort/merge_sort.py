# from arrays import Array

def mergeSort(array):
    temp = list(len(array))
    merge_sort(array, temp, 0, len(array) - 1)


def merge_sort(array, temp, left, right):
    if left < right:
        middle = (left + right) // 2
        merge_sort(array, temp, left, middle)
        merge_sort(array, temp, middle + 1, right)
        merge(array, temp, left, middle, right)


def merge(array, temp, left, middle, right):
    start = left
    center = middle + 1

    for i in range(left, right + 1):
        if start > middle:
            temp[start] = array[center]
            center += 1
        elif center > right:
            temp[i] = array[start]
            start += 1
        elif array[start] < array[center]:
            temp[i] = array[start]
            start += 1
        else:
            temp[i] = array[center]
            center += 1


    for i in range(left, right + 1):
        array[i] = temp[i]

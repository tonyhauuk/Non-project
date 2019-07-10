def insertionSort(array):
    i = 1

    while i < len(array):
        temp = array[i]
        j = i - 1

        while j >= 0:
            if temp < array[j]:
                array[j + 1] = array[j]
                j -= 1
            else:
                break

        array[j + 1] = temp
        i += 1

    print('Insertion Sort: ')
    print(array)

a = [87987, 4, 587, 637, 4879871, 6, -51, -7, 9, 5, 47, 98465, -87, 768, 78, 695, 8, 981, 98, 7, 6, 879, 252, 18, 79, 54, 8, 98, 6354, 1, 1, 5, 476, 87, 65]
insertionSort(a)

def selectionSort(array):
    i = 0
    while i < len(array) - 1:
        min = i
        j = i + 1
        while j < len(array):
            if array[j] < array[min]:
                min = j

            j += 1

        if min != i:
            temp = array[i]
            array[i] = array[min]
            array[min] = temp

        i += 1

    print('Selection Sort: ')
    print(array)

a = [87987, 4, 587, 637, 4879871, 6, -51, -7, 9, 15, 47, 465, -817, 768, 78, 695, 8, 981, 98, 7, 6, 879, 252, 18, 79, 54, 8, 98, 6354, -1, -1, 5, 476, 87, 65]
selectionSort(a)
def bubbleSort(array):
    n = len(array)
    while n > 1:
        flag = False
        i = 1
        while i < n:
            if array[i]< array[i - 1]:
                temp = array[i]
                array[i] = array[i - 1]
                array[i - 1] = temp
                flag = True

            i += 1

        if not flag:
            break

        n -= 1

    print('Bubble Sort: ')
    print(array)

a = [87987, 4, 587, 637, 4879871, 6, -51, 7, 9, 5, 47, 98465, 87, 768, 78, 695, 8, 981, 98, 7, 6, 879, 252, 18, 79, 54, 8, 98, 6354, 1, 1, 5, 476, 87, 65]
r = bubbleSort(a)

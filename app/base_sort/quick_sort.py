def quickSort(a):
    quick_sort(a, 0, len(a) - 1)
    print(a)

def quick_sort(a, left, right):
    if left < right:
        pivot = median3(a, left, right)
        quick_sort(a, left, pivot - 1)
        quick_sort(a, pivot + 1, right)

def median3(a, left, right):
    center = (left + right) // 2

    pivot = a[center]
    a[center] = a[right]
    a[right] = pivot

    boundary = left
    for i in range(left, right):
        if a[i] < pivot:
            swap(a, i, boundary)
            boundary += 1

    swap(a, right, boundary)

    return boundary

def swap(a, left, right):
    a[left], a[right] = a[right], a[left]

    return a





a = [87987, 4, 587, 637, 4879871, 6, -51, 7, 9, 5, 47, 98465, 87, 768, 78, 695, 8, 981, 98, 7, 6, 879, 252, 18, 79, 54, 8, 98, 6354, 1, 1, 5, 476, 87, 65]
r = quickSort(a)

# print(swap([1,2,3], 1, 2 ))
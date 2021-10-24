
array = [2,4,5,7,8,9,15,20,33,55,66,67,88,99]


def binarysearch(min, max, target):
    middle = (max + min) // 2
    print(min, max, middle, array[middle])

    if max >= min:
        if array[middle] == target:
            print("debug, match found with index:", middle)
            return middle
        if array[middle] > target:
            return binarysearch(min, middle - 1, target)
        else:
            return binarysearch(middle + 1, max, target)
    else:
        return -1

aa =  binarysearch(0, len(array) - 1, 20)

if aa == -1:
    print("Not found", aa)
else:
    print("Found, index:", aa)


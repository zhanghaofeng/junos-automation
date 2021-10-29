
def flatNestedList(input):
    res = []
    for i in input:
        if isinstance(i, list):
            res += flatNestedList(i)
        else:
            res.append(i)
    return res

input = [[1,1],2,[1,0,[3,4,5,[7,8,9,[11,12]]],1]]

if __name__ == '__main__':
    res = flatNestedList(input)
    print(res)

# def flatNestedList(input):
#     for i in input:
#         if isinstance(i, list):
#             flatNestedList(i)
#         else:
#             res.append(i)

# input = [[1,1],2,[1,1]]
# res = []

# if __name__ == '__main__':
#     flatNestedList(input)
#     print(res)
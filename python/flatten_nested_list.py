
def flatNestedList(input):
    for i in input:
        if isinstance(i, list):
            flatNestedList(i)
        else:
            res.append(i)

input = [[1,1],2,[1,1]]
res = []

if __name__ == '__main__':
    flatNestedList(input)
    print(res)

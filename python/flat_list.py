
NestedList = [1, 2, 4, [6, 5, 7], 8, 9, [10,['a', ['b', 'bb', 'cc','dd'], 'c'],12], 13]

result=[]

def flat_list(NestedList):
    for i in NestedList:
        if isinstance(i, list):
            flat_list(i)
        else:
            result.append(i)

if __name__ == "__main__":
    flat_list(NestedList)
    print(result)
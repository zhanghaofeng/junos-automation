import itertools

def possibleNumber(digitSet, n):
    res = [[]]

    pools = [digitSet] * n
    # print(pools)
    for pool in pools:
        # print(res)
        res = [ x + [y] for x in res for y in pool]
    for prod in res:
        yield prod

# def possibleNumber(digitSet, n):
#     res = []
#     temp = itertools.product(digitSet, repeat = n)
#     for item in temp:
#         res.append(item)
#     return res

res = possibleNumber('23', 5)
for i in res:
    print(i)
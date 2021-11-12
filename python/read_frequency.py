
from typing import Counter


def readFrequnency(inputfile, keyword):
    res = dict()
    with open(inputfile) as f:
        line = f.readline()
        while line:
            count = line.lower().count(keyword)
            res[keyword] = res.get(keyword, 0) + count

            # Special case, 

            line = f.readline()
    
    return res
    # res = dict()
    # bigString = ''
    # with open(inputfile) as f:
    #     line = f.readline()
    #     while line:
    #         temp = line.strip().lower()
    #         bigString += temp + ' '
    #         line = f.readline()
    
    # print(bigString)
    # count = bigString.count(keyword)
    # res[keyword] = res.get(keyword, 0) + count
    # return res

if __name__ == '__main__':
    inputfile = '48320-0.txt'
    keyword = 'elementary, dear Watson'
    keyword2 = 'Sherlock Holmes'

    res = readFrequnency(inputfile, keyword2.lower())
    print(res[keyword2.lower()])

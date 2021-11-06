
# 5.5.5.5               15169      18057       8183       0       2  1d 4:13:41 Establ
# 2002::11:7:0:10f        1708       3392       6914       0       2  1d 4:01:40 Establ

import re

def parseLog(inputfile):
    bgpDict = dict()

    with open(inputfile) as f:
        lines = f.readlines()
    
    for line in lines:
        line = line.strip()
        pattern = re.compile(r'(^\d+.\d+.\d+.\d+|^\w{1,4}:.*?)\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+\s+(.*$)')
        Matches = re.match(pattern, line)

        if Matches:
            try:
                neighbor = Matches[1]
                status = Matches[2].split()[-1]   
                if status == 'Establ':
                    bgpDict[neighbor] = status
            except Exception as e:
                print(f'Error when processing line {line} with error {e}')
    return bgpDict

def main():
    inputfile = 'bgpRaw.log'
    res = parseLog(inputfile)
    if res:
        print(len(res))
        for neighbors in res.keys():
            print(neighbors)

if __name__ == '__main__':
    main()
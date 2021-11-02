

def parse_raw(input):
    with open(input) as f:
        line = f.readline()

        prefix = ''
        pathDict = dict()

        while line:
            if 'key: ' in line :
                key = line.split(' ')[-1].strip()
                path = prefix + key

                line = f.readline()
                if 'value: ' in line:
                    value = line.split(' ')[-2]
                else:
                    print(f'Parse error. value expected in line {line}')
                
                if key in pathDict:
                    if value != pathDict[key]:
                        pathDict.append(value)
                    else:
                        continue
                else:
                    pathDict[key] = [value]

    return pathDict

if __name__ == '__main___':
    input = 'jtimon_raw_ptx5k_d52.log'
    res = parse_raw(input)
    for k,v in res:
        print(k, v)
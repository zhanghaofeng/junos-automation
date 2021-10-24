import math
from typing import ItemsView

def debugInfo(msg):
    if debug: print(msg)

def getSpeed(stride, leg):
    g = 9.8
    return (stride / leg - 1) * math.sqrt(leg * g)

def parse_data(dataset1, dataset2):
    result = dict()
    dinoInfo = dict()

    with open(dataset2) as f:
        lines = f.readlines()
    for line in lines:
        try:
            dinoName = line.split(',')[0]
            stride = line.split(',')[1]
            instance = line.split(',')[2].strip()
            if instance == 'bipedal':
                dinoInfo[dinoName] = [stride]
        except Exception as e:
            print(f'Parse {line} with error: {e}')

    with open(dataset1) as f:
        lines = f.readlines()
    for line in lines:
        line.strip()
        try:
            dinoName = line.split(',')[0]
            leg = line.split(',')[1]
        except Exception as e:
            print(f'Parse line {line} error with: {e}')
    
        if dinoName in dinoInfo:
            dinoInfo[dinoName].append(leg)
    debugInfo(dinoInfo)
    if len(dinoInfo) == 0: return None

    for name, info in dinoInfo.items():
        if len(info) != 2: continue
        result[name] = getSpeed(float(dinoInfo[name][0]), float(dinoInfo[name][1]))

    result = sorted(result.items(), key=lambda item: item[1], reverse=True)
    return result

if __name__ == '__main__':
    debug = False
    res = parse_data('dataset1.csv', 'dataset2.csv')
    if res:
        for name in res:
            print(name[0])
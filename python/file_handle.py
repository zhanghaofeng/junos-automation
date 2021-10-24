import math, sys
from collections import OrderedDict

data1 = "dataset1.csv"
data2 = "dataset2.csv"
g = 9.8

def speed(stride_len, leg_lenth):
    return (stride_len/leg_lenth - 1) * math.sqrt(leg_lenth * g)

dino = {}

with open(data2) as f:
    lines = f.readlines()
    for line in lines:
        name = line.split(",")[0]
        if "NAME,STRIDE_LENGTH,STANCE" in line:
            continue
        stride_len = float(line.split(",")[1])
        stance = line.split(",")[2].strip()
        if stance == "bipedal":
            dino[name] = [stride_len]
            dino[name].append(sys.maxint)

with open(data1) as f:
    lines = f.readlines()
    for line in lines:
        if "NAME,LEG_LENGTH,DIET" in line:
            continue
        name = line.split(",")[0]
        leg_lenth = float(line.split(",")[1].strip())

        if name in dino.keys():
            dino[name][1] = leg_lenth
            dino[name].append(speed(dino[name][0], dino[name][1]))


for k,v in dino.items():
    if len(v) < 3:
        dino.pop(k)

dino_sort  = sorted(dino.items(), key= lambda x:x[1][-1], reverse= True)
for name in dino_sort:
    print(name[0])

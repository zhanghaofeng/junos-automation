count  = 1
nums = [1,1,2,3,4,5,4,5,3,-1,2]
dic = {}

for i in nums:
    if i in dic.keys():
        dic[i] += 1
    else:
        dic[i] = 1

for k,v in dic.items():
    if v == 1:
        print(f"Final result is {k}")
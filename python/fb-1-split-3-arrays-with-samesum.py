
def solution(nums):
    n = len(nums)
    if n < 3: return None
    total = sum(nums) 
    if total % 3 != 0: 
        return None
    else:
        target = total // 3
    
    temp, start, res = 0, 0, list()
    for i in range(n):
        temp += nums[i]
        if temp == target: 
            res.append(nums[start:i+1])
            temp = 0
            start = i+1
    
    if len(res) != 3: return None
    else:
        return res

test = [3,5,8,0,8]

if __name__ == '__main__':
    res = solution(test)
    print(res)
    
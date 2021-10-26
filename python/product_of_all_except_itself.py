# Given an array nums of n integers where n > 1,  
# return an array output such that output[i] is 
# equal to the product of all the elements of nums except nums[i]

# Solution 1: O(n^2)
# def getProductExceptItself(index, nums):
#     res = 1
#     for i in range(len(nums)):
#         if i == index: continue
#         else:
#             res = res * nums[i]
#     return res

# def getProduct(nums):
#     res = list()
#     for i in range(len(nums)):
#         res.append(getProductExceptItself(i, nums))
    
#     return res

# Solution 2: O(n)

def getProductWithOneZero(nums):
    zeroIndex = nums.index(0)
    total = 1
    res = list()
    for i in range(len(nums)):
        if i == zeroIndex: continue
        total = total * nums[i]
    for i in range(len(nums)):
        if i == zeroIndex: res.append(total)
        else: res.append(0)
    return res

def getProduct(nums):
    if nums.count(0) > 1: return [ 0 ] * len(nums)
    if nums.count(0) == 1: return getProductWithOneZero(nums)
    # No zeros in nums. 
    total, res = 1, []
    for num in nums: total = total * num
    for i in range(len(nums)):
        res.append(total // nums[i])
    return res

input = [1,0,5,7,0,11]

if __name__ == '__main__':
    print(getProduct(input))
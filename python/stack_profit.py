
def max_profile(index, nums):
    profit= dict()
    for i in range(1, len(nums)):
        profit[i] = nums[i] - nums[0]
    
    profit = sorted(profit.items(), key= lambda item:item[1], reverse= True)
    print(profit)
    return [index, index+profit[0][0],profit[0][1]]

def find_buy_sell_stock(nums):
    l = len(nums)
    if l == 0 or l == 1: return None
    currentMax = max_profile(0, nums)
    
    for i in range(1, len(nums)-1):
        res = max_profile(i, nums[i:])
        if res[2] > currentMax[2]:
            currentMax = res
    return currentMax

nums = [21,12,11,9,10,1,0]

if __name__ == '__main__':
    res = find_buy_sell_stock(nums)
    print(res)
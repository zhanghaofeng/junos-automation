# https://leetcode.com/problems/house-robber/
# DP thinking..
# [3,1,3,1,1,5,4,2]
# [3,1,6,4,7,11,11,13]


class Solution:
    def rob(self, nums: List[int]) -> int:
        if len(nums) <= 2: return max(nums)
        
        robList = [0] * len(nums)
        robList[0], robList[1] = nums[0], nums[1]
        
        for i in range(2, len(nums)):
            robList[i] = max(robList[:i-1]) + nums[i]
            
        return max(robList)
# https://leetcode.com/problems/climbing-stairs
# The steps to reach n =  steps to reach n-1 + steps to reach n-2
# This code will wor, as Fibcinno array, but not optimized. 
# class Solution:
#     def climbStairs(self, n: int) -> int:
        
#         if n == 0 or n == 1: 
#             return 1
#         else:
#             return self.climbStairs(n-1) + self.climbStairs(n-2)

class Solution:
    def climbStairs(self, n: int) -> int:
        memo = dict()

        def helper(n):
            if n == 0 or n == 1: 
                return 1
            if n in memo:
                return memo[n]
            else:
                memo[n] = helper(n-1) + helper(n-2)
                return memo[n]
        return helper(n)

myTest = Solution()
res = myTest.climbStairs(38)
print(res)
from random import randint
class Solution:

    def __init__(self, nums):
        self.nums = nums
        self.n = len(nums)

    def reset(self):
        return self.nums

    def shuffle(self):
        arrayDict = dict()
        for i in range(self.n):
            while True:
                if len(arrayDict) == self.n: break
                j = randint(0, self.n-1)
                if j not in arrayDict.keys():
                    arrayDict[j] = self.nums[i]
                    break
        res = []
        for i in range(self.n):
            res.append(arrayDict[i])
        return res

if __name__ == '__main__':
    input = [3,4,5,2,1,1,4,88,99,334,4,52,2,7]
    myTest = Solution(input)
    print(input)
    print(myTest.shuffle())
    print(myTest.reset())
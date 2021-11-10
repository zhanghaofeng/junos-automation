# https://leetcode.com/problems/knight-dialer/

import itertools

class Solution:
    
    # x, y is the index of the digit, say [0,0] is for 1
    def validIndex(self, indexList):
        if indexList[0] > 3 or indexList[1] > 2: return False
        if indexList == [3, 0] or indexList == [3, 2]: return False
        if indexList[0] < 0 or indexList[1] < 0: return False
        return True
    
    # for each position on dial pad, it has 8 possibilities. 
    # input: the position on dial pad
    # output: all possible *valid* positions list of list
    def validNumbers(self, indexList):
        if not self.validIndex(indexList):
            return None
        newList = []
        newList.append([indexList[0] + 2, indexList[1] + 1])
        newList.append([indexList[0] + 2, indexList[1] - 1])
        newList.append([indexList[0] - 2, indexList[1] + 1])
        newList.append([indexList[0] - 2, indexList[1] - 1])
        newList.append([indexList[0] + 1, indexList[1] + 2])
        newList.append([indexList[0] + 1, indexList[1] - 2])
        newList.append([indexList[0] - 1, indexList[1] + 2])
        newList.append([indexList[0] - 1, indexList[1] - 2])

        res = []
        
        for i in newList:
            if self.validIndex(i): res.append(i) 

        return res
    
    # Input location
    # Output single digits [0-9]
    def numberBaseIndex(self, indexList):
        matrix = [['1','2','3'], ['4','5','6'], ['7','8','9'], ['*','0','#']]
        return matrix[indexList[0]][indexList[1]]
    
    # input set of numbers and cell number
    # output possible unique numbers
    def possibleNumber(self, digitSet, n):
        res = [[]]
        pools = [digitSet] * n
        # print(pools)
        for pool in pools:
            # print(res)
            res = [ x + [y] for x in res for y in pool]
        for prod in res:
            yield prod
    # def possibleNumber(self, digitSet, n):
    #     res = []
    #     temp = itertools.product(digitSet, repeat = n)
    #     for item in temp:
    #         res.append(item)
    #     return res

    def knightDialer(self, n: int) -> int:
        res = []
        for i in range(4):
            for j in range(3):
                prefix = self.numberBaseIndex([i,j])
                validDigits = self.validNumbers([i, j])

                if not validDigits: continue
                digitSet = []
                for digit in validDigits:
                    digitSet.append(self.numberBaseIndex(digit))
                if not digitSet: continue

                temp = self.possibleNumber(digitSet, n-1)
                for items in temp:
                    res.append([prefix] + items) 
        return res

if __name__ == '__main__':
    myClass = Solution()
    # res = myClass.knightDialer(3)
    # for i in res:
    #     print(''.join(i))
    # print(len(res))
    #print(''.join(i) for i in res, len(res))
    res = []
    for i in myClass.possibleNumber('ABC', 2):
        res.append(i)
    print(res)
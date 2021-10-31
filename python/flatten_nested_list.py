
# def flatNestedList(input):
#     res = []
#     for i in input:
#         if isinstance(i, list):
#             res += flatNestedList(i)
#         else:
#             res.append(i)
#     return res

# input = [[1,1],2,[1,0,[3,4,5,[7,8,9,[11,12]]],1]]

# if __name__ == '__main__':
#     res = flatNestedList(input)
#     print(res)

# def flatNestedList(input):
#     for i in input:
#         if isinstance(i, list):
#             flatNestedList(i)
#         else:
#             res.append(i)

# input = [[1,1],2,[1,1]]
# res = []

# if __name__ == '__main__':
#     flatNestedList(input)
#     print(res)

# """
# This is the interface that allows for creating nested lists.
# You should not implement it, or speculate about its implementation
# """
#class NestedInteger:
#    def isInteger(self) -> bool:
#        """
#        @return True if this NestedInteger holds a single integer, rather than a nested list.
#        """
#
#    def getInteger(self) -> int:
#        """
#        @return the single integer that this NestedInteger holds, if it holds a single integer
#        Return None if this NestedInteger holds a nested list
#        """
#
#    def getList(self) -> [NestedInteger]:
#        """
#        @return the nested list that this NestedInteger holds, if it holds a nested list
#        Return None if this NestedInteger holds a single integer
#        """

class NestedIterator:
    def __init__(self, nestedList):
        self.nestedList = nestedList
        self.result = self.getFlatList(self.nestedList)
        self.index = 0
        
    def getFlatList(self, nestedList):
        result = []
        for i in nestedList:
            if isinstance(i, list):
                result += self.getFlatList(i)
            else:
                result.append(i)
        return result
                
    def next(self) -> int:
        self.index += 1
        if self.index <= len(self.result):
            return self.result[self.index - 1]
    
    def hasNext(self) -> bool:
        if self.index < len(self.result):
            return True
        else:
            return False


if __name__ == '__main__':
    input = [[1,1],2,[1,1]]
    test = NestedIterator(input)
    result = []
    while test.hasNext():
        result.append(test.next())
    print(result)
    # print(test.getFlatList(input))
    # print(test.result)
    # while test.hasNext:
    #     print(test.next)
    # while test.next:
    #     print(test.next)
# https://leetcode.com/problems/knight-dialer/
# Meaningful discussion: https://alexgolec.dev/google-interview-questions-deconstructed-the-knights-dialer/ 

class Solution:
    # this solution works if n==4
    # def currentPossibilities(self, position, repeat):
    #     NEIGHBORS_MAP = {
    #         1: (6, 8),
    #         2: (7, 9),
    #         3: (4, 8),
    #         4: (3, 9, 0),
    #         5: tuple(),  # 5 has no neighbors
    #         6: (1, 7, 0),
    #         7: (2, 6),
    #         8: (1, 3),
    #         9: (2, 4),
    #         0: (4, 6),
    #     }
    #     res = 0
    #     if repeat == 1: return 1
    #     #if position == 5: return None
    #     for i in NEIGHBORS_MAP[position]:
    #         res += self.currentPossibilities(i, repeat-1)
    #     return res
    
    # this solutions works if n== 3131
#     def currentPossibilities(self, position, repeat):
#         NEIGHBORS_MAP = {
#             1: (6, 8),
#             2: (7, 9),
#             3: (4, 8),
#             4: (3, 9, 0),
#             5: tuple(),  # 5 has no neighbors
#             6: (1, 7, 0),
#             7: (2, 6),
#             8: (1, 3),
#             9: (2, 4),
#             0: (4, 6),
#         }
#         memo = {}
        
#         def helper(position, repeat):
#             res = 0
#             if repeat == 1: return 1
#             for i in NEIGHBORS_MAP[position]:     
#                 if (i, repeat-1) in memo.keys():
#                     res += memo[(i, repeat-1)]
#                 else:
#                     memo[(i, repeat-1)] = helper(i, repeat-1)
#                     res += memo[(i, repeat-1)]
#             return res
#         return helper(position, repeat)
    
    def knightDialer(self, n: int) -> int:
        NEIGHBORS_MAP = {
            1: (6, 8),
            2: (7, 9),
            3: (4, 8),
            4: (3, 9, 0),
            5: tuple(),  # 5 has no neighbors
            6: (1, 7, 0),
            7: (2, 6),
            8: (1, 3),
            9: (2, 4),
            0: (4, 6),
        }
        memo = {}
        
        def helper(position, repeat):
            res = 0
            if repeat == 1: return 1
            for i in NEIGHBORS_MAP[position]:     
                if (i, repeat-1) in memo.keys():
                    res += memo[(i, repeat-1)]
                else:
                    memo[(i, repeat-1)] = helper(i, repeat-1)
                    res += memo[(i, repeat-1)]
            return res
        
        res = 0
        for position in range(10):
            res += helper(position, n)
        return res % (10**9 + 7)